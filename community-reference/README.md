# Community Reference Pack

This folder is the shareable developer/reference bundle for the Max for Live community.

## Primary Files
- `SESSION_VIEW_UI_DEVELOPER_REFERENCE.pdf`
  Presentation-ready developer reference for Session View readable UI terms.
- `SESSION_VIEW_UI_DEVELOPER_REFERENCE.md`
  Editable source copy of the developer reference content.
- `SESSION_VIEW_READABLE_UI_MASTER_LIST.md`
  Exhaustive verified readable-object master list.
- `SESSION_VIEW_READABLE_UI_MASTER_LIST.csv`
  Machine-readable export of the exhaustive master list.

## What This Pack Covers
- Session View focus and selection surfaces
- Scene, track, clip slot, and clip-readable terms
- Mixer and parameter-readable terms relevant to Session workflows
- Practical LiveAPI entry points for accessibility and diagnostic tools

## Verification Basis
The contents are organized around the official Cycling '74 Live Object Model documentation.

## Regenerating The Presentation PDF
From the repository root:

```bash
python3 scripts/build_session_view_ui_reference_pdf.py
```

## Intended Use
This pack is meant to help developers quickly understand:
- what Session View can be read via LiveAPI
- which surfaces matter first for accessibility tools
- how to navigate from broad object paths to exact readable members
