---
name: golf-trip-page
description: Generate a single-file, interactive HTML page for a multi-day golf trip from a JSON config. Tabs for itinerary, courses, embedded Leaflet map, budget, and a live editable leaderboard with handicap-adjusted net scoring. Masters-aesthetic green-and-tan theme by default.
---

# Golf Trip Page Skill

Turn a trip's JSON config into a self-contained HTML page you can ship to your group chat, email out, or open from a phone. No server, no build step. Just one file with embedded Leaflet for the map and inline JS for the live leaderboard.

## When to use

- Planning a buddies trip and you want one shareable link with everything in it
- You want a live leaderboard you can update from your phone during the round
- You want a course rundown with hero photos, logos, stats, and tee times
- You want a map of the courses + lodging + airport
- Budget transparency so the texts stop

## What it builds

A single `.html` file with five tabs:

| Tab | Contents |
|---|---|
| **Itinerary** | Day-by-day cards (2-up grid) with activity rows. Color-coded `food` / `travel` chips. Game-ideas section underneath. |
| **The Courses** | One card per course: hero photo + logo + tagline + stats (designer, par, yards, fee) + description + website/directions buttons. |
| **The Map** | Leaflet + OpenStreetMap, with custom-colored emoji pins and a sortable legend. |
| **Budget** | Greens-fees table + per-person summary tiles (with an "All-In" highlighted tile). |
| **Leaderboard** | Editable handicaps, per-round score inputs, auto-calculated gross/net totals, and a podium with gold/silver/bronze ranking. |

## How to use

### 1. Install deps (one-time)

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

### 2. Write a config

Start by copying [examples/pebble-beach-2026.json](examples/pebble-beach-2026.json) and editing for your trip. The schema is documented inline below.

### 3. Render

```powershell
python skills/golf-trip-page/scripts/generate.py `
    --config skills/golf-trip-page/examples/pebble-beach-2026.json `
    --output out/my-trip.html

start out/my-trip.html
```

## Config schema

Top-level shape:

```jsonc
{
  "meta":        { /* page title, hero, stats */ },
  "tabs":        [ /* optional, defaults to all 5 */ ],
  "theme":       { /* optional color overrides */ },
  "itinerary":   { /* days + games */ },
  "courses":     { /* course cards */ },
  "map":         { /* center, zoom, pins */ },
  "budget":      { /* table + summary tiles */ },
  "leaderboard": { /* players + handicaps */ }
}
```

Omit any of `itinerary`, `courses`, `map`, `budget`, `leaderboard` and that tab won't render.

### `meta`

```jsonc
{
  "title":       "Carmel · Pebble Beach",          // big hero title
  "subtitle":    "Some trips you plan...",         // italicized tagline (no quotes needed)
  "eyebrow":     "⛳ Summer 2026 · Carmel Calling", // small uppercase line above title
  "page_title":  "Carmel Boys Trip · June 24-27",  // browser tab title
  "footer_tag":  "⛳ Hit 'em straight, boys. ⛳",
  "footer_note": "Generated June 6, 2026 · Last updated by Sam",
  "stats": [
    { "label": "Dates",    "value": "June 24-27, 2026" },
    { "label": "Rounds",   "value": "5" },
    { "label": "The Crew", "value": "Sam · Marcus · Hopps · Jay" }
  ]
}
```

### `itinerary`

```jsonc
{
  "subtitle": "5 rounds. 4 days. Zero excuses.",
  "days": [
    {
      "name": "Wednesday · June 24",
      "tag":  "Arrival",
      "activities": [
        { "time": "ALL DAY", "type": "travel", "name": "Crew arrives", "note": "Whenever you land." },
        { "time": "EVENING", "type": "food",   "name": "Brewery",      "note": "Stock the house." }
      ]
    }
  ],
  "games": {
    "subtitle": "Bring your handicap, bring your wallet.",
    "cards": [
      { "name": "🐺 Wolf",       "desc": "Rotating partners each hole..." },
      { "name": "📊 Stableford", "desc": "Points per hole..." }
    ]
  }
}
```

`activity.type` controls chip color: omit for default fairway-green, `"food"` for red, `"travel"` for muted gray.

### `courses`

