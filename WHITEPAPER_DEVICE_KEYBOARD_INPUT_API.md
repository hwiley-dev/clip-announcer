# Whitepaper Draft

## Deterministic Device Keyboard Input for Ableton Live and Max for Live

**Version:** Draft 0.1  
**Date:** February 21, 2026  
**Author:** Clip Announcer project context (working draft)

## Executive Summary

Ableton Live currently offers excellent global keyboard shortcuts, key mapping, MIDI mapping, and computer-MIDI-keyboard workflows. However, there is no deterministic, accessibility-focused keyboard input path that a specific Max for Live (M4L) device can reliably own and process across normal production conditions. Existing approaches are either focus-dependent, conflict-prone, or platform-variable.

This paper proposes an opt-in **Device Keyboard Input API** for Live/M4L that introduces explicit permissions, conflict resolution, and accessibility-first behavior. The goal is to enable reliable, low-friction single-keystroke control for device workflows while preserving safety, shortcut integrity, and cross-platform predictability.

## Problem Statement

Users building assistive workflows in Live need deterministic trigger paths. Today, those users face inconsistent keyboard behavior because:

1. Input delivery is focus-dependent in Max patch contexts.
2. Live-level shortcut and mapping systems may consume key events before device logic receives them.
3. Character-based key matching is layout/IME/dead-key sensitive.
4. There is no formal per-device keyboard ownership or arbitration model.

The practical outcome is that many accessibility and automation designs must fall back to MIDI-note triggers for reliability, even when keyboard input would be the natural interface.

## Scope

This proposal is about **computer keyboard event routing to device logic** in Live and M4L.

In scope:

1. Per-device key subscriptions.
2. Permission and safety model.
3. Conflict management with existing shortcuts and mappings.
4. Accessibility requirements for remapping and predictability.
5. macOS and Windows behavior requirements.

Out of scope:

1. Replacing Live global shortcuts.
2. Building a full OS-wide global hotkey system.
3. Changing MIDI mapping fundamentals.
4. Re-architecting all Max input objects.

## Current-State Constraints (Observed)

### 1) Event Ownership Is Layered

Keyboard events can be processed by OS input systems, Live shortcut handling, active UI focus, and only then device-level logic (if delivered). This layered ownership makes delivery nondeterministic from a device author perspective.

### 2) Focus Dependency

Max key events are typically bound to active/focused patcher contexts. Device authors cannot assume event receipt when focus is elsewhere in Live.

### 3) Character vs Physical-Key Ambiguity

