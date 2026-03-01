# Session View UI Terms Developer Reference

Updated: February 27, 2026  
Audience: Max for Live developers, accessibility-tool builders, LiveAPI researchers  
Verification basis: official Cycling '74 Live Object Model docs

## Purpose
This document is a developer-facing reference for the **readable Session View UI surfaces** available through LiveAPI.

It is designed to answer three questions quickly:
- What parts of Session View can a Max for Live device read?
- Which object paths matter most for accessibility and announcement tools?
- What is the exhaustive set of readable children and properties on those Session-facing objects?

## What "UI Terms" Means Here
This document covers **readable object names, children, and properties** that correspond to Session View UI state.

It does not treat write-only functions, setters, or non-Session domains as readable UI terms.

## Coverage Summary
Verified readable entries in the companion master CSV:

| Layer | Entries |
|---|---:|
| `selection` | 8 |
| `session_global` | 57 |
| `scene` | 11 |
| `track` | 47 |
| `track_view` | 3 |
| `clip_slot` | 12 |
| `clip` | 49 |
| `clip_view` | 2 |
| `mixer` | 11 |
| `parameter` | 12 |
| `total` | 212 |

## Fastest Entry Points
These are the highest-value objects for most Session View accessibility tools:

### 1. `live_set view`
Use this first when you need the current UI focus.

Most important readable members:
- `selected_track`
- `selected_scene`
- `highlighted_clip_slot`
- `detail_clip`

### 2. `live_set tracks N clip_slots M`
Use this to understand the selected Session cell.

Most important readable members:
- `has_clip`
- `is_playing`
- `is_recording`
- `is_triggered`
- `playing_status`
- `clip`

### 3. `live_set tracks N clip_slots M clip`
Use this when the slot contains a clip and you need detailed clip metadata.

Most important readable members:
- `name`
- `length`
- `looping`
- `loop_start`
- `loop_end`
- `playing_position`
- `is_audio_clip`
- `is_midi_clip`
- `color`

### 4. `live_set tracks N`
Use this for track identity, metering, arm/mute/solo state, and launch status.

Most important readable members:
- `name`
- `color`
- `arm`
- `mute`
- `solo`
- `playing_slot_index`
- `fired_slot_index`
- `input_meter_level`
- `output_meter_level`

### 5. `live_set scenes N`
Use this for scene naming and scene-level launch metadata.

Most important readable members:
- `name`
- `color`
- `is_triggered`
- `tempo`
- `tempo_enabled`
- `time_signature_numerator`
- `time_signature_denominator`

## Exhaustive Readable Object Map

### A. Selection Layer
Object: `Song.View`  
Path: `live_set view`

Readable children:
- `detail_clip`
- `highlighted_clip_slot`
- `selected_chain`
- `selected_parameter`
- `selected_scene`
- `selected_track`

Readable properties:
- `draw_mode`
- `follow_song`

Developer note:
- For Session accessibility tools, `selected_track`, `selected_scene`, and `highlighted_clip_slot` are the core focus signals.

### B. Session Global Layer
Object: `Song`  
Path: `live_set`

Readable children:
- `cue_points`
- `return_tracks`
- `scenes`
- `tracks`
- `visible_tracks`
- `master_track`
- `view`
- `groove_pool`
- `tuning_system`

Readable properties:
- `appointed_device`
- `arrangement_overdub`
- `back_to_arranger`
- `can_capture_midi`
- `can_jump_to_next_cue`
- `can_jump_to_prev_cue`
- `can_redo`
- `can_undo`
- `clip_trigger_quantization`
- `count_in_duration`
- `current_song_time`
- `exclusive_arm`
- `exclusive_solo`
- `file_path`
- `groove_amount`
- `is_ableton_link_enabled`
- `is_ableton_link_start_stop_sync_enabled`
- `is_counting_in`
- `is_playing`
- `last_event_time`
- `loop`
- `loop_length`
- `loop_start`
- `metronome`
- `midi_recording_quantization`
- `name`
- `nudge_down`
- `nudge_up`
- `tempo_follower_enabled`
- `overdub`
- `punch_in`
- `punch_out`
- `re_enable_automation_enabled`
- `record_mode`
- `root_note`
- `scale_intervals`
- `scale_mode`
- `scale_name`
- `select_on_launch`
- `session_automation_record`
- `session_record`
- `session_record_status`
- `signature_denominator`
- `signature_numerator`
- `song_length`
- `start_time`
- `swing_amount`
- `tempo`

