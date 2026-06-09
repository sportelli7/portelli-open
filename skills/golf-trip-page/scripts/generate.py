"""Generate a single-file golf trip HTML page from a JSON config.

Usage:
    python generate.py --config path/to/trip.json --output path/to/trip.html

The config schema is documented in ../SKILL.md and exemplified by
../examples/pebble-beach-2026.json.
"""

from __future__ import annotations

import argparse
import json
import sys
from pathlib import Path

from jinja2 import Environment, FileSystemLoader, ChainableUndefined

DEFAULT_THEME = {
    "fairway": "#2d5016",
    "fairway_deep": "#1a3009",
    "fairway_light": "#4a7c2e",
    "sand": "#d4b88a",
    "sand_light": "#f5e8d0",
    "cream": "#faf5ea",
    "paper": "#fffdf7",
    "ink": "#1a2e0a",
    "ink_soft": "#3d4a32",
    "rough": "#6b8e4e",
    "flag_red": "#b8412c",
    "gold": "#c89b3c",
}

DEFAULT_TABS = [
    {"id": "itinerary", "label": "Itinerary"},
    {"id": "courses", "label": "The Courses"},
    {"id": "map", "label": "The Map"},
    {"id": "budget", "label": "Budget"},
    {"id": "leaderboard", "label": "Leaderboard"},
]


def _merge_theme(user_theme: dict | None) -> dict:
    theme = dict(DEFAULT_THEME)
    if user_theme:
        for key, value in user_theme.items():
            if key in theme:
                theme[key] = value
    return theme


def _slugify(value: str) -> str:
    out = []
    for ch in value.lower():
        if ch.isalnum():
            out.append(ch)
        elif ch in (" ", "-", "_"):
            out.append("")
    return "".join(out) or "course"


def _normalize(config: dict) -> dict:
    """Fill in derived/default fields the template expects."""
    config.setdefault("meta", {})
    meta = config["meta"]
    meta.setdefault("page_title", meta.get("title", "Golf Trip"))
    meta.setdefault("eyebrow", "")
    meta.setdefault("subtitle", "")
    meta.setdefault("stats", [])
    meta.setdefault("footer_tag", "⛳ Hit 'em straight. ⛳")
    meta.setdefault("footer_note", "")

    config["theme"] = _merge_theme(config.get("theme"))
    config.setdefault("tabs", DEFAULT_TABS)

    # Default fallback gradient for any course missing one
    if config.get("courses") and config["courses"].get("items"):
        for idx, c in enumerate(config["courses"]["items"]):
            c.setdefault("fallback_gradient", ["#4a7c2e", "#2d5016"])
            c.setdefault("scorecard_label", c.get("name", f"C{idx}"))
            c.setdefault("par", 72)
            # Derive a stable JS-safe scorecard key
            c.setdefault("id", _slugify(c["scorecard_label"]))

    return config


def render(config: dict, template_dir: Path) -> str:
    env = Environment(
        loader=FileSystemLoader(str(template_dir)),
        undefined=ChainableUndefined,
        keep_trailing_newline=True,
    )
    template = env.get_template("trip.html.j2")

    pins = []
    if config.get("map") and config["map"].get("pins"):
        pins = config["map"]["pins"]

    players = []
    course_keys: list[str] = []
    course_pars: list[int] = []
    if config.get("leaderboard"):
        players = config["leaderboard"].get("players", [])
        if config.get("courses") and config["courses"].get("items"):
            course_keys = [c["id"] for c in config["courses"]["items"]]
            course_pars = [int(c.get("par", 72)) for c in config["courses"]["items"]]

    return template.render(
        **config,
        map_pins_json=json.dumps(pins, ensure_ascii=False),
        players_json=json.dumps(
            [{"id": p["id"], "name": p["name"]} for p in players], ensure_ascii=False
        ),
        course_keys_json=json.dumps(course_keys, ensure_ascii=False),
        course_pars_json=json.dumps(course_pars),
    )


def main() -> int:
    parser = argparse.ArgumentParser(description="Render a golf trip HTML page from JSON.")
    parser.add_argument("--config", required=True, type=Path, help="Path to trip JSON config")
    parser.add_argument("--output", required=True, type=Path, help="Path to write the HTML")
    args = parser.parse_args()

    if not args.config.exists():
        print(f"ERROR: config not found: {args.config}", file=sys.stderr)
        return 1

    with args.config.open(encoding="utf-8") as fh:
        config = json.load(fh)

    config = _normalize(config)
    template_dir = Path(__file__).resolve().parent.parent / "templates"
    html = render(config, template_dir)

    args.output.parent.mkdir(parents=True, exist_ok=True)
    args.output.write_text(html, encoding="utf-8")
    print(f"Wrote {args.output} ({len(html):,} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
