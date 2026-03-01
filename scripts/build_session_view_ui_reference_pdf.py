#!/usr/bin/env python3
from __future__ import annotations

from collections import Counter, defaultdict
from pathlib import Path

from build_accessibility_workflow_report import (
    ACCENT,
    ACCENT_DARK,
    CONTENT_WIDTH,
    INK,
    LEFT_MARGIN,
    MUTED,
    PAGE_WIDTH,
    PDFWriter,
    SOFT_FILL,
    WHITE,
    LayoutDocument,
    add_text,
    add_text_lines,
    color_fill,
    generated_on_label,
    load_csv,
    rect_cmd,
)


LAYER_TITLES = {
    "selection": "Selection Layer",
    "session_global": "Session Global Layer",
    "scene": "Scene Row Layer",
    "track": "Track Column Layer",
    "track_view": "Track UI Subview",
    "clip_slot": "Clip Slot Cell Layer",
    "clip": "Session Clip Layer",
    "clip_view": "Clip UI Subview",
    "mixer": "Mixer Strip Layer",
    "parameter": "Parameter Read Layer",
}

OBJECT_NOTES = {
    "Song.View": "Best first stop for current focus, highlighted slot, and selected track/scene context.",
    "Song": "Global transport, tempo, recording, quantization, scale, and session-wide policy context.",
    "Scene": "Scene naming, trigger state, and scene-scoped tempo or signature metadata.",
    "Track": "Column identity, arm/mute/solo state, routing, meters, and current launch state.",
    "Track.View": "Narrow UI subview. Useful for selected device and collapsed/insert-mode state.",
    "ClipSlot": "Most important Session cell object for launch, trigger, record, and occupancy state.",
    "Clip": "Detailed clip identity, timing, looping, clip type, and playback/recording metadata.",
    "Clip.View": "Grid-display state for the clip editor view.",
    "MixerDevice": "Mixer strip access point for volume, pan, sends, activator, and crossfader children.",
    "DeviceParameter": "Readable leaf for numeric/display values on mixer and device controls.",
}

OBJECT_ORDER = [
    "Song.View",
    "Song",
    "Scene",
    "Track",
    "Track.View",
    "ClipSlot",
    "Clip",
    "Clip.View",
    "MixerDevice",
    "DeviceParameter",
]


def title_page(document: LayoutDocument, total_entries: int) -> None:
    page = document.page
    page.add(f"{color_fill(WHITE)}{rect_cmd(0, 0, PAGE_WIDTH, 792)}")
    page.add(f"{color_fill(SOFT_FILL)}{rect_cmd(0, 0, PAGE_WIDTH, 210)}")
    page.add(f"{color_fill(ACCENT)}{rect_cmd(LEFT_MARGIN, 86, 8, 94)}")
    add_text_lines(
        page,
        LEFT_MARGIN + 22,
        92,
        [
            "Session View UI Terms",
            "Developer Reference",
        ],
        font="F2",
        size=22,
        leading=26,
        color=INK,
    )
    add_text(
        page,
        LEFT_MARGIN + 22,
        148,
        "Readable LiveAPI surfaces for Max for Live accessibility and tooling work",
        font="F1",
        size=12,
        color=MUTED,
    )
    add_text(
        page,
        LEFT_MARGIN + 22,
        170,
        generated_on_label(),
        font="F1",
        size=10.5,
        color=ACCENT_DARK,
    )
    document.cursor_y = 236
    document.paragraph(
        "This reference is intended for developers who need a fast, reliable map of what Ableton Live "
        "Session View exposes through the Live Object Model. It is structured for quick orientation first, "
        "then deep reference, so it works both as a briefing document and as a build-time lookup sheet."
    )
    document.callout(
        "What is verified here",
        (
            f"The companion master CSV contains {total_entries} verified readable entries across selection, "
            "global session state, scenes, tracks, clip slots, clips, clip view, mixer surfaces, and "
            "device parameters. This PDF is the developer-friendly presentation layer for that inventory."
        ),
    )


def coverage_rows(rows: list[dict[str, str]]) -> list[list[str]]:
    counts = Counter(row["layer"] for row in rows)
    ordered_layers = [
        "selection",
        "session_global",
        "scene",
        "track",
        "track_view",
        "clip_slot",
        "clip",
        "clip_view",
        "mixer",
        "parameter",
    ]
    rows_out = []
    for layer in ordered_layers:
        rows_out.append([LAYER_TITLES[layer], str(counts[layer])])
    rows_out.append(["Total verified readable entries", str(sum(counts.values()))])
    return rows_out


def entry_point_rows() -> list[list[str]]:
    return [
        [
            "`live_set view`",
            "Current Session focus",
            "selected_track, selected_scene, highlighted_clip_slot, detail_clip",
        ],
        [
            "`live_set tracks N clip_slots M`",
            "Selected grid cell state",
            "has_clip, is_playing, is_recording, is_triggered, playing_status, clip",
        ],
        [
            "`live_set tracks N clip_slots M clip`",
            "Detailed clip metadata",
            "name, length, looping, loop_start, loop_end, playing_position, is_audio_clip, is_midi_clip",
        ],
        [
            "`live_set tracks N`",
            "Track identity and status",
            "name, arm, mute, solo, fired_slot_index, playing_slot_index, input_meter_level, output_meter_level",
        ],
        [
            "`live_set scenes N`",
            "Scene row state",
            "name, is_triggered, tempo, tempo_enabled, time_signature_numerator, time_signature_denominator",
        ],
    ]


