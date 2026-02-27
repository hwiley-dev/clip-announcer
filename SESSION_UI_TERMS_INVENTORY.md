# Clip Announcer Beta: Session UI Terms Inventory

Updated: February 27, 2026  
Source of truth: `clip_announcer.js`, `ClipAnnouncer.maxpat`, `TEST_PLAN_PHASE2.md`, `PHASE1_NOTES.md`

## Scope
This inventory covers the terms currently exposed by the beta device through:
- Spoken summary output
- Structured `STATE` console output
- Device UI trigger naming

## 1) Exact Spoken Vocabulary (Current Beta)
These are the exact fixed words/phrases emitted by the current summary template:

- `Track`
- `Slot`
- `Clip`
- `Status`
- `Unknown Track`
- `Empty`
- `(Unnamed Clip)`
- `Recording`
- `Playing`
- `Stopped`
- `?` (fallback when index is unknown)

Current spoken template:
- `Track {track_index}: {track_name}.`
- `Slot {slot_index}.`
- `Clip: {clip_name or Empty}.`
- `Status: {Stopped|Playing|Recording}.`

## 2) Complete Exposed Session Terms (Data/Fields)
These are all session-context fields currently exposed in beta (spoken and/or logged):

- `track_index`
- `track_name`
- `track_id`
- `slot_index`
- `slot_id`
- `has_clip`
- `clip_id`
- `clip_name`
- `clip_length`
- `looping`
- `loop_start`
- `loop_end`
- `status`

Related LiveAPI properties currently queried:
- `selected_track`
- `selected_scene`
- `highlighted_clip_slot`
- `name` (track/clip)
- `has_clip`
- `is_recording`
- `is_playing`
- `clip`
- `length`
- `looping`
- `loop_start`
- `loop_end`

## 3) Workflow Grouping (Live Performance)
Methodical grouping for performance workflows:

| Workflow Group | Purpose During Performance | Terms |
|---|---|---|
| 1. Orientation / Location | Confirm where focus is in Session grid | `track_index`, `track_name`, `slot_index`, `selected_track`, `selected_scene`, `highlighted_clip_slot`, `Track`, `Slot`, `Unknown Track`, `?` |
| 2. Clip Presence Check | Confirm whether slot is empty or populated | `has_clip`, `clip_id`, `clip_name`, `Clip`, `Empty`, `(Unnamed Clip)` |
| 3. Action Status Check | Confirm transport/record state before triggering decisions | `status`, `is_recording`, `is_playing`, `Status`, `Recording`, `Playing`, `Stopped` |
| 4. Timing / Loop Awareness | Confirm loop boundaries and clip duration for launch confidence | `clip_length`, `looping`, `loop_start`, `loop_end`, `length` |
| 5. Trigger + Feedback Layer | Confirm announce control and console feedback path | `WHERE`, `WHAT`, `STATE` (button labels), `where_button`, `what_button`, `state_button`, `SUMMARY`, `STATE` |

## 4) What Is Available But Not Spoken Yet
These fields are currently exposed in `STATE` but not included in spoken output:

- `track_id`
- `slot_id`
- `clip_id`
- `clip_length`
- `looping`
- `loop_start`
- `loop_end`

## 5) Proposed 3-Button Category Model (Next Iteration)
To support broader live workflows with simple controls, split announce output into three buttons:

| Button | Primary Question | Term Focus |
|---|---|---|
| `WHERE` | "Where am I in Session?" | `track_index`, `track_name`, `slot_index`, `selected_track`, `selected_scene`, `highlighted_clip_slot` |
| `WHAT` | "What is in this slot?" | `has_clip`, `clip_name`, `clip_id`, `clip_length`, `looping`, `loop_start`, `loop_end` |
| `STATE` | "What is it doing right now?" | `status`, `is_recording`, `is_playing`, `Recording`, `Playing`, `Stopped` |

Example deterministic templates:
- `WHERE`: `Track {index}: {name}. Slot {index}.`
- `WHAT`: `Clip: {name or Empty}. Length: {length}. Loop: {on/off}, {start} to {end}.`
- `STATE`: `Status: {Stopped|Playing|Recording}.`

## 6) Downloadable Artifact
CSV export of this same inventory is stored at:
- `SESSION_UI_TERMS_INVENTORY.csv`
