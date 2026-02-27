# Session View Readable UI Elements: Master List (Exhaustive)

Updated: February 27, 2026  
Live Object Model baseline: Ableton Live 12.3b9 (as stated in Cycling '74 LOM docs)

## Scope
This document is the exhaustive master list of **readable Session View UI elements** for Max for Live LiveAPI workflows.

Definition used here:
- `readable` = can be queried/observed via LiveAPI (`get` / `observe` / read-only child access).
- `Session View UI elements` = Session matrix + related track/scene/clip/mixer/selection/global controls that are visible or behaviorally active while operating in Session View.

## Primary Sources
- [Live Object Model index](https://docs.cycling74.com/apiref/lom/)
- [Song.View](https://docs.cycling74.com/apiref/lom/song_view/)
- [Song](https://docs.cycling74.com/apiref/lom/song/)
- [Scene](https://docs.cycling74.com/apiref/lom/scene/)
- [Track](https://docs.cycling74.com/apiref/lom/track/)
- [ClipSlot](https://docs.cycling74.com/apiref/lom/clipslot/)
- [Clip](https://docs.cycling74.com/apiref/lom/clip/)
- [MixerDevice](https://docs.cycling74.com/apiref/lom/mixerdevice/)
- [DeviceParameter](https://docs.cycling74.com/apiref/lom/deviceparameter/)

## 1) Session Selection Layer
Object: `Song.View`  
Canonical path: `live_set view`

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

## 2) Session Global Layer
Object: `Song`  
Canonical path: `live_set`

Readable child collections/objects:
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

## 3) Scene Row Layer
Object: `Scene`  
Canonical path: `live_set scenes N`

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

## 4) Track Column Layer
Object: `Track`  
Canonical path: `live_set tracks N`

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

### Track UI Subview
Object: `Track.View`  
Canonical path: `live_set tracks N view`

Readable children:
- `selected_device`

Readable properties:
- `selected_device`
- `is_collapsed`
- `is_showing_chains`
- `selected_track`
- `visible_tracks`

## 5) Clip Slot Cell Layer
Object: `ClipSlot`  
Canonical path: `live_set tracks N clip_slots M`

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

## 6) Session Clip Layer
Object: `Clip`  
Canonical path: `live_set tracks N clip_slots M clip`

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

### Clip UI Subview
Object: `Clip.View`  
Canonical path: `live_set tracks N clip_slots M clip view`

Readable properties:
- `grid_is_triplet`
- `grid_quantization`
- `grid_snap`
- `hide_envelope`
- `show_envelope`
- `show_loop`
- `show_warp_as`
- `show_warp`

## 7) Mixer Strip Layer
Object: `MixerDevice`  
Canonical path: `live_set tracks N mixer_device`

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

### DeviceParameter Read Model (for mixer/parameter values)
Object: `DeviceParameter`  
Canonical path example: `live_set tracks N mixer_device volume` (and similar parameter paths)

Readable properties:
- `automation_state`
- `default_value`
- `is_enabled`
- `is_quantized`
- `max`
- `min`
- `name`
- `original_name`
- `state`
- `value`
- `display_value`
- `value_items`

## Practical Note For Clip Announcer
This master list is exhaustive for readable Session View surfaces via LiveAPI.  
Your current beta implementation only uses a subset of these fields.
