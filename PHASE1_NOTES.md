# Clip Announcer Phase 1

## 1. Patch Structure Description

The device patch (`ClipAnnouncer.maxpat`) uses this signal chain:

1. `live.button` (`ANNOUNCE`) emits `1` on press.
2. `sel 1` filters press events and sends `announce`.
3. `js clip_announcer.js`:
   - Reads Live selection via LiveAPI.
   - Builds deterministic clip summary text.
   - Logs structured state to Max Console.
   - Outputs `speak <summary>` to outlet 0.
4. `node.script clip_announcer_tts.js @autostart 1`:
   - Receives `speak` messages.
   - Runs macOS `say` for TTS.
   - Enforces additional speech debounce / overlap protection.

`loadbang` sends `refresh` and `debug` on patch load for immediate state visibility.

## 2. LiveAPI Path Logic Used

Core objects and paths:

- `live_set view` observer:
  - Observed properties:
    - `selected_track`
    - `highlighted_clip_slot`
    - `selected_scene` (fallback context)
- Track lookup:
  - Selected track id from `live_set view -> selected_track`
  - Track name from `id <track_id> -> name`
  - Track index from scan of `live_set tracks <i>` matching id
- Slot lookup:
  - Selected slot id from `live_set view -> highlighted_clip_slot`
  - Slot index parsed from slot path `... clip_slots <i>`
  - Fallback scan of `live_set tracks <track_index> clip_slots <i>` matching id
- Clip lookup (only when `has_clip == 1`):
  - Clip id from `id <slot_id> -> clip`
  - Clip data from `id <clip_id>`:
    - `name`
    - `length`
    - `looping`
    - `loop_start`
    - `loop_end`
- Status lookup from slot:
  - `is_recording` -> `Recording`
  - else `is_playing` -> `Playing`
  - else `Stopped`

## 3. Object Safety Handling Explanation

Safety controls implemented in `clip_announcer.js`:

- Every LiveAPI call is wrapped in safe helpers (`safeGet`, `safeApiFromId`, typed parsers).
- All ids are validated (`id > 0`) before object creation / querying.
- Empty slot path is handled explicitly via `has_clip` guard.
- Selection-change observer callback is throttled by a short delayed task (`25 ms`) to reduce burst/race effects during rapid navigation.
- ANNOUNCE action has an explicit `300 ms` debounce gate.
- Exceptions are caught and logged as `[ClipAnnouncer][ERROR]` without throwing hard failures.

## 4. macOS Speech Implementation Notes

Speech is implemented in `clip_announcer_tts.js` (Node for Max):

- Receives `speak` command from Max patch.
- Sanitizes text (whitespace cleanup + max length).
- Uses `child_process.spawn("say", [text])` (shell command path on macOS).
- Enforces:
  - `300 ms` debounce for repeated requests.
  - Single active speech process at a time (prevents overlapping speech spam).
- Optional `stop` handler terminates active speech with `SIGTERM`.

## 5. Phase 2 Recommendations

1. Add optional **Auto Announce** mode bound to selection changes (disabled by default).
2. Add clip color / scene name in summary for richer accessibility context.
3. Add voice/rate preferences (`say -v`, `say -r`) as user parameters.
4. Add transport-state-aware phrasing (triggered/queued states if needed).
5. Add a small test harness patch that replays synthetic message patterns into JS/Node logic.
