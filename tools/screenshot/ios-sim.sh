#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-.pixel-perfect/captures/ios-simulator.png}"
DEVICE="${2:-booted}"

mkdir -p "$(dirname "$OUT")"

if ! command -v xcrun >/dev/null 2>&1; then
  echo "xcrun is required (Xcode Command Line Tools)." >&2
  exit 2
fi

xcrun simctl io "$DEVICE" screenshot "$OUT"
echo "$OUT"