```jsonc
{
  "subtitle": "From the oldest course in the west to a top-10 in America.",
  "items": [
    {
      "id":                 "del-monte",                 // used as leaderboard column key
      "name":               "Del Monte Golf Course",
      "tagline":            "Oldest course west of the Mississippi (est. 1897)",
      "day_tag":            "Thursday · 8:40 AM",
      "hero_image":         "https://...jpg",            // big banner photo
      "logo_image":         "https://...png",            // optional small logo (top-right of hero)
      "logo_alt":           "Del Monte logo",
      "fallback_gradient":  ["#4a7c2e", "#2d5016"],      // shown if hero_image fails to load
      "stats": [
        { "label": "Designer", "value": "Charles Maud" },
        { "label": "Par",      "value": "72" },
        { "label": "Yards",    "value": "6,365" },
        { "label": "Green Fee","value": "$75pp" }
      ],
      "description":        "A walk through history...",
      "website":            "https://www.pebblebeach.com/golf/del-monte-golf-course/",
      "directions":         "https://www.google.com/maps/search/Del+Monte+Golf+Course",
      "par":                72,                          // used for leaderboard "to par" calc
      "scorecard_label":    "Del Monte"                  // short label for scorecard column header
    }
  ]
}
```

**Image sources that work well:**
- Course websites (right-click hero banner → copy image address)
- GolfPass / Golf Digest CDN URLs
- Wikimedia Commons: `https://commons.wikimedia.org/wiki/Special:FilePath/<filename>?width=1600`
- Squarespace, Brightspot, etc.

**Logo sources:**
- Official course website (look for `/images/logo.png` or similar)
- `https://www.google.com/s2/favicons?sz=128&domain=<course.com>` (quick fallback)

### `map`

```jsonc
{
  "subtitle": "All 5 courses plus the lodging.",
  "center":   [36.605, -121.91],
  "zoom":     12,
  "pins": [
    {
      "name":   "Portelli Beach House",
      "lat":    36.5511,
      "lng":    -121.9302,
      "color":  "#c89b3c",
      "label":  "13th & Scenic, Carmel",
      "icon":   "🏠",
      "legend": "<strong>Portelli Beach House</strong> — 13th & Scenic, Carmel"
    }
  ]
}
```

`icon` accepts any emoji; renders inside the colored circle. `legend` accepts HTML (used in the legend list below the map).

### `budget`

```jsonc
{
  "title":    "The Damage",
  "subtitle": "Greens fees only.",
  "table": {
    "columns": ["Course", "Day", "Per Person", "Total"],
    "rows": [
      { "course": "Del Monte", "day": "Thu AM", "per_person": "$75",  "total": "$300" },
      { "course": "Spyglass",  "day": "Fri PM", "per_person": "$320", "total": "$1,280" }
    ],
    "total": {
      "course": "Greens Fees Total", "day": "5 rounds",
      "per_person": "$798", "total": "$3,192"
    }
  },
  "summary": {
    "title": "Per Person Snapshot",
    "tiles": [
      { "value": "~$800",   "label": "Greens Fees" },
      { "value": "~$250",   "label": "Food & Drinks (est.)" },
      { "value": "$125",    "label": "Rental Car Split", "label_subtext": "($500 SUV ÷ 4)" },
      { "value": "~$1,175", "label": "All-In Estimate", "highlight": true }
    ]
  }
}
```

`highlight: true` renders the tile with dark-green background as the visual anchor.

### `leaderboard`

```jsonc
{
  "subtitle": "Updates live. Net scores use your handicap. Don't sandbag.",
  "champion_title": "Trip Champion Leaderboard",
  "players": [
    { "id": "sam",    "name": "Sam",    "default_handicap": 14 },
    { "id": "marcus", "name": "Marcus", "default_handicap": 0 }
  ]
}
```

Scorecard columns are auto-derived from `courses.items[]` (each course becomes one input column). Pars for the "to-par" calc come from each course's `par` field.

### `theme` (optional)

Override any color. Defaults are the masters-y green-and-tan:

```jsonc
{
  "fairway":       "#2d5016",
  "fairway_deep":  "#1a3009",
  "fairway_light": "#4a7c2e",
  "sand":          "#d4b88a",
  "sand_light":    "#f5e8d0",
  "cream":         "#faf5ea",
  "paper":         "#fffdf7",
  "ink":           "#1a2e0a",
  "ink_soft":      "#3d4a32",
  "rough":         "#6b8e4e",
  "flag_red":      "#b8412c",
  "gold":          "#c89b3c"
}
```

## Tips

- **Image loading**: hero photos use the URL with a gradient fallback. If you get a broken image, the gradient still looks good while you swap the URL.
- **Mobile**: the page is responsive. Day grid stacks to 1 column under 900px, budget grid stacks under 768px.
- **No build step**: rendered file is fully self-contained except for Leaflet CDN + the image URLs you reference. Works offline if you self-host the images.
- **Reuse across trips**: keep a folder of JSON configs per trip. Re-render anytime you tweak.

## Example

See [examples/pebble-beach-2026.json](examples/pebble-beach-2026.json) and the rendered [examples/pebble-beach-2026.html](examples/pebble-beach-2026.html).