Developer note:
- This layer holds transport, tempo, recording, scale, and global launch context that can enrich Session announcements.

### C. Scene Row Layer
Object: `Scene`  
Path: `live_set scenes N`

Readable children:
- `clip_slots`

Readable properties:
- `color`
- `color_index`
- `is_empty`
- `is_triggered`
- `name`
- `tempo`
- `tempo_enabled`
- `time_signature_numerator`
- `time_signature_denominator`
- `time_signature_enabled`

Developer note:
- Scene objects matter when you want row-level naming, tempo-scene workflows, or scene launch feedback.

### D. Track Column Layer
Object: `Track`  
Path: `live_set tracks N`

Readable children:
- `take_lanes`
- `clip_slots`
- `arrangement_clips`
- `devices`
- `group_track`
- `mixer_device`
- `view`

Readable properties:
- `arm`
- `available_input_routing_channels`
- `available_input_routing_types`
- `available_output_routing_channels`
- `available_output_routing_types`
- `back_to_arranger`
- `can_be_armed`
- `can_be_frozen`
- `can_show_chains`
- `color`
- `color_index`
- `fired_slot_index`
- `fold_state`
- `has_audio_input`
- `has_audio_output`
- `has_midi_input`
- `has_midi_output`
- `implicit_arm`
- `input_meter_left`
- `input_meter_level`
- `input_meter_right`
- `input_routing_channel`
- `input_routing_type`
- `is_foldable`
- `is_frozen`
- `is_grouped`
- `is_part_of_selection`
- `is_showing_chains`
- `is_visible`
- `mute`
- `muted_via_solo`
- `name`
- `output_meter_left`
- `output_meter_level`
- `output_meter_right`
- `performance_impact`
- `output_routing_channel`
- `output_routing_type`
- `playing_slot_index`
- `solo`

Developer note:
- Track is the main identity and status object for column-oriented Session navigation.

### E. Track UI Subview
Object: `Track.View`  
Path: `live_set tracks N view`

Readable children:
- `selected_device`

Readable properties:
- `device_insert_mode`
- `is_collapsed`

Developer note:
- `Track.View` is narrower than many developers expect. It is useful, but not a broad mirror of the visible track strip.

### F. Clip Slot Cell Layer
Object: `ClipSlot`  
Path: `live_set tracks N clip_slots M`

Readable children:
- `clip`

Readable properties:
- `color`
- `color_index`
- `controls_other_clips`
- `has_clip`
- `has_stop_button`
- `is_group_slot`
- `is_playing`
- `is_recording`
- `is_triggered`
- `playing_status`
- `will_record_on_start`

Developer note:
- This is the single most important cell-state object for Session grid readout.

### G. Session Clip Layer
Object: `Clip`  
Path: `live_set tracks N clip_slots M clip`

Readable children:
- `view`

Readable properties:
- `available_warp_modes`
- `color`
- `color_index`
- `end_marker`
- `end_time`
- `gain`
- `gain_display_string`
- `file_path`
- `groove`
- `has_envelopes`
- `has_groove`
- `is_session_clip`
- `is_arrangement_clip`
- `is_take_lane_clip`
- `is_audio_clip`
- `is_midi_clip`
- `is_overdubbing`
- `is_playing`
- `is_recording`
- `is_triggered`
- `launch_mode`
- `launch_quantization`
- `legato`
- `length`
- `loop_end`
- `loop_jump`
- `loop_start`
- `looping`
- `muted`
- `name`
- `notes`
- `warp_markers`
- `pitch_coarse`
- `pitch_fine`
- `playing_position`
- `playing_status`
- `position`
- `ram_mode`
- `sample_length`
- `sample_rate`
- `signature_denominator`
- `signature_numerator`
- `start_marker`
- `start_time`
- `velocity_amount`
- `warp_mode`
- `warping`
- `will_record_on_start`

