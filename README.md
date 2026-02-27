# Clip Announcer Accessibility Tool

Clip Announcer is an Accessibility Screen Reader Tool for Max for Live device. It reads the currently highlighted clip context in Ableton Live and speaks a deterministic summary using macOS text-to-speech.

## What It Does

- Adds three category buttons in the device UI: `WHERE`, `WHAT`, `STATE`.
- Reads selected track and highlighted clip slot state through LiveAPI.
- Logs deterministic status details to the Max Console.
- Speaks a short summary through `node.script` using the macOS `say` command.
- Uses button-driven triggers only (no raw MIDI note trigger path).

## Trigger Model

- Manual triggers: click `WHERE`, `WHAT`, or `STATE`.
- Keyboard mapping path: map each button in Ableton Live Key Map mode.
- No default MIDI note trigger is wired, to avoid collisions with instrument keyboard input.
- Live/M4L still does not expose a deterministic per-device global keyboard combo API, so mapping behavior remains Live-focus dependent.

## Repository Layout

- `ClipAnnouncer.dev.amxd`: editable source device.
- `ClipAnnouncer.maxpat`: patch source.
- `clip_announcer.js`: LiveAPI state and summary logic.
- `clip_announcer_tts.js`: speech process logic.
- `dist/ClipAnnouncer.amxd`: release artifact.
- `scripts/`: release validation and packaging scripts.
- `RELEASE.md`: release contract and checklist.
- `TEST_PLAN_PHASE2.md`: test plan.

## Quick Start

1. Open Ableton Live with Max for Live available.
2. Load `dist/ClipAnnouncer.amxd` on a MIDI track.
3. Highlight a clip slot in Session View.
4. Trigger announce by clicking `WHERE`, `WHAT`, or `STATE`.
5. Optional: enter Ableton Key Map mode and map keyboard keys to those three buttons.

## Release Workflow

Run these from the repository root:

```bash
./scripts/verify_contract.sh
./scripts/prepare_release.sh
# freeze/embed in Max for Live and save dist/ClipAnnouncer.amxd
./scripts/verify_release.sh dist/ClipAnnouncer.amxd --strict
./scripts/finalize_release.sh dist/ClipAnnouncer.amxd
```

Detailed release requirements and pass/fail checks are documented in `RELEASE.md`.

## Notes

- Speech output currently uses macOS `say`.
- This repository includes a design paper at `WHITEPAPER_DEVICE_KEYBOARD_INPUT_API.md` discussing deterministic keyboard input for accessibility workflows.
