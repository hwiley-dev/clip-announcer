#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "$0")/.." && pwd)"
JS_FILE="$ROOT_DIR/clip_announcer.js"
TTS_FILE="$ROOT_DIR/clip_announcer_tts.js"

has_match() {
  local pattern="$1"
  local file="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -q "$pattern" "$file"
  else
    grep -Eq "$pattern" "$file"
  fi
}

require_pattern() {
  local file="$1"
  local pattern="$2"
  local label="$3"
  if ! has_match "$pattern" "$file"; then
    echo "[FAIL] missing $label in $file"
    exit 1
  fi
}

require_pattern "$JS_FILE" '^function init\(' 'JS command: init()'
require_pattern "$JS_FILE" '^function announce\(' 'JS command: announce()'
require_pattern "$JS_FILE" '^function announce_where\(' 'JS command: announce_where()'
require_pattern "$JS_FILE" '^function announce_what\(' 'JS command: announce_what()'
require_pattern "$JS_FILE" '^function announce_state\(' 'JS command: announce_state()'
require_pattern "$JS_FILE" '^function dump_state\(' 'JS command: dump_state()'
require_pattern "$JS_FILE" '^function refresh\(' 'JS command: refresh()'
require_pattern "$JS_FILE" '\[ClipAnnouncer\]' 'JS log prefix'
require_pattern "$JS_FILE" '\[ClipAnnouncer\]\[ERROR\]' 'JS error prefix'

require_pattern "$TTS_FILE" 'maxApi\.addHandler\("speak"' 'TTS handler: speak'
require_pattern "$TTS_FILE" 'maxApi\.addHandler\("speak_test"' 'TTS handler: speak_test'
require_pattern "$TTS_FILE" 'maxApi\.addHandler\("stop"' 'TTS handler: stop'
require_pattern "$TTS_FILE" '\[ClipAnnouncer:TTS\]' 'TTS log prefix'
require_pattern "$TTS_FILE" '\[ClipAnnouncer:TTS\]\[ERROR\]' 'TTS error prefix'

echo "[OK] interface contract verified"
