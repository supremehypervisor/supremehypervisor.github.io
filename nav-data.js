/**
 * nav-data.js — Orbital Index navigation manifest
 *
 * This file is read by index.html to build the sidebar and project cards.
 * You can edit it by hand, or regenerate it automatically by running:
 *
 *   python3 scripts/update-index.py      (recommended)
 *   bash scripts/update-index.sh         (bash alternative)
 *
 * STRUCTURE:
 *   NAV_DATA.sections is an object where each key is a folder name.
 *   Each section has a `label` (displayed in sidebar) and `items` array.
 *
 * ITEM FIELDS:
 *   title    (string)   — display name
 *   path     (string)   — relative URL to the project's index.html
 *   desc     (string)   — short description shown on cards (~120 chars)
 *   tag      (string)   — optional badge label e.g. "playable", "wip", "new"
 *   featured (boolean)  — if true, appears in the Featured section at top
 *
 * AUTO-GENERATED FIELDS (set by update script, safe to override):
 *   updated  (string)   — ISO date of last modification
 */

const NAV_DATA = {

  meta: {
    title:       "Orbital Index",
    description: "Games, stories, and demos",
    generated:   "2025-06-10",
  },

  sections: {

    demos: {
      label: "Demos",
      items: [
        {
          title:    "Example Game Demo",
          path:     "demos/example-game/index.html",
          desc:     "A placeholder demo. Replace this entry or run update-index.py to auto-detect projects.",
          tag:      "playable",
          featured: true,
          updated:  "2025-06-10",
        },
      ],
    },

    stories: {
      label: "Stories",
      items: [
        {
          title:    "Example Story",
          path:     "stories/example-story/index.html",
          desc:     "A placeholder story entry. Add your own HTML files in a subfolder and regenerate.",
          tag:      "fiction",
          featured: false,
          updated:  "2025-06-10",
        },
      ],
    },

    explanations: {
      label: "Explanations",
      items: [
        // Add explanation / devlog pages here, or let the update script find them.
      ],
    },

  },

};
