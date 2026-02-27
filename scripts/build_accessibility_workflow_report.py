#!/usr/bin/env python3
from __future__ import annotations

import csv
from collections import Counter, defaultdict
from dataclasses import dataclass
from datetime import date
from pathlib import Path
from typing import Iterable


PAGE_WIDTH = 612.0
PAGE_HEIGHT = 792.0
LEFT_MARGIN = 42.0
RIGHT_MARGIN = 42.0
TOP_MARGIN = 44.0
BOTTOM_MARGIN = 40.0
HEADER_HEIGHT = 24.0
FOOTER_HEIGHT = 22.0
CONTENT_WIDTH = PAGE_WIDTH - LEFT_MARGIN - RIGHT_MARGIN
CONTENT_BOTTOM = PAGE_HEIGHT - BOTTOM_MARGIN - FOOTER_HEIGHT

INK = (0.14, 0.15, 0.18)
MUTED = (0.34, 0.36, 0.39)
ACCENT = (0.74, 0.47, 0.18)
ACCENT_DARK = (0.41, 0.25, 0.08)
SOFT_FILL = (0.96, 0.93, 0.88)
RULE = (0.82, 0.78, 0.73)
WHITE = (1.0, 1.0, 1.0)


@dataclass(frozen=True)
class Workflow:
    id: str
    order: int
    title: str
    lane: str
    question: str
    rationale: str
    blind_value: str
    examples: tuple[str, ...]


WORKFLOWS: tuple[Workflow, ...] = (
    Workflow(
        id="orientation_set_scanning",
        order=1,
        title="Orientation and Set Scanning",
        lane="` + n",
        question="Where am I, and what is immediately around me?",
        rationale=(
            "Blind and vision-impaired musicians need a stable orientation layer before any launch, "
            "record, or edit decision. This lane prioritizes focus, track identity, scene identity, "
            "and the currently highlighted slot."
        ),
        blind_value=(
            "This lane reduces guessing and panic. It turns Session View from a spatially hidden grid "
            "into a spoken coordinate system."
        ),
        examples=("track name", "selected track", "selected scene", "highlighted clip slot"),
    ),
    Workflow(
        id="clip_scene_discovery",
        order=2,
        title="Clip and Scene Discovery",
        lane="` + c",
        question="What is in this slot or scene before I act on it?",
        rationale=(
            "Discovery should answer identity first: whether a slot is empty, whether a clip exists, "
            "what the clip is called, and what kind of material it contains."
        ),
        blind_value=(
            "This lane supports safe browsing, recall, and setup. It keeps the musician from launching "
            "unknown material just to learn what is there."
        ),
        examples=("has clip", "clip name", "scene name", "audio or MIDI clip"),
    ),
    Workflow(
        id="launch_performance_state",
        order=3,
        title="Launch and Performance State",
        lane="` + p",
        question="What is sounding or about to sound right now?",
        rationale=(
            "Performance state is a low-latency safety layer. The musician needs immediate confirmation "
            "about triggered, playing, or back-to-arranger states before launching again."
        ),
        blind_value=(
            "This lane prevents accidental relaunches, dead air, and confusion about whether a clip is "
            "already active, queued, or overridden."
        ),
        examples=("playing status", "triggered state", "playing slot index", "back to arranger"),
    ),
    Workflow(
        id="recording_capture_safety",
        order=4,
        title="Recording and Capture Safety",
        lane="` + r",
        question="Am I about to record, overdub, or overwrite something important?",
        rationale=(
            "Recording errors are expensive. A blind or VI workflow must surface arm state, session "
            "record, overdub, count-in, and will-record-on-start signals before capture begins."
        ),
        blind_value=(
            "This lane treats recording as a safety-critical workflow. It minimizes destructive mistakes "
            "and supports confidence before committing a take."
        ),
        examples=("track arm", "session record", "overdub", "will record on start"),
    ),
    Workflow(
        id="timing_loop_grid_control",
        order=5,
        title="Timing, Loop, and Grid Control",
        lane="` + t",
        question="How is time structured here?",
        rationale=(
            "Time structure governs groove, launch confidence, and edit accuracy. This lane gathers "
            "tempo, quantization, loop boundaries, grid state, and related clip timing metadata."
        ),
        blind_value=(
            "This lane gives blind and VI users the same phrase-level confidence sighted users get from "
            "reading loop braces, grid lines, and time rulers."
        ),
        examples=("tempo", "loop start", "loop end", "launch quantization"),
    ),
    Workflow(
        id="mixer_metering_balance",
        order=6,
        title="Mixer, Metering, and Balance",
        lane="` + m",
        question="How loud is this, and how is it positioned in the mix?",
        rationale=(
            "Mix choices must be speakable. This lane covers mute, solo, meters, volume, pan, sends, "
            "crossfader state, and readable parameter values tied to the mixer strip."
        ),
        blind_value=(
            "This lane replaces visual meter glances with deterministic readouts so balancing decisions "
            "can stay keyboard-first."
        ),
        examples=("volume", "panning", "solo", "output meter level"),
    ),
    Workflow(
        id="track_device_routing_architecture",
        order=7,
        title="Track, Device, and Routing Architecture",
        lane="` + d",
        question="How is this track wired, focused, or structurally configured?",
        rationale=(
            "As projects grow, routing and device focus become navigation problems. This lane groups "
            "track structure, chain visibility, routing channels, and selected device or parameter focus."
        ),
        blind_value=(
            "This lane exposes the technical architecture that is usually only obvious from the screen, "
            "which is essential for complex sets and collaboration."
        ),
        examples=("selected parameter", "input routing type", "output routing channel", "selected device"),
    ),
    Workflow(
        id="global_session_governance",
        order=8,
        title="Global Session Governance",
        lane="` + g",
        question="What set-wide conditions are shaping the whole session?",
        rationale=(
            "Some states are not local to a track or clip. Link, automation, cue availability, undo or "
            "redo, scale context, and transport policy all belong to a session-wide governance layer."
        ),
        blind_value=(
            "This lane keeps global surprises out of the way. It helps the musician trust that the "
            "environment itself is behaving as expected."
        ),
        examples=("Ableton Link enabled", "undo available", "automation re-enable", "scale name"),
    ),
)


