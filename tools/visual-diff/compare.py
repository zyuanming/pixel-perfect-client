#!/usr/bin/env python3
from __future__ import annotations

import argparse
import json
import math
from pathlib import Path
from typing import Any

import numpy as np
from PIL import Image, ImageChops


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description="Compare a reference screenshot with a rendered implementation."
    )
    parser.add_argument("--reference", required=True, type=Path)
    parser.add_argument("--actual", required=True, type=Path)
    parser.add_argument("--out", required=True, type=Path)
    parser.add_argument(
        "--normalize",
        choices=["strict", "resize-actual"],
        default="strict",
        help="How to handle dimension mismatch.",
    )
    parser.add_argument(
        "--pixel-threshold",
        type=float,
        default=12.0 / 255.0,
        help="Per-pixel max-channel delta counted as changed (0..1).",
    )
    parser.add_argument(
        "--max-changed-ratio",
        type=float,
        default=0.02,
        help="Maximum changed-pixel ratio for baseline pass.",
    )
    parser.add_argument(
        "--max-mae",
        type=float,
        default=0.015,
        help="Maximum mean absolute error for baseline pass.",
    )
    parser.add_argument(
        "--tile-size",
        type=int,
        default=64,
        help="Tile size used to report high-error regions.",
    )
    parser.add_argument(
        "--top-regions",
        type=int,
        default=8,
        help="Maximum number of high-error regions to report.",
    )
    return parser.parse_args()


def load_rgba(path: Path) -> Image.Image:
    if not path.exists():
        raise FileNotFoundError(path)
    return Image.open(path).convert("RGBA")


def flatten_on_white(image: Image.Image) -> Image.Image:
    bg = Image.new("RGBA", image.size, (255, 255, 255, 255))
    return Image.alpha_composite(bg, image).convert("RGB")


def global_ssim(reference: np.ndarray, actual: np.ndarray) -> float:
    # Lightweight global SSIM-like metric. It is intentionally not a replacement
    # for windowed perceptual analysis; it is only a baseline signal.
    ref = reference.astype(np.float64)
    act = actual.astype(np.float64)

    # Luma approximation.
    ref_y = 0.2126 * ref[..., 0] + 0.7152 * ref[..., 1] + 0.0722 * ref[..., 2]
    act_y = 0.2126 * act[..., 0] + 0.7152 * act[..., 1] + 0.0722 * act[..., 2]

    mu_x = float(ref_y.mean())
    mu_y = float(act_y.mean())
    var_x = float(ref_y.var())
    var_y = float(act_y.var())
    cov = float(((ref_y - mu_x) * (act_y - mu_y)).mean())

    c1 = (0.01 * 255.0) ** 2
    c2 = (0.03 * 255.0) ** 2

    numerator = (2 * mu_x * mu_y + c1) * (2 * cov + c2)
    denominator = (mu_x * mu_x + mu_y * mu_y + c1) * (var_x + var_y + c2)

    if denominator == 0:
        return 1.0 if numerator == 0 else 0.0
    return max(-1.0, min(1.0, numerator / denominator))


def top_error_tiles(error_map: np.ndarray, tile_size: int, count: int) -> list[dict[str, Any]]:
    h, w = error_map.shape
    tiles: list[dict[str, Any]] = []

    for y in range(0, h, tile_size):
        for x in range(0, w, tile_size):
            tile = error_map[y : min(y + tile_size, h), x : min(x + tile_size, w)]
            if tile.size == 0:
                continue
            tiles.append(
                {
                    "x": x,
                    "y": y,
                    "width": int(tile.shape[1]),
                    "height": int(tile.shape[0]),
                    "meanError": float(tile.mean()),
                    "maxError": float(tile.max()),
                }
            )

    tiles.sort(key=lambda item: (item["meanError"], item["maxError"]), reverse=True)
    return tiles[: max(0, count)]


