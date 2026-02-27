# Clip Announcer Phase 2 Release Guide

## Artifact Contract

- Editable source device: `/Users/hunterwiley/Code-Projects/Clip-Announcer/ClipAnnouncer.dev.amxd`
- Distributable release artifact: `/Users/hunterwiley/Code-Projects/Clip-Announcer/dist/ClipAnnouncer.amxd`
- Legacy artifact archive: `/Users/hunterwiley/Code-Projects/Clip-Announcer/archive/`

Users should receive only `dist/ClipAnnouncer.amxd`.

## Interface Contract (must remain stable)

### `clip_announcer.js` commands

- `init`
- `announce`
- `dump_state`
- `refresh`

### `clip_announcer_tts.js` handlers

- `speak`
- `speak_test`
- `stop`

### Log prefixes

- JS: `[ClipAnnouncer]`, `[ClipAnnouncer][ERROR]`
- TTS: `[ClipAnnouncer:TTS]`, `[ClipAnnouncer:TTS][ERROR]`

### Trigger behavior

- Category announce can be triggered by:
  - Clicking `WHERE`, `WHAT`, or `STATE` in the device UI.
  - Mapping keyboard keys to those buttons in Live Key Map mode.
- No raw MIDI note trigger path is wired, so note input for instruments is not intercepted by Clip Announcer.
- Note: Live/Max for Live still does not provide a reliable per-device global keyboard-combo API.

## Release Workflow

1. Validate source contract:
   1. `./scripts/verify_contract.sh`
2. Stage release artifact from source device:
   1. `./scripts/prepare_release.sh`
   2. This now copies temporary sidecar files into `dist/` so `dist/ClipAnnouncer.amxd` can load before freeze:
      - `dist/clip_announcer.js`
      - `dist/clip_announcer_tts.js`
   3. The script also flips the staged `node.script` embed flag (`"embed" : 1`) before freeze/save.
3. Open `dist/ClipAnnouncer.amxd` in Max from Live and embed dependencies:
   1. Use Max for Live freeze/collect workflow in your Max version.
   2. Ensure external script dependencies are embedded into the `.amxd`.
4. Save the device back to `dist/ClipAnnouncer.amxd`.
5. Run strict verification:
   1. `./scripts/verify_release.sh dist/ClipAnnouncer.amxd --strict`
   2. Strict mode validates embedded script-content signatures (not only metadata flags like `"embed"`).
6. Remove staged sidecars from `dist/` only after strict verify passes:
   1. `rm dist/clip_announcer.js dist/clip_announcer_tts.js`
7. Finalize release (strict verify + remove staged sidecars):
   1. `./scripts/finalize_release.sh dist/ClipAnnouncer.amxd`
8. Run isolation smoke test:
   1. Copy only `dist/ClipAnnouncer.amxd` to a clean temp folder with no JS files.
   2. Load it in Live.
   3. Confirm startup, announce behavior, and speech all work.

## Pass/Fail Checklist

- [ ] `verify_contract.sh` passes.
- [ ] `verify_release.sh --strict` passes.
- [ ] `dist/clip_announcer.js` and `dist/clip_announcer_tts.js` removed after strict pass.
- [ ] No startup missing-file errors.
- [ ] No `jsliveapi property cannot be listened to` warning during normal use.
- [ ] `WHERE`, `WHAT`, and `STATE` return deterministic category summaries in console.
- [ ] Speech is audible and does not overlap/spam.
- [ ] Device works when only the release `.amxd` is present.