def object_summary_rows(rows: list[dict[str, str]]) -> list[list[str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["object"]].append(row)

    summary = []
    for object_name in OBJECT_ORDER:
        object_rows = grouped[object_name]
        if not object_rows:
            continue
        summary.append(
            [
                object_name,
                object_rows[0]["canonical_path"],
                str(len(object_rows)),
                OBJECT_NOTES[object_name],
            ]
        )
    return summary


def readable_lists(rows: list[dict[str, str]]) -> tuple[str, str]:
    children = [row["member_name"] for row in rows if row["member_type"] == "child"]
    properties = [row["member_name"] for row in rows if row["member_type"] == "property"]
    child_text = ", ".join(children) if children else "None"
    property_text = ", ".join(properties) if properties else "None"
    return child_text, property_text


def object_sections(document: LayoutDocument, rows: list[dict[str, str]]) -> None:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in rows:
        grouped[row["object"]].append(row)

    for object_name in OBJECT_ORDER:
        object_rows = grouped[object_name]
        if not object_rows:
            continue

        child_text, property_text = readable_lists(object_rows)
        document.section_title(object_name)
        document.bullets(
            [
                f"Layer: {LAYER_TITLES[object_rows[0]['layer']]}",
                f"Canonical path: {object_rows[0]['canonical_path']}",
                f"Readable entry count: {len(object_rows)}",
                OBJECT_NOTES[object_name],
            ],
            bullet_indent=16,
        )
        document.subhead("Readable children")
        document.paragraph(child_text, size=9.5, leading=12.5)
        document.subhead("Readable properties")
        document.paragraph(property_text, size=9.5, leading=12.5)


def source_rows() -> list[list[str]]:
    return [
        ["LOM index", "https://docs.cycling74.com/apiref/lom/"],
        ["Song.View", "https://docs.cycling74.com/apiref/lom/song_view/"],
        ["Song", "https://docs.cycling74.com/apiref/lom/song/"],
        ["Scene", "https://docs.cycling74.com/apiref/lom/scene/"],
        ["Track", "https://docs.cycling74.com/apiref/lom/track/"],
        ["Track.View", "https://docs.cycling74.com/apiref/lom/track_view/"],
        ["ClipSlot", "https://docs.cycling74.com/apiref/lom/clipslot/"],
        ["Clip", "https://docs.cycling74.com/apiref/lom/clip/"],
        ["Clip.View", "https://docs.cycling74.com/apiref/lom/clip_view/"],
        ["MixerDevice", "https://docs.cycling74.com/apiref/lom/mixerdevice/"],
        ["DeviceParameter", "https://docs.cycling74.com/apiref/lom/deviceparameter/"],
    ]


def build_pdf(master_csv: Path, output_pdf: Path) -> int:
    rows = load_csv(master_csv)
    document = LayoutDocument(
        "Session View UI Terms",
        "Community developer reference",
    )
    title_page(document, len(rows))

    document.section_title("Quick Orientation")
    document.paragraph(
        "If you are building a screen-reader bridge, announcer, or diagnostic tool, start at "
        "`live_set view` for focus, then descend into `Track`, `ClipSlot`, and `Clip` only as needed. "
        "That keeps speech stable and avoids needlessly expensive traversal."
    )
    document.table(
        ["Start path", "Why it matters", "High-value readable members"],
        entry_point_rows(),
        [150.0, 130.0, CONTENT_WIDTH - 150.0 - 130.0],
        body_size=8.6,
        body_leading=11.0,
        header_size=8.9,
    )

    document.section_title("Coverage Summary")
    document.paragraph(
        "The reference inventory separates Session View into layers so other developers can reason about "
        "what belongs to focus, what belongs to clip-state, and what belongs to global transport or mixer state."
    )
    document.table(
        ["Layer", "Verified entries"],
        coverage_rows(rows),
        [220.0, CONTENT_WIDTH - 220.0],
        body_size=9.1,
        body_leading=11.6,
        header_size=9.0,
    )

    document.section_title("Exhaustive Object Map")
    document.paragraph(
        "This table is the fastest complete map from object to canonical path and practical development role."
    )
    document.table(
        ["Object", "Canonical path", "Entries", "Developer use"],
        object_summary_rows(rows),
        [86.0, 172.0, 44.0, CONTENT_WIDTH - 86.0 - 172.0 - 44.0],
        body_size=8.1,
        body_leading=10.2,
        header_size=8.5,
    )

    object_sections(document, rows)

    document.section_title("Recommended Minimum Read Set")
    document.bullets(
        [
            "Focus: selected_track, selected_scene, highlighted_clip_slot.",
            "Slot state: has_clip, is_playing, is_recording, is_triggered.",
            "Clip identity and timing: name, length, looping, loop_start, loop_end.",
            "Track status: arm, mute, solo, playing_slot_index.",
            "Global state: is_playing, tempo, session_record.",
        ],
        bullet_indent=16,
    )

    document.section_title("Primary Sources")
    document.table(
        ["Source", "URL"],
        source_rows(),
        [112.0, CONTENT_WIDTH - 112.0],
        body_font="F3",
        body_size=7.8,
        body_leading=9.6,
        header_size=8.6,
    )

    document.add_header_footer()
    writer = PDFWriter(document.pages)
    writer.write(output_pdf)
    return len(document.pages)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    master_csv = repo_root / "SESSION_VIEW_READABLE_UI_MASTER_LIST.csv"
    output_pdf = repo_root / "community-reference" / "SESSION_VIEW_UI_DEVELOPER_REFERENCE.pdf"

    page_count = build_pdf(master_csv, output_pdf)
    print(f"[OK] wrote {output_pdf}")
    print(f"[OK] pages: {page_count}")


if __name__ == "__main__":
    main()
