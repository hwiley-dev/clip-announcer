#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
DEVICE="${1:-$ROOT_DIR/dist/ClipAnnouncer.amxd}"
DIST_DIR="$(dirname "$DEVICE")"
JS_SIDE="$DIST_DIR/clip_announcer.js"
TTS_SIDE="$DIST_DIR/clip_announcer_tts.js"

if [[ ! -f "$DEVICE" ]]; then
  echo "[FAIL] release artifact not found: $DEVICE"
  exit 1
fi

"$ROOT_DIR/scripts/verify_release.sh" "$DEVICE" --strict

if [[ -f "$JS_SIDE" ]]; then
  rm -f "$JS_SIDE"
  echo "[OK] removed staged sidecar: $JS_SIDE"
fi

if [[ -f "$TTS_SIDE" ]]; then
  rm -f "$TTS_SIDE"
  echo "[OK] removed staged sidecar: $TTS_SIDE"
fi

echo "[OK] release finalized: $DEVICE"
