# Clip Announcer Phase 2 Test Plan

## Test Matrix

| ID | Scenario | Steps | Expected Console Output | Expected Result |
|---|---|---|---|---|
| T1 | Boot test | Load `dist/ClipAnnouncer.amxd` on MIDI track | `[ClipAnnouncer:TTS] ready ...` and no missing-file errors | Device initializes cleanly |
| T2 | Track + scene selection | Change selected track and scene, then press ANNOUNCE | `STATE` line with valid `track_name`, `track_index`, `slot_index` | Indices and names reflect selection |
| T3 | Empty slot announce | Select empty slot and press ANNOUNCE | `SUMMARY ... Clip: Empty. Status: ...` | Speaks once; no crash |
| T4 | Populated slot announce | Select slot with clip and press ANNOUNCE | `SUMMARY ... Clip: <name>. Status: ...` and clip metadata in `STATE` | Speaks once with clip info |
| T5 | Rapid button press | Press ANNOUNCE repeatedly | `[ClipAnnouncer] announce skipped (debounce)` appears | No speech spam or overlap |
| T6 | Rapid navigation | Move quickly across tracks/scenes while testing ANNOUNCE | No uncaught `[ERROR]` spam; stable `STATE` updates | No crash, remains responsive |
| T7 | Speech diagnostic | In edit mode trigger `speak_test` message to node.script | `[ClipAnnouncer:TTS] speaking: Clip announcer speech test` | Audible speech output |
| T8 | Isolation packaging | Load only copied release `.amxd` in clean folder | No missing JS/TTS dependency errors | Works without sidecar files |
| T9 | MIDI trigger (no mapping) | Play MIDI note number `60` into the track with device loaded | `ANNOUNCE -> ...` and standard `SUMMARY ...` line | Announces once without using Live key/midi map mode |

## Detailed Procedure

1. Open Max Console before testing.
2. Run tests T1-T9 in order.
3. Record pass/fail and any exact error line.
4. If T8 fails, rerun freeze/collect and repeat T1 + T8.

## Acceptance Gates

- All tests pass.
- No dependency/path errors in boot.
- Deterministic summary format remains:
  - `Track {index}: {track_name}.`
  - `Slot {slot_index}.`
  - `Clip: {clip_name or Empty}.`
  - `Status: {Stopped/Playing/Recording}.`