WORKFLOW_BY_ID = {workflow.id: workflow for workflow in WORKFLOWS}
WORKFLOW_ORDER = {workflow.id: workflow.order for workflow in WORKFLOWS}
PRIORITY_ORDER = {"core": 0, "extended": 1, "deep": 2}
OBJECT_ORDER = {
    "Song.View": 0,
    "Song": 1,
    "Scene": 2,
    "Track": 3,
    "Track.View": 4,
    "ClipSlot": 5,
    "Clip": 6,
    "Clip.View": 7,
    "MixerDevice": 8,
    "DeviceParameter": 9,
}
MEMBER_TYPE_ORDER = {"child": 0, "property": 1}

CURRENT_WORKFLOW_NAMES = {
    "orientation_location": "Orientation / Location",
    "clip_presence": "Clip Presence",
    "action_status": "Action Status",
    "timing_loop": "Timing / Loop",
    "trigger_feedback": "Trigger / Feedback",
    "identity_reference": "Identity / Reference",
}


class PDFPage:
    def __init__(self) -> None:
        self.commands: list[str] = []

    def add(self, command: str) -> None:
        self.commands.append(command)

    def extend(self, commands: Iterable[str]) -> None:
        self.commands.extend(commands)

    def content(self) -> str:
        return "\n".join(self.commands) + ("\n" if self.commands else "")