Character-level matching (for example, backtick `` ` ``) is sensitive to layout and dead-key rules. Physical-key matching is more stable, but currently lacks a dedicated, portable M4L routing contract.

### 4) No Device-Level Reservation Primitive

There is no first-class mechanism for a device to request specific keys with clear policy:

1. Which keys may be reserved.
2. How collisions are detected and resolved.
3. Whether event capture is foreground-only or set-wide.

## Accessibility Impact

This gap disproportionately affects users who rely on:

1. One-action keyboard macros.
2. Reduced-motion or reduced-precision controller interactions.
3. Screen-reader-guided or low-vision workflows where keyboard predictability is critical.
4. Consistent command muscle memory across sessions and sets.

Without deterministic delivery, accessibility workflows become brittle and require workaround complexity.

## Proposed Solution: Device Keyboard Input API

Introduce an opt-in API exposed through Live/M4L with explicit subscription and lifecycle semantics.

### Design Principles

1. **Deterministic:** Device knows whether it owns a binding.
2. **Safe:** Protected shortcuts remain protected.
3. **Transparent:** Users can inspect and manage all bindings in one place.
4. **Accessible:** Remappable, stateful, low-latency, and feedback-oriented.
5. **Portable:** Same behavior contract on macOS and Windows.

### Conceptual API Surface

Example pseudocode (illustrative only):

```js
// request keyboard access for this device instance
const kb = liveDevice.keyboard.requestAccess({
  scope: "foreground_device", // or "set_session" with stricter prompts
  purpose: "Accessible trigger for clip announcement"
});

// subscribe by physical key code (recommended) plus optional modifiers
const sub = kb.bind({
  keyCode: "Backquote",        // physical key identity
  modifiers: ["Shift"],        // optional
  mode: "press",               // press | release | repeat
  repeatPolicy: "ignore"
});

sub.on("event", (evt) => {
  // evt includes delivery guarantees + source metadata
  if (evt.delivered && evt.state === "press") {
    triggerAnnounce();
  }
});

// clear on device unload
sub.dispose();
kb.releaseAccess();
```

### API Requirements

1. Provide **physical key identifiers** (layout-agnostic) and optional character output when available.
2. Provide explicit **delivery status** (`delivered`, `blocked_reserved_shortcut`, `blocked_conflict`, `blocked_focus_policy`).
3. Support **foreground-only default** scope, with optional expanded scope behind stronger consent.
4. Offer **discoverable binding UI** at Live level (not hidden in patch internals).
5. Provide stable callback timing and bounded latency.

## Conflict and Arbitration Model

### Reserved-Key Policy

Live-defined critical shortcuts remain unbindable for devices by default.

### Collision Handling

When two devices request the same key, Live should:

1. Prompt the user with clear options.
2. Allow explicit priority assignment.
3. Offer fallback recommendations.
4. Persist decisions per set with visible indicators.

### Explicit Resolution States

Every binding should show one of:

1. Active.
2. Blocked by reserved shortcut.
3. Blocked by conflict.
4. Disabled by policy.
5. Suspended (device offline/inactive).

## Security and Privacy Guardrails

1. No silent background keylogging behavior.
2. No unrestricted text-stream capture by default.
3. Permission prompts must explain scope and purpose.
4. API should expose only subscribed keys, not all keystrokes.
5. Session indicator should show active keyboard-capturing devices.

## Accessibility Requirements (Normative)

1. Bindings must be remappable without patch editing.
2. All binding states must be screen-reader accessible in Live UI.
3. Users must get immediate success/failure feedback on key press.
4. Fallback path to MIDI trigger must be one click away.
5. Profiles should be exportable/importable for portability.

## Implementation Plan

### Phase 1: Minimal Viable API

1. Foreground-device scope only.
2. Physical key + modifier binding.
3. Reserved-key blocking.
4. Live-level Binding Manager panel.
5. Basic event telemetry.

### Phase 2: Accessibility Expansion

1. Improved spoken/visual feedback hooks.
2. Conflict wizard and guided remediation.
3. Profile presets for common assistive setups.
4. Per-set validation warnings before performance mode.

### Phase 3: Advanced Policy

1. Optional expanded scope under strict user consent.
2. Team/shared-set policy controls.
3. Deeper controller and automation interoperability.

## Validation and Test Matrix

The API should ship with an explicit matrix:

1. OS: current macOS and Windows versions.
2. Keyboard layouts: US, ISO variants, selected non-Latin layouts.
3. Input methods: dead keys, IME modes, accessibility keyboard tools.
4. Live contexts: session view, arrangement view, text-entry focus, mapping modes.
5. Device contexts: single instance, multiple instance conflicts, unloaded/reloaded sets.
6. Latency and dropped-event benchmarks under CPU load.

## Success Metrics

1. Reduction in failed trigger rate versus current M4L key workflows.
2. Reduced setup steps for accessible keyboard control.
3. Reduced support incidents involving key conflicts and focus surprises.
4. User-reported confidence in repeatable keyboard-trigger behavior.

## Risks and Mitigations

1. **Risk:** Shortcut regressions.  
   **Mitigation:** Reserved-key catalog + automated regression tests.
2. **Risk:** User confusion with multi-device conflicts.  
   **Mitigation:** Central Binding Manager and explicit state labels.
3. **Risk:** Security concerns around key capture.  
   **Mitigation:** Scope-limited permissions and transparent indicators.
4. **Risk:** Cross-platform divergence.  
   **Mitigation:** Normalize around physical key IDs and defined fallback behavior.

## Immediate Recommendation

Adopt a product requirement for deterministic device keyboard input with accessibility-first defaults. Implement a Phase 1 API and Binding Manager prototype, then validate with users building assistive M4L workflows before wider rollout.

## Appendix A: Example UI Copy (Draft)

Permission prompt:

> "Allow this device to receive `Shift + Backquote` while it is active in the foreground? Live shortcuts remain protected."

Conflict prompt:

> "`Shift + Backquote` is already assigned to another device in this set. Choose which device should receive it."

Binding state tooltip:

> "Blocked: key is reserved by Live shortcut policy."
