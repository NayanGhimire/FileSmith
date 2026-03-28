# ⚙️ FileSmith — Bulk File Renamer

> A fast, dark-themed desktop app for bulk renaming any type of file — with live preview before you commit.

![Python](https://img.shields.io/badge/Python-3.10%2B-yellow?style=flat-square&logo=python)
![Tkinter](https://img.shields.io/badge/GUI-Tkinter-blue?style=flat-square)
![Platform](https://img.shields.io/badge/Platform-Windows%20%7C%20macOS%20%7C%20Linux-lightgrey?style=flat-square)
![License](https://img.shields.io/badge/License-MIT-green?style=flat-square)

---

## ✨ Features

| Mode | What it does | Example |
|------|-------------|---------|
| ⚡ Quick Rename | Type one name, files become `name_001`, `name_002`… | `mypic_001.jpg` |
| ← Add Prefix | Prepend text to every filename | `holiday_photo.jpg` |
| → Add Suffix | Append text before the extension | `photo_final.jpg` |
| `##` Sequential | Full control: base name, start number, padding | `doc_005.pdf` |
| 📅 Date Stamp | Prepend, append, or replace with today's date | `2026-03-28_photo.jpg` |
| ↔ Find & Replace | Replace any text in filenames — regex supported | `IMG_001` → `nepal_001` |
| ← + ## Combined | Prefix AND sequential numbering together | `trip_photo_001.jpg` |

![FileSmith Screenshot](screenshot.png)

**Other highlights:**
- 🔍 **Live preview** — see every rename before it happens
- 🗂️ **Extension filter** — target only `.jpg`, `.docx`, etc., or all files
- 🔁 **Recursive mode** — optionally include subfolders
- ⚠️ **Conflict protection** — skips files that would overwrite existing ones
- 🖤 **Dark industrial UI** — easy on the eyes during long sessions

---

## 📦 Requirements

- Python **3.10+**
- `tkinter` — comes bundled with Python on Windows and macOS

> On Linux, install tkinter separately if needed:
> ```bash
> sudo apt install python3-tk
> ```

No third-party packages required. Zero dependencies.

---

## 🚀 Installation & Running

### 1. Clone the repo

```bash
git clone https://github.com/yourusername/filesmith.git
cd filesmith
```

### 2. Run the app

```bash
python filesmith.py
```

That's it. No `pip install` needed.

---

## 🖥️ How to Use

### Step 1 — Select your folder

Click **Browse** to pick the folder containing your files, or paste the path directly into the field.

```
📁 C:\Users\Broddy\Pictures\Nepal Trip
```

Optionally filter by extension (e.g. `jpg,png`) — leave blank to include all file types.
Check **Include subfolders** if you want recursive renaming.

Click **Load Files** to scan the folder.

---

### Step 2 — Choose a rename mode

Click any mode tab at the top of the **Rename Mode** section:

#### ⚡ Quick Rename *(most common)*
Type a base name. Files get sequentially numbered from `001`.

```
Name: mypic
→ mypic_001.jpg
→ mypic_002.jpg
→ mypic_003.png
```

#### ← Add Prefix
```
Prefix: holiday_
→ holiday_photo.jpg
→ holiday_sunset.png
```

#### → Add Suffix
```
Suffix: _final
→ report_final.docx
→ budget_final.xlsx
```

#### `##` Sequential
Full control over the output format.
```
Base: photo  |  Start: 5  |  Padding: 4
→ photo_0005.jpg
→ photo_0006.jpg
```

#### 📅 Date Stamp
Stamps today's date onto filenames. Three position options:

| Option | Result |
|--------|--------|
| Prepend | `2026-03-28_photo.jpg` |
| Append  | `photo_2026-03-28.jpg` |
| Replace | `2026-03-28.jpg` |

#### ↔ Find & Replace
```
Find: IMG_    Replace: trip_
→ IMG_001.jpg  becomes  trip_001.jpg
```
Enable **Regex** for pattern-based matching (e.g. `IMG_\d+` → `photo_\1`).

#### ← + ## Combined
Adds both a prefix AND sequential numbering.
```
Prefix: nepal_  |  Base: photo  |  Start: 1  |  Pad: 3
→ nepal_photo_001.jpg
→ nepal_photo_002.jpg
```

---

### Step 3 — Preview

Click **▶ Preview** to see exactly what will change:

```
ORIGINAL FILE                                 NEW NAME
───────────────────────────────────────────────────────────
  IMG_4521.jpg                            →  mypic_001.jpg
  IMG_4522.jpg                            →  mypic_002.jpg
  IMG_4523.png                            →  mypic_003.png

  3 file(s) will be renamed
```

Nothing is changed yet.

---

### Step 4 — Apply

Click **✔ Apply Renames** and confirm. FileSmith renames all files and shows a summary:

```
✔ Renamed: 3
⚠ Skipped (name exists): 0
```

The preview refreshes automatically with the updated filenames.

---

## 📁 Project Structure

```
filesmith/
│
├── filesmith.py       # Main app (GUI + logic, single file)
├── auto_renamer.py    # CLI / terminal version
└── README.md
```

---

## 🔧 Also Included: CLI Version

For terminal lovers or automation scripts, `auto_renamer.py` has all the same features in an interactive command-line interface.

```bash
python auto_renamer.py
```

Or use it non-interactively:

```bash
# Add prefix to all jpg files
python auto_renamer.py "C:/Photos" --ext jpg prefix "vacation_"

# Sequential rename with dry run (preview only)
python auto_renamer.py "C:/Photos" --dry-run seq --base photo --pad 3 --start 1

# Find and replace
python auto_renamer.py "C:/Photos" replace "IMG_" "trip_"
```

---

## ⚠️ Notes

- FileSmith **skips** any rename that would overwrite an existing file.
- There is **no undo** — use **Preview** before applying.
- Folders and hidden system files are ignored automatically.
- File extensions are always preserved (except in Date → Replace mode, intentionally).

---

## 📄 License

MIT License — free to use, modify, and distribute.

---

*Built by Broddy — Nepal 🇳🇵*