# Clip Announcer Phase 2 Test Plan

## Test Matrix

| ID | Scenario | Steps | Expected Console Output | Expected Result |
|---|---|---|---|---|
| T1 | Boot test | Load `dist/ClipAnnouncer.amxd` on MIDI track | `[ClipAnnouncer:TTS] ready ...` and no missing-file errors | Device initializes cleanly |
| T2 | Track + scene selection | Change selected track and scene, then press `WHERE` | `STATE` line with valid `track_name`, `track_index`, `slot_index` | Indices and names reflect selection |
| T3 | Empty slot announce | Select empty slot and press `WHAT` | `WHAT -> Clip: Empty.` | Speaks once; no crash |
| T4 | Populated slot announce | Select slot with clip and press `WHAT` | `WHAT -> Clip: <name>. Length: ... Loop: ...` and clip metadata in `STATE` | Speaks once with clip info |
| T5 | Status announce | While clip stopped/playing/recording press `STATE` | `STATE -> Status: ...` | Speaks status exactly once |
| T6 | Rapid button press | Press `WHERE` (or `WHAT`, `STATE`) repeatedly | `[ClipAnnouncer] announce skipped (debounce)` appears | No speech spam or overlap |
| T7 | Rapid navigation | Move quickly across tracks/scenes while testing `WHERE` + `WHAT` | No uncaught `[ERROR]` spam; stable `STATE` updates | No crash, remains responsive |
| T8 | Keyboard mapping | Map keys in Live Key Map mode to `WHERE/WHAT/STATE`, then trigger by keyboard | Corresponding `WHERE -> ...`, `WHAT -> ...`, `STATE -> ...` lines | Keyboard map path works without MIDI note triggers |
| T9 | MIDI instrument isolation | Play MIDI notes into instrument while Clip Announcer track is armed/monitored | No Clip Announcer trigger lines caused by note input | Device does not intercept note stream |
| T10 | Speech diagnostic | In edit mode trigger `speak_test` message to node.script | `[ClipAnnouncer:TTS] speaking: Clip announcer speech test` | Audible speech output |
| T11 | Isolation packaging | Load only copied release `.amxd` in clean folder | No missing JS/TTS dependency errors | Works without sidecar files |

## Detailed Procedure

1. Open Max Console before testing.
2. Run tests T1-T11 in order.
3. Record pass/fail and any exact error line.
4. If T11 fails, rerun freeze/collect and repeat T1 + T11.

## Acceptance Gates

- All tests pass.
- No dependency/path errors in boot.
- Deterministic category outputs remain:
  - `WHERE -> Track {index}: {track_name}. Slot {slot_index}.`
  - `WHAT -> Clip: {clip_name or Empty}.` (+ length/loop fields when clip exists)
  - `STATE -> Status: {Stopped/Playing/Recording}.`
