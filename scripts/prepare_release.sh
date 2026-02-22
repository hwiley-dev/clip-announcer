#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
SRC_DEVICE="${1:-$ROOT_DIR/ClipAnnouncer.dev.amxd}"
OUT_DEVICE="${2:-$ROOT_DIR/dist/ClipAnnouncer.amxd}"
DIST_DIR="$(dirname "$OUT_DEVICE")"
SRC_JS="$ROOT_DIR/clip_announcer.js"
SRC_TTS="$ROOT_DIR/clip_announcer_tts.js"
OUT_JS="$DIST_DIR/clip_announcer.js"
OUT_TTS="$DIST_DIR/clip_announcer_tts.js"

if [[ ! -f "$SRC_DEVICE" ]]; then
  echo "[FAIL] source device not found: $SRC_DEVICE"
  exit 1
fi

if [[ ! -f "$SRC_JS" || ! -f "$SRC_TTS" ]]; then
  echo "[FAIL] missing sidecar JS source files in project root"
  exit 1
fi

mkdir -p "$DIST_DIR"
cp -f "$SRC_DEVICE" "$OUT_DEVICE"
cp -f "$SRC_JS" "$OUT_JS"
cp -f "$SRC_TTS" "$OUT_TTS"

# Ensure node.script textfile is marked embeddable in staged release device.
# Max still needs Freeze Device + Save to actually bake dependencies.
python3 - "$OUT_DEVICE" <<'PY'
import re
import sys
from pathlib import Path

device = Path(sys.argv[1])
data = device.read_bytes()
pattern = re.compile(rb'("embed"\s*:\s*)0')
data, count = pattern.subn(rb'\g<1>1', data)

if count > 0:
    device.write_bytes(data)
    print(f"[OK] set embed flag to 1 in staged release artifact ({count} replacements)")
else:
    print("[WARN] no embed flag patch applied (pattern not found)")
PY

echo "[OK] staged release artifact: $OUT_DEVICE"
echo "[OK] staged sidecars for freeze:"
echo "      $OUT_JS"
echo "      $OUT_TTS"
echo "[NEXT] open $OUT_DEVICE in Max, click Freeze Device, and Save"
echo "[NEXT] after freeze/save, run strict verify and then remove staged sidecars from dist"

"$ROOT_DIR/scripts/verify_release.sh" "$OUT_DEVICE" --allow-sidecar
