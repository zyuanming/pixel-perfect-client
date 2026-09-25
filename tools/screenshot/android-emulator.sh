#!/usr/bin/env bash
set -euo pipefail

OUT="${1:-.pixel-perfect/captures/android-emulator.png}"
SERIAL="${2:-}"

mkdir -p "$(dirname "$OUT")"

if ! command -v adb >/dev/null 2>&1; then
  echo "adb is required." >&2
  exit 2
fi

if [[ -n "$SERIAL" ]]; then
  adb -s "$SERIAL" exec-out screencap -p > "$OUT"
else
  adb exec-out screencap -p > "$OUT"
fi

echo "$OUT"