class PDFWriter:
    def __init__(self, pages: list[PDFPage]) -> None:
        self.pages = pages

    def _stream_object(self, payload: str) -> bytes:
        data = payload.encode("utf-8")
        header = f"<< /Length {len(data)} >>\nstream\n".encode("utf-8")
        return header + data + b"endstream"

    def write(self, path: Path) -> None:
        path.parent.mkdir(parents=True, exist_ok=True)
        objects: list[bytes | None] = []

        def reserve() -> int:
            objects.append(None)
            return len(objects)

        def set_object(object_id: int, value: str | bytes) -> None:
            objects[object_id - 1] = value.encode("utf-8") if isinstance(value, str) else value

        font_regular = reserve()
        font_bold = reserve()
        font_mono = reserve()
        font_mono_bold = reserve()
        pages_id = reserve()
        page_ids = [reserve() for _ in self.pages]
        content_ids = [reserve() for _ in self.pages]
        catalog_id = reserve()

        set_object(font_regular, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica >>")
        set_object(font_bold, "<< /Type /Font /Subtype /Type1 /BaseFont /Helvetica-Bold >>")
        set_object(font_mono, "<< /Type /Font /Subtype /Type1 /BaseFont /BaseFont /Courier >>".replace("/BaseFont /BaseFont", "/BaseFont"))
        set_object(font_mono_bold, "<< /Type /Font /Subtype /Type1 /BaseFont /Courier-Bold >>")

        for index, page in enumerate(self.pages):
            payload = page.content()
            set_object(content_ids[index], self._stream_object(payload))
            page_body = (
                f"<< /Type /Page /Parent {pages_id} 0 R "
                f"/MediaBox [0 0 {pdf_num(PAGE_WIDTH)} {pdf_num(PAGE_HEIGHT)}] "
                f"/Resources << /Font << "
                f"/F1 {font_regular} 0 R /F2 {font_bold} 0 R "
                f"/F3 {font_mono} 0 R /F4 {font_mono_bold} 0 R >> >> "
                f"/Contents {content_ids[index]} 0 R >>"
            )
            set_object(page_ids[index], page_body)

        kids = " ".join(f"{page_id} 0 R" for page_id in page_ids)
        set_object(
            pages_id,
            f"<< /Type /Pages /Count {len(page_ids)} /Kids [{kids}] >>",
        )
        set_object(catalog_id, f"<< /Type /Catalog /Pages {pages_id} 0 R >>")

        output = bytearray(b"%PDF-1.4\n%\xe2\xe3\xcf\xd3\n")
        offsets = [0]
        for object_id, body in enumerate(objects, start=1):
            if body is None:
                raise RuntimeError(f"PDF object {object_id} was not written")
            offsets.append(len(output))
            output.extend(f"{object_id} 0 obj\n".encode("utf-8"))
            output.extend(body)
            output.extend(b"\nendobj\n")

        xref_offset = len(output)
        output.extend(f"xref\n0 {len(objects) + 1}\n".encode("utf-8"))
        output.extend(b"0000000000 65535 f \n")
        for offset in offsets[1:]:
            output.extend(f"{offset:010d} 00000 n \n".encode("utf-8"))
        output.extend(
            (
                f"trailer << /Size {len(objects) + 1} /Root {catalog_id} 0 R >>\n"
                f"startxref\n{xref_offset}\n%%EOF\n"
            ).encode("utf-8")
        )
        path.write_bytes(output)


class LayoutDocument:
    def __init__(self, title: str, subtitle: str) -> None:
        self.title = title
        self.subtitle = subtitle
        self.pages: list[PDFPage] = []
        self.cursor_y = TOP_MARGIN + HEADER_HEIGHT
        self.new_page()

    def new_page(self) -> None:
        page = PDFPage()
        page.add(f"{color_fill(WHITE)}{rect_cmd(0, 0, PAGE_WIDTH, PAGE_HEIGHT)}")
        self.pages.append(page)
        self.cursor_y = TOP_MARGIN + HEADER_HEIGHT

    @property
    def page(self) -> PDFPage:
        return self.pages[-1]

    def ensure_space(self, height: float) -> None:
        if self.cursor_y + height > CONTENT_BOTTOM:
            self.new_page()

    def add_header_footer(self) -> None:
        page_total = len(self.pages)
        for index, page in enumerate(self.pages, start=1):
            if index == 1:
                header_fill = color_fill(SOFT_FILL)
                page.add(
                    f"{header_fill}{rect_cmd(0, 0, PAGE_WIDTH, TOP_MARGIN + 12)}"
                )
            else:
                page.add(
                    f"{color_stroke(RULE)}0.5 w {line_cmd(LEFT_MARGIN, TOP_MARGIN + HEADER_HEIGHT - 6, PAGE_WIDTH - RIGHT_MARGIN, TOP_MARGIN + HEADER_HEIGHT - 6)}"
                )
                add_text(
                    page,
                    LEFT_MARGIN,
                    TOP_MARGIN + 4,
                    self.title,
                    font="F2",
                    size=10,
                    color=MUTED,
                )
                add_text(
                    page,
                    PAGE_WIDTH - RIGHT_MARGIN - 110,
                    TOP_MARGIN + 4,
                    self.subtitle,
                    font="F1",
                    size=8.5,
                    color=MUTED,
                )
            page.add(
                f"{color_stroke(RULE)}0.5 w {line_cmd(LEFT_MARGIN, PAGE_HEIGHT - BOTTOM_MARGIN - FOOTER_HEIGHT + 4, PAGE_WIDTH - RIGHT_MARGIN, PAGE_HEIGHT - BOTTOM_MARGIN - FOOTER_HEIGHT + 4)}"
            )
            add_text(
                page,
                LEFT_MARGIN,
                PAGE_HEIGHT - BOTTOM_MARGIN - 12,
                "Generated from workflow-sorted LiveAPI inventory",
                font="F1",
                size=8.5,
                color=MUTED,
            )
            add_text(
                page,
                PAGE_WIDTH - RIGHT_MARGIN - 54,
                PAGE_HEIGHT - BOTTOM_MARGIN - 12,
                f"{index} / {page_total}",
                font="F2",
                size=8.5,
                color=MUTED,
            )

    def title_page(self, generated_on: str) -> None:
        self.page.add(f"{color_fill(SOFT_FILL)}{rect_cmd(0, 0, PAGE_WIDTH, 210)}")
        self.page.add(f"{color_fill(ACCENT)}{rect_cmd(LEFT_MARGIN, 86, 8, 88)}")
        add_text_lines(
            self.page,
            LEFT_MARGIN + 22,
            94,
            ["Blind and VI-First Session View", "Accessibility Strings"],
            font="F2",
            size=21,
            leading=25,
            color=INK,
        )
        add_text(
            self.page,
            LEFT_MARGIN + 22,
            144,
            "Workflow-sorted PDF report for Ableton Live / Clip Announcer research",
            font="F1",
            size=12,
            color=MUTED,
        )
        add_text(
            self.page,
            LEFT_MARGIN + 22,
            166,
            generated_on,
            font="F1",
            size=11,
            color=ACCENT_DARK,
        )
        self.cursor_y = 236
        self.paragraph(
            "Purpose: create a coherent, blind and vision-impaired-first layout of exposed Session View "
            "accessibility strings, sort them by real music-making workflow, and frame a deterministic "
            "voice-reader palette as the interaction model.",
            size=11.5,
            leading=15,
        )
        self.callout(
            "Research stance",
            (
                "This report intentionally avoids an LLM in the interaction loop. The preferred model is "
                "an inert, deterministic voice-reader: safer for a basic access need, lighter on compute, "
                "and easier to trust under performance conditions. Voice quality can be upgraded later "
                "without adding inference."
            ),
        )
        self.section_title("Key Findings")
        self.bullets(
            [
                "Workflow grouping is more important than raw API breadth. Blind and VI users need stable spoken categories before they need more data.",
                "A single palette entry point such as the backquote key can reduce cognitive load if every modifier keeps the same semantic meaning.",
                "The current Clip Announcer WHERE / WHAT / STATE model already maps well to three of the most important workflow lanes and can be expanded rather than replaced.",
                "A smoother deterministic TTS voice, comparable in listener comfort to commercial voice-reader products, is a voice-layer upgrade rather than an intelligence-layer requirement.",
            ],
            bullet_indent=14,
        )
        self.section_title("Source Scope")
        self.bullets(
            [
                "Current beta inventory: SESSION_UI_TERMS_INVENTORY.csv (43 rows).",
                "Exhaustive readable Session View surface: SESSION_VIEW_READABLE_UI_MASTER_LIST.csv (221 rows).",
                "Scope is Session View and related LiveAPI-readable context, not the full Arrangement View UI.",
            ],
            bullet_indent=14,
        )

    def section_title(self, text: str) -> None:
        self.ensure_space(28)
        y = self.cursor_y
        self.page.add(f"{color_fill(SOFT_FILL)}{rect_cmd(LEFT_MARGIN, y, CONTENT_WIDTH, 20)}")
        self.page.add(f"{color_fill(ACCENT)}{rect_cmd(LEFT_MARGIN, y, 6, 20)}")
        add_text(self.page, LEFT_MARGIN + 14, y + 4, text, font="F2", size=13, color=INK)
        self.cursor_y += 28

    def subhead(self, text: str) -> None:
        self.ensure_space(18)
        add_text(self.page, LEFT_MARGIN, self.cursor_y, text, font="F2", size=11, color=ACCENT_DARK)
        self.cursor_y += 16

    def paragraph(
        self,
        text: str,
        *,
        size: float = 10.5,
        leading: float = 14.0,
        color: tuple[float, float, float] = INK,
    ) -> None:
        lines = wrap_text(text, CONTENT_WIDTH, size, font="F1")
        height = len(lines) * leading + 2
        self.ensure_space(height)
        add_text_lines(
            self.page,
            LEFT_MARGIN,
            self.cursor_y,
            lines,
            font="F1",
            size=size,
            leading=leading,
            color=color,
        )
        self.cursor_y += height

    def bullets(
        self,
        items: list[str],
        *,
        size: float = 10.2,
        leading: float = 13.5,
        bullet_indent: float = 12.0,
    ) -> None:
        for item in items:
            text_width = CONTENT_WIDTH - bullet_indent - 10
            lines = wrap_text(item, text_width, size, font="F1")
            height = max(leading, len(lines) * leading) + 1
            self.ensure_space(height)
            add_text(self.page, LEFT_MARGIN, self.cursor_y, "-", font="F2", size=size, color=ACCENT_DARK)
            add_text_lines(
                self.page,
                LEFT_MARGIN + bullet_indent,
                self.cursor_y,
                lines,
                font="F1",
                size=size,
                leading=leading,
                color=INK,
            )
            self.cursor_y += height

    def callout(self, title: str, text: str) -> None:
        lines = wrap_text(text, CONTENT_WIDTH - 24, 10.2, font="F1")
        height = 22 + len(lines) * 13.0 + 10
        self.ensure_space(height)
        y = self.cursor_y
        self.page.add(f"{color_fill(SOFT_FILL)}{rect_cmd(LEFT_MARGIN, y, CONTENT_WIDTH, height)}")
        self.page.add(f"{color_stroke(ACCENT)}1 w {rect_outline_cmd(LEFT_MARGIN, y, CONTENT_WIDTH, height)}")
        add_text(self.page, LEFT_MARGIN + 12, y + 8, title, font="F2", size=11, color=ACCENT_DARK)
        add_text_lines(
            self.page,
            LEFT_MARGIN + 12,
            y + 24,
            lines,
            font="F1",
            size=10.2,
            leading=13,
            color=INK,
        )
        self.cursor_y += height + 10

    def table(
        self,
        headers: list[str],
        rows: list[list[str]],
        widths: list[float],
        *,
        body_font: str = "F1",
        body_size: float = 8.0,
        body_leading: float = 10.5,
        header_font: str = "F2",
        header_size: float = 8.4,
        repeat_header: bool = True,
    ) -> None:
        if abs(sum(widths) - CONTENT_WIDTH) > 0.2:
            raise ValueError("table widths must equal content width")

        def row_metrics(cells: list[str], font: str, size: float) -> tuple[list[list[str]], float]:
            wrapped: list[list[str]] = []
            max_lines = 1
            for cell, width in zip(cells, widths):
                lines = wrap_text(cell, width - 8, size, font=font) or [""]
                wrapped.append(lines)
                max_lines = max(max_lines, len(lines))
            return wrapped, max_lines * body_leading + 8

        def draw_header() -> None:
            header_lines: list[list[str]] = []
            max_lines = 1
            for cell, width in zip(headers, widths):
                lines = wrap_text(cell, width - 8, header_size, font=header_font) or [""]
                header_lines.append(lines)
                max_lines = max(max_lines, len(lines))
            height = max_lines * (header_size + 1.8) + 8
            self.ensure_space(height)
            y = self.cursor_y
            x = LEFT_MARGIN
            for cell_lines, width in zip(header_lines, widths):
                self.page.add(f"{color_fill(SOFT_FILL)}{rect_cmd(x, y, width, height)}")
                self.page.add(f"{color_stroke(RULE)}0.5 w {rect_outline_cmd(x, y, width, height)}")
                add_text_lines(
                    self.page,
                    x + 4,
                    y + 4,
                    cell_lines,
                    font=header_font,
                    size=header_size,
                    leading=header_size + 1.8,
                    color=ACCENT_DARK,
                )
                x += width
            self.cursor_y += height

        if repeat_header:
            draw_header()

        for row in rows:
            wrapped_cells, height = row_metrics(row, body_font, body_size)
            if self.cursor_y + height > CONTENT_BOTTOM:
                self.new_page()
                if repeat_header:
                    draw_header()
            y = self.cursor_y
            x = LEFT_MARGIN
            for cell_lines, width in zip(wrapped_cells, widths):
                self.page.add(f"{color_stroke(RULE)}0.45 w {rect_outline_cmd(x, y, width, height)}")
                add_text_lines(
                    self.page,
                    x + 4,
                    y + 4,
                    cell_lines,
                    font=body_font,
                    size=body_size,
                    leading=body_leading,
                    color=INK,
                )
                x += width
            self.cursor_y += height


def pdf_num(value: float) -> str:
    text = f"{value:.2f}"
    return text.rstrip("0").rstrip(".")


def pdf_escape(text: str) -> str:
    return text.replace("\\", "\\\\").replace("(", "\\(").replace(")", "\\)")


def rgb(color: tuple[float, float, float]) -> str:
    return " ".join(pdf_num(part) for part in color)


def color_fill(color: tuple[float, float, float]) -> str:
    return f"{rgb(color)} rg "


def color_stroke(color: tuple[float, float, float]) -> str:
    return f"{rgb(color)} RG "


def rect_cmd(x: float, y: float, width: float, height: float) -> str:
    bottom = PAGE_HEIGHT - y - height
    return f"{pdf_num(x)} {pdf_num(bottom)} {pdf_num(width)} {pdf_num(height)} re f\n"


def rect_outline_cmd(x: float, y: float, width: float, height: float) -> str:
    bottom = PAGE_HEIGHT - y - height
    return f"{pdf_num(x)} {pdf_num(bottom)} {pdf_num(width)} {pdf_num(height)} re S\n"


def line_cmd(x1: float, y1: float, x2: float, y2: float) -> str:
    return (
        f"{pdf_num(x1)} {pdf_num(PAGE_HEIGHT - y1)} m "
        f"{pdf_num(x2)} {pdf_num(PAGE_HEIGHT - y2)} l S\n"
    )


def add_text(
    page: PDFPage,
    x: float,
    y: float,
    text: str,
    *,
    font: str,
    size: float,
    color: tuple[float, float, float],
) -> None:
    baseline = PAGE_HEIGHT - y - size
    page.add(
        f"BT {rgb(color)} rg /{font} {pdf_num(size)} Tf "
        f"1 0 0 1 {pdf_num(x)} {pdf_num(baseline)} Tm "
        f"({pdf_escape(text)}) Tj ET"
    )


def add_text_lines(
    page: PDFPage,
    x: float,
    y: float,
    lines: list[str],
    *,
    font: str,
    size: float,
    leading: float,
    color: tuple[float, float, float],
) -> None:
    if not lines:
        lines = [""]
    baseline = PAGE_HEIGHT - y - size
    commands = [
        "BT",
        f"{rgb(color)} rg",
        f"/{font} {pdf_num(size)} Tf",
        f"{pdf_num(leading)} TL",
        f"1 0 0 1 {pdf_num(x)} {pdf_num(baseline)} Tm",
    ]
    first, *rest = lines
    commands.append(f"({pdf_escape(first)}) Tj")
    for line in rest:
        commands.append("T*")
        commands.append(f"({pdf_escape(line)}) Tj")
    commands.append("ET")
    page.add(" ".join(commands))


def measure_text(text: str, size: float, font: str) -> float:
    if font in {"F3", "F4"}:
        return len(text) * size * 0.6
    total = 0.0
    for char in text:
        if char == " ":
            total += 0.28
        elif char in "ilI.,:;!'|":
            total += 0.25
        elif char in "mwMW@%#&Q":
            total += 0.86
        elif char.isupper():
            total += 0.68
        elif char.isdigit():
            total += 0.56
        else:
            total += 0.53
    return total * size


def wrap_text(text: str, width: float, size: float, *, font: str) -> list[str]:
    text = " ".join(text.split())
    if not text:
        return [""]

    words = text.split(" ")
    lines: list[str] = []
    current = words[0]
    for word in words[1:]:
        candidate = f"{current} {word}"
        if measure_text(candidate, size, font) <= width:
            current = candidate
            continue
        if measure_text(word, size, font) > width:
            split_word = split_long_token(word, width, size, font)
            if current:
                lines.append(current)
            lines.extend(split_word[:-1])
            current = split_word[-1]
            continue
        lines.append(current)
        current = word
    if current:
        lines.append(current)
    return lines


def split_long_token(token: str, width: float, size: float, font: str) -> list[str]:
    pieces: list[str] = []
    current = ""
    for char in token:
        candidate = current + char
        if current and measure_text(candidate, size, font) > width:
            pieces.append(current)
            current = char
        else:
            current = candidate
    if current:
        pieces.append(current)
    return pieces or [token]


def friendly_object_name(object_name: str) -> str:
    return {
        "Song.View": "selection",
        "Song": "song",
        "Scene": "scene",
        "Track": "track",
        "Track.View": "track view",
        "ClipSlot": "clip slot",
        "Clip": "clip",
        "Clip.View": "clip view",
        "MixerDevice": "mixer",
        "DeviceParameter": "parameter",
    }.get(object_name, object_name.lower())


def readable_label(row: dict[str, str]) -> str:
    object_name = row["object"]
    name = row["member_name"]
    object_prefix = friendly_object_name(object_name)
    special = {
        ("Song", "name"): "Set name",
        ("Scene", "name"): "Scene name",
        ("Track", "name"): "Track name",
        ("Clip", "name"): "Clip name",
        ("DeviceParameter", "name"): "Parameter name",
        ("Song", "view"): "Song view",
        ("Track", "view"): "Track view",
        ("Clip", "view"): "Clip view",
        ("Track", "clip_slots"): "Track clip slots",
        ("Scene", "clip_slots"): "Scene clip slots",
        ("ClipSlot", "clip"): "Clip in slot",
        ("Track", "devices"): "Track devices",
        ("Track", "mixer_device"): "Track mixer device",
        ("Song", "tracks"): "Track list",
        ("Song", "visible_tracks"): "Visible track list",
        ("Song", "scenes"): "Scene list",
        ("Song", "return_tracks"): "Return track list",
        ("Song", "master_track"): "Master track",
        ("Song.View", "selected_track"): "Selected track",
        ("Song.View", "selected_scene"): "Selected scene",
        ("Song.View", "selected_parameter"): "Selected parameter",
        ("Song.View", "selected_chain"): "Selected chain",
        ("Song.View", "highlighted_clip_slot"): "Highlighted clip slot",
        ("Song.View", "detail_clip"): "Detail clip",
        ("Song", "appointed_device"): "Appointed device",
        ("Track.View", "selected_device"): "Selected device",
        ("Track.View", "selected_track"): "Selected track in view",
        ("Track.View", "visible_tracks"): "Visible tracks in view",
        ("Clip", "available_warp_modes"): "Available warp modes",
        ("Clip.View", "show_warp_as"): "Show warp as",
        ("MixerDevice", "track_activator"): "Track activator",
        ("DeviceParameter", "display_value"): "Display value",
        ("Song", "is_ableton_link_enabled"): "Ableton Link enabled",
        ("Song", "is_ableton_link_start_stop_sync_enabled"): "Ableton Link start/stop sync enabled",
        ("Song", "clip_trigger_quantization"): "Clip trigger quantization",
        ("Song", "session_automation_record"): "Session automation record",
        ("Song", "session_record_status"): "Session record status",
        ("ClipSlot", "has_stop_button"): "Slot has stop button",
        ("ClipSlot", "controls_other_clips"): "Controls other clips",
        ("ClipSlot", "will_record_on_start"): "Will record on start",
        ("Track", "fired_slot_index"): "Fired slot index",
        ("Track", "playing_slot_index"): "Playing slot index",
        ("Track", "input_meter_level"): "Input meter level",
        ("Track", "output_meter_level"): "Output meter level",
    }
    if (object_name, name) in special:
        return special[(object_name, name)]

    if name in {"name", "color", "color_index"}:
        return f"{object_prefix} {name.replace('_', ' ')}".title()
    if name == "view":
        return f"{object_prefix} view".title()
    if name.startswith("is_"):
        return name[3:].replace("_", " ").title()
    if name.startswith("has_"):
        return "Has " + name[4:].replace("_", " ")
    if name.startswith("can_"):
        return "Can " + name[4:].replace("_", " ")
    return name.replace("_", " ").title()


def short_context(row: dict[str, str]) -> str:
    path = row["canonical_path"].replace("live_set ", "")
    member_kind = "child" if row["member_type"] == "child" else "prop"
    return f"{row['object']} {member_kind} @ {path}"


def classify_workflow(row: dict[str, str]) -> str:
    object_name = row["object"]
    member = row["member_name"]

    if object_name == "Song.View":
        if member in {"selected_chain", "selected_parameter"}:
            return "track_device_routing_architecture"
        if member == "follow_song":
            return "launch_performance_state"
        return "orientation_set_scanning"

    if object_name == "Song":
        if member in {"appointed_device"}:
            return "track_device_routing_architecture"
        if member in {
            "arrangement_overdub",
            "can_capture_midi",
            "count_in_duration",
            "is_counting_in",
            "overdub",
            "punch_in",
            "punch_out",
            "record_mode",
            "session_record",
            "session_record_status",
        }:
            return "recording_capture_safety"
        if member in {
            "clip_trigger_quantization",
            "current_song_time",
            "groove_amount",
            "last_event_time",
            "loop",
            "loop_length",
            "loop_start",
            "metronome",
            "midi_recording_quantization",
            "signature_denominator",
            "signature_numerator",
            "song_length",
            "start_time",
            "swing_amount",
            "tempo",
        }:
            return "timing_loop_grid_control"
        if member in {
            "can_jump_to_next_cue",
            "can_jump_to_prev_cue",
            "can_redo",
            "can_undo",
            "exclusive_arm",
            "exclusive_solo",
            "file_path",
            "is_ableton_link_enabled",
            "is_ableton_link_start_stop_sync_enabled",
            "name",
            "nudge_down",
            "nudge_up",
            "re_enable_automation_enabled",
            "root_note",
            "scale_intervals",
            "scale_mode",
            "scale_name",
            "select_on_launch",
            "session_automation_record",
            "tempo_follower_enabled",
        }:
            return "global_session_governance"
        if member in {
            "cue_points",
            "master_track",
            "return_tracks",
            "scenes",
            "tracks",
            "visible_tracks",
            "view",
            "groove_pool",
            "tuning_system",
        }:
            return "orientation_set_scanning"
        if member in {"back_to_arranger", "is_playing"}:
            return "launch_performance_state"

    if object_name == "Scene":
        if member in {
            "tempo",
            "tempo_enabled",
            "time_signature_numerator",
            "time_signature_denominator",
            "time_signature_enabled",
        }:
            return "timing_loop_grid_control"
        if member == "is_triggered":
            return "launch_performance_state"
        return "orientation_set_scanning"

    if object_name == "Track":
        if member in {"arm", "can_be_armed", "implicit_arm"}:
            return "recording_capture_safety"
        if member in {
            "input_meter_left",
            "input_meter_level",
            "input_meter_right",
            "mute",
            "muted_via_solo",
            "output_meter_left",
            "output_meter_level",
            "output_meter_right",
            "performance_impact",
            "solo",
        }:
            return "mixer_metering_balance"
        if member in {"fired_slot_index", "playing_slot_index", "back_to_arranger"}:
            return "launch_performance_state"
        if member in {"name", "color", "color_index", "is_part_of_selection", "is_visible", "clip_slots"}:
            return "orientation_set_scanning"
        return "track_device_routing_architecture"

    if object_name == "Track.View":
        if member in {"selected_track", "visible_tracks"}:
            return "orientation_set_scanning"
        return "track_device_routing_architecture"

    if object_name == "ClipSlot":
        if member in {"is_playing", "is_recording", "is_triggered", "playing_status"}:
            return "launch_performance_state"
        if member == "will_record_on_start":
            return "recording_capture_safety"
        return "clip_scene_discovery"

    if object_name == "Clip":
        if member in {"is_playing", "is_triggered", "playing_position", "playing_status", "position"}:
            return "launch_performance_state"
        if member in {"is_recording", "is_overdubbing"}:
            return "recording_capture_safety"
        if member in {
            "end_marker",
            "end_time",
            "groove",
            "launch_mode",
            "launch_quantization",
            "legato",
            "length",
            "loop_end",
            "loop_jump",
            "loop_start",
            "looping",
            "pitch_coarse",
            "pitch_fine",
            "sample_length",
            "sample_rate",
            "start_marker",
            "start_time",
            "velocity_amount",
            "warp_mode",
            "warping",
            "available_warp_modes",
        }:
            return "timing_loop_grid_control"
        if member in {"gain", "gain_display_string"}:
            return "mixer_metering_balance"
        return "clip_scene_discovery"

    if object_name == "Clip.View":
        return "timing_loop_grid_control"

    if object_name in {"MixerDevice", "DeviceParameter"}:
        return "mixer_metering_balance"

    return "global_session_governance"


def classify_priority(row: dict[str, str], workflow_id: str) -> str:
    object_name = row["object"]
    member = row["member_name"]

    core_by_workflow = {
        "orientation_set_scanning": {
            "highlighted_clip_slot",
            "selected_scene",
            "selected_track",
            "tracks",
            "scenes",
            "visible_tracks",
            "name",
            "is_visible",
            "is_part_of_selection",
        },
        "clip_scene_discovery": {
            "clip",
            "clip_slots",
            "has_clip",
            "has_stop_button",
            "is_empty",
            "is_audio_clip",
            "is_midi_clip",
            "name",
        },
        "launch_performance_state": {
            "back_to_arranger",
            "fired_slot_index",
            "follow_song",
            "is_playing",
            "is_triggered",
            "playing_position",
            "playing_slot_index",
            "playing_status",
            "position",
            "select_on_launch",
        },
        "recording_capture_safety": {
            "arm",
            "can_be_armed",
            "is_recording",
            "overdub",
            "record_mode",
            "session_record",
            "session_record_status",
            "will_record_on_start",
        },
        "timing_loop_grid_control": {
            "clip_trigger_quantization",
            "current_song_time",
            "grid_quantization",
            "launch_quantization",
            "length",
            "loop_end",
            "loop_start",
            "looping",
            "metronome",
            "signature_denominator",
            "signature_numerator",
            "tempo",
        },
        "mixer_metering_balance": {
            "cue_volume",
            "display_value",
            "input_meter_level",
            "mute",
            "output_meter_level",
            "panning",
            "solo",
            "track_activator",
            "value",
            "volume",
        },
        "track_device_routing_architecture": {
            "appointed_device",
            "devices",
            "group_track",
            "input_routing_channel",
            "input_routing_type",
            "output_routing_channel",
            "output_routing_type",
            "selected_chain",
            "selected_device",
            "selected_parameter",
        },
        "global_session_governance": {
            "can_jump_to_next_cue",
            "can_jump_to_prev_cue",
            "can_redo",
            "can_undo",
            "exclusive_arm",
            "exclusive_solo",
            "is_ableton_link_enabled",
            "is_ableton_link_start_stop_sync_enabled",
            "re_enable_automation_enabled",
            "session_automation_record",
        },
    }

    deep_names = {
        "automation_state",
        "color_index",
        "default_value",
        "draw_mode",
        "groove_pool",
        "last_event_time",
        "max",
        "min",
        "original_name",
        "performance_impact",
        "sample_length",
        "sample_rate",
        "state",
        "tuning_system",
        "value_items",
    }

    if member in core_by_workflow.get(workflow_id, set()):
        return "core"
    if member in deep_names:
        return "deep"
    if object_name == "DeviceParameter" and member not in {"display_value", "value"}:
        return "deep"
    return "extended"


def blind_vi_purpose(workflow_id: str) -> str:
    purposes = {
        "orientation_set_scanning": "Confirms current location and nearby structure.",
        "clip_scene_discovery": "Reveals identity before the user triggers anything.",
        "launch_performance_state": "Prevents accidental relaunches and silent mistakes.",
        "recording_capture_safety": "Reduces destructive recording errors.",
        "timing_loop_grid_control": "Communicates phrase structure and edit timing.",
        "mixer_metering_balance": "Supports level, pan, and meter decisions without sight.",
        "track_device_routing_architecture": "Exposes wiring, chains, and focus targets.",
        "global_session_governance": "Confirms set-wide policies and transport conditions.",
    }
    return purposes[workflow_id]


def enrich_master_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    enriched: list[dict[str, str]] = []
    for row in rows:
        workflow_id = classify_workflow(row)
        workflow = WORKFLOW_BY_ID[workflow_id]
        enriched_row = dict(row)
        enriched_row["workflow_id"] = workflow_id
        enriched_row["workflow_title"] = workflow.title
        enriched_row["workflow_order"] = str(workflow.order)
        enriched_row["palette_lane"] = workflow.lane
        enriched_row["accessible_label"] = readable_label(row)
        enriched_row["context_label"] = short_context(row)
        enriched_row["priority_tier"] = classify_priority(row, workflow_id)
        enriched_row["blind_vi_purpose"] = blind_vi_purpose(workflow_id)
        enriched.append(enriched_row)

    enriched.sort(
        key=lambda row: (
            int(row["workflow_order"]),
            PRIORITY_ORDER[row["priority_tier"]],
            OBJECT_ORDER.get(row["object"], 99),
            MEMBER_TYPE_ORDER.get(row["member_type"], 9),
            row["accessible_label"].lower(),
            row["member_name"].lower(),
        )
    )
    return enriched


def load_csv(path: Path) -> list[dict[str, str]]:
    with path.open(newline="", encoding="utf-8") as handle:
        return list(csv.DictReader(handle))


def write_csv(path: Path, rows: list[dict[str, str]], fieldnames: list[str]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as handle:
        writer = csv.DictWriter(handle, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(rows)


def generated_on_label() -> str:
    today = date.today()
    return f"Generated {today:%B} {today.day}, {today.year}"


def workflow_summary_rows(enriched_rows: list[dict[str, str]]) -> list[list[str]]:
    grouped: dict[str, list[dict[str, str]]] = defaultdict(list)
    for row in enriched_rows:
        grouped[row["workflow_id"]].append(row)

    rows: list[list[str]] = []
    for workflow in WORKFLOWS:
        members = grouped[workflow.id]
        core_labels = [row["accessible_label"].lower() for row in members if row["priority_tier"] == "core"][:4]
        rows.append(
            [
                workflow.lane,
                workflow.title,
                workflow.question,
                str(len(members)),
                ", ".join(core_labels),
            ]
        )
    return rows


def modifier_rows() -> list[list[str]]:
    return [
        ["` + key", "Speak the concise summary for the chosen workflow lane."],
        ["Shift + ` + key", "Speak expanded detail in the same lane without changing categories."],
        ["Control + ` + key", "Prefer raw values, indices, and exact numeric state when available."],
        ["Option + ` + key", "Turn on monitored or repeating readouts only for that lane, to avoid speech overload."],
    ]


def workflow_section_rows(enriched_rows: list[dict[str, str]], workflow_id: str) -> list[dict[str, str]]:
    return [row for row in enriched_rows if row["workflow_id"] == workflow_id]


def current_inventory_rows(rows: list[dict[str, str]]) -> list[dict[str, str]]:
    ordered = list(rows)
    ordered.sort(
        key=lambda row: (
            list(CURRENT_WORKFLOW_NAMES).index(row["workflow_group"])
            if row["workflow_group"] in CURRENT_WORKFLOW_NAMES
            else 999,
            row["term"].lower(),
        )
    )
    return ordered


def build_report(
    enriched_rows: list[dict[str, str]],
    current_rows: list[dict[str, str]],
    output_pdf: Path,
    preview_dir: Path,
) -> int:
    document = LayoutDocument(
        "Blind and VI-First Accessibility Strings",
        "Session View workflow report",
    )
    document.title_page(generated_on_label())

    document.section_title("Palette Model")
    document.paragraph(
        "The report assumes a single palette entry point such as the backquote key. Once engaged, the "
        "musician stays inside a stable keyboard vocabulary: top-level letters choose a workflow lane, "
        "and modifiers change detail level rather than meaning. That consistency matters for muscle memory."
    )
    document.table(
        ["Modifier pattern", "Recommended behavior"],
        modifier_rows(),
        [126.0, CONTENT_WIDTH - 126.0],
        body_size=8.7,
        body_leading=11.3,
        header_size=8.8,
    )

    document.section_title("Workflow Lanes")
    document.paragraph(
        "The eight lanes below are ordered by practical music-making flow for blind and VI users: "
        "orientation first, then discovery, then live state, then recording safety, then deeper control."
    )
    document.table(
        ["Lane", "Workflow", "Primary question", "Items", "Core examples"],
        workflow_summary_rows(enriched_rows),
        [44.0, 118.0, 176.0, 42.0, CONTENT_WIDTH - 44.0 - 118.0 - 176.0 - 42.0],
        body_size=8.0,
        body_leading=10.4,
        header_size=8.5,
    )

    for workflow in WORKFLOWS:
        rows = workflow_section_rows(enriched_rows, workflow.id)
        sample_core = [row["accessible_label"] for row in rows if row["priority_tier"] == "core"][:6]
        document.section_title(workflow.title)
        document.paragraph(workflow.rationale)
        document.bullets(
            [
                f"Primary question: {workflow.question}",
                f"Default lane: {workflow.lane}",
                f"Blind / VI value: {workflow.blind_value}",
                "Modifier rule: Shift expands, Control speaks raw values, Option enables monitoring within the same lane.",
                f"High-value strings: {', '.join(sample_core).lower()}",
            ],
            bullet_indent=16,
        )

    document.section_title("Critical Findings")
    document.bullets(
        [
            "Deterministic voice access is a feature, not a compromise. For basic accessibility, inert and trustworthy output is often more just than a more intelligent but less predictable layer.",
            "The palette should prefer short first-pass utterances and offer expansion on demand. Speech overload is a real ergonomic cost.",
            "The current WHERE / WHAT / STATE model is a strong seed. It can expand into `n`, `c`, `p`, `r`, `t`, `m`, `d`, and `g` without losing clarity.",
            "Voice smoothness should be treated as a swappable rendering layer. A calmer premium TTS voice can improve comfort while remaining deterministic and local-first where possible.",
        ],
        bullet_indent=14,
    )

    document.section_title("Appendix A: Current Beta Exposed Terms")
    document.paragraph(
        "These rows capture the present beta surface: spoken tokens, state fields, and device-trigger terms "
        "already exposed by Clip Announcer."
    )
    appendix_a_rows = [
        [
            CURRENT_WORKFLOW_NAMES.get(row["workflow_group"], row["workflow_group"]),
            row["term"],
            row["current_surface"],
            row["notes"],
        ]
        for row in current_rows
    ]
    document.table(
        ["Workflow group", "Term", "Current surface", "Notes"],
        appendix_a_rows,
        [112.0, 110.0, 122.0, CONTENT_WIDTH - 112.0 - 110.0 - 122.0],
        body_size=7.9,
        body_leading=10.1,
        header_size=8.5,
    )

    document.section_title("Appendix B: Exhaustive Workflow-Sorted Accessibility Strings")
    document.paragraph(
        "Each row below is a readable Session View element. The report assigns it to one primary workflow lane, "
        "gives it a proposed spoken label, and sorts it by priority tier so the list stays usable."
    )
    appendix_b_rows = [
        [
            row["workflow_title"],
            row["priority_tier"].title(),
            row["palette_lane"],
            row["member_name"],
            row["accessible_label"],
            row["context_label"],
        ]
        for row in enriched_rows
    ]
    document.table(
        ["Workflow", "Tier", "Lane", "Source token", "Spoken label", "Context"],
        appendix_b_rows,
        [98.0, 38.0, 38.0, 78.0, 110.0, CONTENT_WIDTH - 98.0 - 38.0 - 38.0 - 78.0 - 110.0],
        body_font="F3",
        body_size=7.1,
        body_leading=9.0,
        header_size=8.0,
    )

    document.add_header_footer()
    writer = PDFWriter(document.pages)
    writer.write(output_pdf)

    preview_dir.mkdir(parents=True, exist_ok=True)
    for index, page in enumerate(document.pages, start=1):
        page_writer = PDFWriter([page])
        page_writer.write(preview_dir / f"page-{index:03d}.pdf")
    return len(document.pages)


def main() -> None:
    repo_root = Path(__file__).resolve().parents[1]
    master_csv = repo_root / "SESSION_VIEW_READABLE_UI_MASTER_LIST.csv"
    current_csv = repo_root / "SESSION_UI_TERMS_INVENTORY.csv"

    output_pdf = repo_root / "output" / "pdf" / "session_view_accessibility_workflow_report.pdf"
    output_master_csv = repo_root / "output" / "csv" / "session_view_accessibility_strings_by_workflow.csv"
    output_current_csv = repo_root / "output" / "csv" / "clip_announcer_current_beta_terms_by_workflow.csv"
    preview_dir = repo_root / "tmp" / "pdfs" / "session_view_accessibility_workflow_report_pages"

    master_rows = load_csv(master_csv)
    current_rows = current_inventory_rows(load_csv(current_csv))
    enriched_rows = enrich_master_rows(master_rows)

    write_csv(
        output_master_csv,
        enriched_rows,
        [
            "workflow_order",
            "workflow_id",
            "workflow_title",
            "palette_lane",
            "priority_tier",
            "layer",
            "object",
            "canonical_path",
            "member_type",
            "member_name",
            "accessible_label",
            "context_label",
            "blind_vi_purpose",
        ],
    )
    write_csv(
        output_current_csv,
        current_rows,
        ["workflow_group", "term", "kind", "current_surface", "notes"],
    )

    page_count = build_report(enriched_rows, current_rows, output_pdf, preview_dir)
    counts = Counter(row["workflow_title"] for row in enriched_rows)
    print(f"PDF: {output_pdf}")
    print(f"Pages: {page_count}")
    print(f"Workflow CSV: {output_master_csv}")
    print(f"Current beta CSV: {output_current_csv}")
    for workflow in WORKFLOWS:
        print(f"{workflow.title}: {counts[workflow.title]} items")


if __name__ == "__main__":
    main()