Developer note:
- Use `Clip` only after `ClipSlot.has_clip == 1`, otherwise many clip-specific reads are not relevant.

### H. Clip UI Subview
Object: `Clip.View`  
Path: `live_set tracks N clip_slots M clip view`

Readable properties:
- `grid_is_triplet`
- `grid_quantization`

Developer note:
- `Clip.View` contributes grid-display context, not broad playback state.

### I. Mixer Strip Layer
Object: `MixerDevice`  
Path: `live_set tracks N mixer_device`

Readable children:
- `sends`
- `cue_volume`
- `crossfader`
- `left_split_stereo`
- `panning`
- `right_split_stereo`
- `song_tempo`
- `track_activator`
- `volume`

Readable properties:
- `crossfade_assign`
- `panning_mode`

Developer note:
- Mixer state is essential when your tool needs to report whether something is effectively audible or muted.

### J. Parameter Read Layer
Object: `DeviceParameter`  
Example path: `live_set tracks N mixer_device volume`

Readable properties:
- `automation_state`
- `default_value`
- `display_value`
- `is_enabled`
- `is_quantized`
- `max`
- `min`
- `name`
- `original_name`
- `state`
- `value`
- `value_items`

Developer note:
- Treat `DeviceParameter` as the readable leaf layer for volume, pan, sends, activators, and similar controls.

## Recommended Minimum Read Set For Accessibility Devices
If you are building a first-pass Session announcer, start here:

### Focus / location
- `live_set view -> selected_track`
- `live_set view -> selected_scene`
- `live_set view -> highlighted_clip_slot`
- `track -> name`

### Slot state
- `clip_slot -> has_clip`
- `clip_slot -> is_playing`
- `clip_slot -> is_recording`
- `clip_slot -> is_triggered`

### Clip identity and timing
- `clip -> name`
- `clip -> length`
- `clip -> looping`
- `clip -> loop_start`
- `clip -> loop_end`

### Track state
- `track -> arm`
- `track -> mute`
- `track -> solo`
- `track -> playing_slot_index`

### Global state
- `live_set -> is_playing`
- `live_set -> tempo`
- `live_set -> session_record`

## Companion Files
- Raw exhaustive list: [SESSION_VIEW_READABLE_UI_MASTER_LIST.md](/Users/hunterwiley/Code-Projects/Clip-Announcer/SESSION_VIEW_READABLE_UI_MASTER_LIST.md)
- Machine-readable list: [SESSION_VIEW_READABLE_UI_MASTER_LIST.csv](/Users/hunterwiley/Code-Projects/Clip-Announcer/SESSION_VIEW_READABLE_UI_MASTER_LIST.csv)

## Sources
- [Cycling '74 Live Object Model Index](https://docs.cycling74.com/apiref/lom/)
- [Song.View](https://docs.cycling74.com/apiref/lom/song_view/)
- [Song](https://docs.cycling74.com/apiref/lom/song/)
- [Scene](https://docs.cycling74.com/apiref/lom/scene/)
- [Track](https://docs.cycling74.com/apiref/lom/track/)
- [Track.View](https://docs.cycling74.com/apiref/lom/track_view/)
- [ClipSlot](https://docs.cycling74.com/apiref/lom/clipslot/)
- [Clip](https://docs.cycling74.com/apiref/lom/clip/)
- [Clip.View](https://docs.cycling74.com/apiref/lom/clip_view/)
- [MixerDevice](https://docs.cycling74.com/apiref/lom/mixerdevice/)
- [DeviceParameter](https://docs.cycling74.com/apiref/lom/deviceparameter/)
