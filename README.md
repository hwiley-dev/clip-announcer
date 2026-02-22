# Clip Announcer

Clip Announcer is a Max for Live device that reads the currently highlighted clip context in Ableton Live and speaks a deterministic summary using macOS text-to-speech.

## What It Does

- Adds an `ANNOUNCE` button in the device UI.
- Reads selected track and highlighted clip slot state through LiveAPI.
- Logs deterministic status details to the Max Console.
- Speaks a short summary through `node.script` using the macOS `say` command.
- Supports a no-mapping hardware/software trigger via MIDI note `60` (velocity > 0).

## Trigger Model

- Manual trigger: click `ANNOUNCE`.
- Deterministic auto trigger path: send MIDI note `60`.
- Computer keyboard pre-binding per device instance is not guaranteed in Live/M4L, so keyboard-only automation may be focus/conflict dependent.

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
4. Trigger announce by:
   - Clicking `ANNOUNCE`, or
   - Sending MIDI note `60` with velocity > 0.

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