def save_heatmap(error_map: np.ndarray, output: Path) -> None:
    intensity = np.clip(error_map * 255.0, 0, 255).astype(np.uint8)
    Image.fromarray(intensity, mode="L").save(output)


def main() -> int:
    args = parse_args()
    args.out.mkdir(parents=True, exist_ok=True)

    reference_raw = load_rgba(args.reference)
    actual_raw = load_rgba(args.actual)

    reference_size = reference_raw.size
    actual_original_size = actual_raw.size
    normalization = "none"

    if reference_raw.size != actual_raw.size:
        if args.normalize == "strict":
            report = {
                "finalResult": "blocked",
                "reason": "dimension-mismatch",
                "reference": {
                    "path": str(args.reference),
                    "width": reference_raw.width,
                    "height": reference_raw.height,
                },
                "actual": {
                    "path": str(args.actual),
                    "width": actual_raw.width,
                    "height": actual_raw.height,
                },
                "normalization": "strict",
            }
            (args.out / "report.json").write_text(
                json.dumps(report, indent=2, ensure_ascii=False) + "\n",
                encoding="utf-8",
            )
            print(json.dumps(report, indent=2, ensure_ascii=False))
            return 2

        actual_raw = actual_raw.resize(reference_raw.size, Image.Resampling.LANCZOS)
        normalization = "resize-actual"

    reference = flatten_on_white(reference_raw)
    actual = flatten_on_white(actual_raw)

    ref = np.asarray(reference).astype(np.float32) / 255.0
    act = np.asarray(actual).astype(np.float32) / 255.0

    abs_diff = np.abs(ref - act)
    per_pixel = abs_diff.max(axis=2)

    mae = float(abs_diff.mean())
    rmse = float(math.sqrt(float(np.square(ref - act).mean())))
    changed_ratio = float((per_pixel > args.pixel_threshold).mean())
    mean_pixel_delta = float(per_pixel.mean())
    max_pixel_delta = float(per_pixel.max())
    ssim = float(global_ssim(np.asarray(reference), np.asarray(actual)))

    passed = changed_ratio <= args.max_changed_ratio and mae <= args.max_mae

    # Visual artifacts.
    diff = ImageChops.difference(reference, actual)
    diff.save(args.out / "diff.png")

    save_heatmap(per_pixel, args.out / "heatmap.png")
    Image.blend(reference, actual, alpha=0.5).save(args.out / "overlay.png")

    top_regions = top_error_tiles(per_pixel, args.tile_size, args.top_regions)

    report = {
        "finalResult": "passed" if passed else "blocked",
        "reference": {
            "path": str(args.reference),
            "width": reference_size[0],
            "height": reference_size[1],
        },
        "actual": {
            "path": str(args.actual),
            "originalWidth": actual_original_size[0],
            "originalHeight": actual_original_size[1],
            "comparedWidth": actual.width,
            "comparedHeight": actual.height,
        },
        "normalization": normalization,
        "thresholds": {
            "pixelThreshold": args.pixel_threshold,
            "maxChangedRatio": args.max_changed_ratio,
            "maxMae": args.max_mae,
        },
        "metrics": {
            "mae": mae,
            "rmse": rmse,
            "changedRatio": changed_ratio,
            "meanPixelDelta": mean_pixel_delta,
            "maxPixelDelta": max_pixel_delta,
            "globalSsimLike": ssim,
        },
        "topErrorRegions": top_regions,
        "artifacts": {
            "diff": str(args.out / "diff.png"),
            "heatmap": str(args.out / "heatmap.png"),
            "overlay": str(args.out / "overlay.png"),
        },
        "note": (
            "Numeric metrics are baseline evidence only. Final visual QA must still inspect "
            "geometry, typography, colors, assets, content, and runtime state."
        ),
    }

    (args.out / "report.json").write_text(
        json.dumps(report, indent=2, ensure_ascii=False) + "\n",
        encoding="utf-8",
    )
    print(json.dumps(report, indent=2, ensure_ascii=False))

    return 0 if passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
