# portelli-open

Personal open-source bench. Reusable tools, skills, and templates that don't belong inside a private workspace.

## What's here

### 🏌️ `skills/golf-trip-page/`

Generate a single-file, interactive HTML page for a multi-day golf trip from a JSON config. Tabs for itinerary, courses, an embedded map (Leaflet + OpenStreetMap), budget, and a live, editable leaderboard. Green-and-tan masters-aesthetic theme by default.

See [skills/golf-trip-page/SKILL.md](skills/golf-trip-page/SKILL.md) for usage.

## Repo layout

```
portelli-open/
├── README.md
├── LICENSE
├── requirements.txt           # shared python deps
├── .gitignore
└── skills/
    └── golf-trip-page/
        ├── SKILL.md           # how to use
        ├── scripts/
        │   └── generate.py    # JSON -> HTML
        ├── templates/
        │   └── trip.html.j2   # Jinja2 template
        └── examples/
            ├── pebble-beach-2026.json   # full sample config
            └── pebble-beach-2026.html   # rendered example
```

## Quick start

```powershell
# Install deps (one-time)
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt

# Render the example trip page
python skills/golf-trip-page/scripts/generate.py `
    --config skills/golf-trip-page/examples/pebble-beach-2026.json `
    --output out/pebble-beach-2026.html

# Open it
start out/pebble-beach-2026.html
```

## License

MIT. See [LICENSE](LICENSE).
