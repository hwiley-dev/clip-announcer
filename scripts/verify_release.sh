#!/usr/bin/env bash
set -euo pipefail

STRICT=1
DEVICE="dist/ClipAnnouncer.amxd"

for arg in "$@"; do
  case "$arg" in
    --allow-sidecar)
      STRICT=0
      ;;
    --strict)
      STRICT=1
      ;;
    *)
      DEVICE="$arg"
      ;;
  esac
done

if [[ ! -f "$DEVICE" ]]; then
  echo "[FAIL] release artifact not found: $DEVICE"
  exit 1
fi

DUMP_FILE="$(mktemp)"
trap 'rm -f "$DUMP_FILE"' EXIT
strings "$DEVICE" > "$DUMP_FILE"

has_match() {
  local pattern="$1"
  local file="$2"
  if command -v rg >/dev/null 2>&1; then
    rg -q "$pattern" "$file"
  else
    grep -Eq "$pattern" "$file"
  fi
}

must_have() {
  local pattern="$1"
  local label="$2"
  if ! has_match "$pattern" "$DUMP_FILE"; then
    echo "[FAIL] missing release requirement: $label"
    exit 1
  fi
}

must_not_have() {
  local pattern="$1"
  local label="$2"
  if has_match "$pattern" "$DUMP_FILE"; then
    echo "[FAIL] release should not contain: $label"
    exit 1
  fi
}

must_have 'js clip_announcer\.js' 'js runtime object'
must_have 'node\.script clip_announcer_tts\.js' 'node runtime object'
must_have 'live\.thisdevice' 'live.thisdevice init object'
must_have 'where_button' 'where button parameter'
must_have 'what_button' 'what button parameter'
must_have 'state_button' 'state button parameter'
must_have 'announce_where' 'where announce message route'
must_have 'announce_what' 'what announce message route'
must_have 'announce_state' 'state announce message route'
must_have 'dump_state' 'diagnostic message'
must_have 'speak_test' 'speech diagnostic message'
must_not_have 'Build your MIDI effect here' 'empty template text'

if [[ "$STRICT" -eq 1 ]]; then
  # Freeze may keep metadata flags/paths even when script bodies are embedded.
  # Strict mode validates embedded content signatures instead of raw embed flags.
  must_have 'announce aborted: state unavailable' 'embedded clip_announcer.js content'
  must_have 'announce_where' '3-button JS command content'
  must_have 'buildWhereSummary' 'WHERE summary builder content'
  must_have 'buildWhatSummary' 'WHAT summary builder content'
  must_have 'buildStateSummary' 'STATE summary builder content'
  must_have 'Clip announcer speech test' 'embedded clip_announcer_tts.js content'
  if has_match '"embed" : 0' "$DUMP_FILE"; then
    echo "[WARN] embed flag still reports 0 in metadata; validated embedded content signatures instead"
  fi
  if has_match '/Users/hunterwiley/Code-Projects/Clip-Announcer' "$DUMP_FILE"; then
    echo "[WARN] local path metadata still present in dependency_cache"
  fi
  echo "[OK] strict release verification passed"
else
  if has_match '"embed" : 0' "$DUMP_FILE"; then
    echo "[WARN] artifact still appears to reference unembedded scripts"
  fi
  echo "[OK] non-strict release verification passed"
fi
