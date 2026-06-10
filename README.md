# Orbital Index

A static host page for games, demos, stories, and explanations.
**Slate + orange orbital theme. Auto-indexing sidebar. GitHub Pages ready.**

---

## Setup

### 1. Deploy to GitHub Pages

1. Push this repo to GitHub
2. Go to **Settings → Pages → Source → Deploy from branch → main / (root)**
3. Done — `index.html` is your live splash page

### 2. Add a project

Create a subfolder under the right section folder with its own `index.html`:

```
demos/
  my-game/
    index.html       ← your game page
    game.js
    ...

stories/
  chapter-one/
    index.html       ← your story page

explanations/
  how-arcs-work/
    index.html
```

The subpage's `<title>` and `<meta>` tags feed into the auto-index:

```html
<title>My Game Title</title>
<meta name="description" content="A 20-floor roguelike with card-based combat." />
<meta name="tag"         content="playable" />
<meta name="featured"    content="true" />   <!-- pins to Featured section -->
```

### 3. Update the index

**Locally:**
```bash
python3 scripts/update-index.py
```

**Automatically:** The included GitHub Actions workflow (`.github/workflows/update-index.yml`) regenerates `nav-data.js` and commits it whenever you push a change to any `index.html`. No manual step needed.

---

## Folder structure

```
/
├── index.html                  ← splash + auto-index
├── nav-data.js                 ← generated manifest (sidebar + cards data)
├── demos/
│   └── your-game/index.html
├── stories/
│   └── your-story/index.html
├── explanations/
│   └── your-explanation/index.html
├── scripts/
│   ├── update-index.py         ← main update script
│   └── update-index.sh         ← bash wrapper
└── .github/
    └── workflows/
        └── update-index.yml    ← auto-update on push
```

---

## Theme

**Palette**

| Token | Hex | Role |
|-------|-----|------|
| Deep space | `#0F1117` | Page background |
| Panel slate | `#1A1F2E` | Sidebar, cards |
| Elevated | `#252B3B` | Hover surfaces |
| Border | `#2E3650` | Dividers |
| Orbital orange | `#FF6B2B` | Primary accent |
| Amber | `#FF9A5C` | Secondary / hover |

**Fonts:** [Orbitron](https://fonts.google.com/specimen/Orbitron) (display) + [Inter](https://fonts.google.com/specimen/Inter) (body)

---

## Sections

The update script groups projects by their parent folder name.
Known section names with nice labels:

| Folder | Label |
|--------|-------|
| `demos` | Demos |
| `stories` | Stories |
| `explanations` | Explanations |
| `experiments` | Experiments |
| `devlogs` | Devlogs |

Any other folder name is title-cased automatically.
