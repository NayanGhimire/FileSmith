import os
import re
from pathlib import Path
from datetime import datetime
import tkinter as tk
from tkinter import filedialog, messagebox, ttk

# ───────────────────────────────────────────────
#  RENAME FUNCTIONS
# ───────────────────────────────────────────────

def add_prefix(filename, prefix):
    stem, ext = os.path.splitext(filename)
    return f"{prefix}{stem}{ext}"

def add_suffix(filename, suffix):
    stem, ext = os.path.splitext(filename)
    return f"{stem}{suffix}{ext}"

def sequential_rename(filename, index, base_name, padding):
    _, ext = os.path.splitext(filename)
    return f"{base_name}_{str(index).zfill(padding)}{ext}"

def date_rename(filename, mode):
    stem, ext = os.path.splitext(filename)
    date_str = datetime.now().strftime("%Y-%m-%d")
    if mode == "prepend":   return f"{date_str}_{stem}{ext}"
    elif mode == "append":  return f"{stem}_{date_str}{ext}"
    elif mode == "replace": return f"{date_str}{ext}"
    return filename

def replace_text(filename, find, replace, use_regex=False):
    stem, ext = os.path.splitext(filename)
    new_stem = re.sub(find, replace, stem) if use_regex else stem.replace(find, replace)
    return f"{new_stem}{ext}"

def get_files(folder, extensions, recursive):
    folder_path = Path(folder)
    pattern = "**/*" if recursive else "*"
    files = [f for f in folder_path.glob(pattern) if f.is_file()]
    if extensions:
        exts = {e.lower().lstrip(".") for e in extensions}
        files = [f for f in files if f.suffix.lower().lstrip(".") in exts]
    return sorted(files)

def apply_renames(renames, dry_run=False):
    success, skipped = 0, 0
    for original, new_name in renames:
        new_path = original.parent / new_name
        if new_path.exists():
            skipped += 1
            continue
        if not dry_run:
            original.rename(new_path)
        success += 1
    return success, skipped

# ───────────────────────────────────────────────
#  THEME
# ───────────────────────────────────────────────

BG       = "#0f0f0f"
BG2      = "#1a1a1a"
BG3      = "#242424"
BORDER   = "#2e2e2e"
ACCENT   = "#e8ff00"       # electric yellow
ACCENT2  = "#00d4aa"       # teal
RED      = "#ff4444"
FG       = "#e0e0e0"
FG2      = "#888888"
FONT     = ("Courier New", 10)
FONT_B   = ("Courier New", 10, "bold")
FONT_H   = ("Courier New", 14, "bold")
FONT_SM  = ("Courier New", 9)

# ───────────────────────────────────────────────
#  CUSTOM WIDGETS
# ───────────────────────────────────────────────

class DarkEntry(tk.Entry):
    def __init__(self, parent, **kw):
        super().__init__(parent,
            bg=BG3, fg=FG, insertbackground=ACCENT,
            relief="flat", bd=0,
            highlightthickness=1, highlightbackground=BORDER, highlightcolor=ACCENT,
            font=FONT, **kw)

class DarkButton(tk.Button):
    def __init__(self, parent, accent=False, danger=False, **kw):
        color = ACCENT if accent else (RED if danger else BG3)
        fg    = BG if accent else (FG if not danger else "#fff")
        self._color = color
        self._fg    = fg
        super().__init__(parent,
            bg=color, fg=fg, activebackground=ACCENT2, activeforeground=BG,
            relief="flat", bd=0, cursor="hand2",
            font=FONT_B, padx=12, pady=6, **kw)
        self.bind("<Enter>", lambda e: self.config(bg=ACCENT2, fg=BG))
        self.bind("<Leave>", lambda e: self.config(bg=self._color, fg=self._fg))

class DarkCheckbutton(tk.Checkbutton):
    def __init__(self, parent, **kw):
        super().__init__(parent,
            bg=BG2, fg=FG, selectcolor=BG3,
            activebackground=BG2, activeforeground=ACCENT,
            font=FONT, relief="flat", bd=0, **kw)

class Section(tk.Frame):
    def __init__(self, parent, title, **kw):
        super().__init__(parent, bg=BG2, bd=0, highlightthickness=1,
                         highlightbackground=BORDER, **kw)
        header = tk.Frame(self, bg=BG3)
        header.pack(fill="x")
        tk.Label(header, text=f"  {title}", bg=BG3, fg=ACCENT,
                 font=FONT_B, anchor="w", pady=6).pack(fill="x")
        self.body = tk.Frame(self, bg=BG2)
        self.body.pack(fill="both", expand=True, padx=10, pady=8)

# ───────────────────────────────────────────────
#  MODE PANELS
# ───────────────────────────────────────────────

class ModePanel(tk.Frame):
    """Base class — each mode shows its own inputs."""
    def __init__(self, parent):
        super().__init__(parent, bg=BG2)
    def get_params(self):
        return {}

class PrefixPanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Prefix:", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,6))
        self.entry = DarkEntry(self, width=24)
        self.entry.pack(side="left")
        tk.Label(self, text="→  mypic.jpg  becomes  prefix_mypic.jpg", bg=BG2, fg=FG2, font=FONT_SM).pack(side="left", padx=12)
    def get_params(self): return {"prefix": self.entry.get().strip()}

class SuffixPanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Suffix:", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,6))
        self.entry = DarkEntry(self, width=24)
        self.entry.pack(side="left")
        tk.Label(self, text="→  mypic.jpg  becomes  mypic_suffix.jpg", bg=BG2, fg=FG2, font=FONT_SM).pack(side="left", padx=12)
    def get_params(self): return {"suffix": self.entry.get().strip()}

class SequentialPanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        for label, attr, default, w in [
            ("Base name:", "base", "file", 14),
            ("Start #:", "start", "1", 5),
            ("Padding:", "pad", "3", 4),
        ]:
            tk.Label(self, text=label, bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,4))
            e = DarkEntry(self, width=w)
            e.insert(0, default)
            e.pack(side="left", padx=(0,10))
            setattr(self, attr, e)
        tk.Label(self, text="→  file_001.jpg, file_002.jpg …", bg=BG2, fg=FG2, font=FONT_SM).pack(side="left", padx=8)
    def get_params(self):
        try: start = int(self.start.get())
        except: start = 1
        try: pad = int(self.pad.get())
        except: pad = 3
        return {"base": self.base.get().strip() or "file", "start": start, "pad": pad}

class DatePanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Position:", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,6))
        self.mode_var = tk.StringVar(value="prepend")
        for val, lbl in [("prepend","Prepend"), ("append","Append"), ("replace","Replace")]:
            tk.Radiobutton(self, text=lbl, variable=self.mode_var, value=val,
                bg=BG2, fg=FG, selectcolor=BG3, activebackground=BG2,
                activeforeground=ACCENT, font=FONT).pack(side="left", padx=6)
        tk.Label(self, text="→  2026-03-28_mypic.jpg", bg=BG2, fg=FG2, font=FONT_SM).pack(side="left", padx=12)
    def get_params(self): return {"date_mode": self.mode_var.get()}

class ReplacePanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Find:", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,4))
        self.find = DarkEntry(self, width=16)
        self.find.pack(side="left", padx=(0,10))
        tk.Label(self, text="Replace:", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,4))
        self.repl = DarkEntry(self, width=16)
        self.repl.pack(side="left", padx=(0,10))
        self.regex_var = tk.BooleanVar()
        DarkCheckbutton(self, text="Regex", variable=self.regex_var).pack(side="left")
    def get_params(self): return {"find": self.find.get(), "replace": self.repl.get(), "use_regex": self.regex_var.get()}

class QuickPanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        tk.Label(self, text="Name:", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,6))
        self.entry = DarkEntry(self, width=24)
        self.entry.pack(side="left")
        tk.Label(self, text="→  mypic_001.jpg, mypic_002.jpg …", bg=BG2, fg=FG2, font=FONT_SM).pack(side="left", padx=12)
    def get_params(self): return {"base": self.entry.get().strip() or "file"}

class PrefixSeqPanel(ModePanel):
    def __init__(self, parent):
        super().__init__(parent)
        for label, attr, default, w in [
            ("Prefix:", "prefix", "", 10),
            ("Base:", "base", "file", 10),
            ("Start:", "start", "1", 4),
            ("Pad:", "pad", "3", 3),
        ]:
            tk.Label(self, text=label, bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,3))
            e = DarkEntry(self, width=w)
            if default: e.insert(0, default)
            e.pack(side="left", padx=(0,8))
            setattr(self, attr, e)
    def get_params(self):
        try: start = int(self.start.get())
        except: start = 1
        try: pad = int(self.pad.get())
        except: pad = 3
        return {"prefix": self.prefix.get().strip(), "base": self.base.get().strip() or "file", "start": start, "pad": pad}

# ───────────────────────────────────────────────
#  MAIN APP
# ───────────────────────────────────────────────

class FileSmith:
    MODES = [
        ("quick",      "⚡ Quick Rename",    QuickPanel),
        ("prefix",     "← Add Prefix",       PrefixPanel),
        ("suffix",     "→ Add Suffix",       SuffixPanel),
        ("sequential", "## Sequential",      SequentialPanel),
        ("date",       "📅 Date Stamp",      DatePanel),
        ("replace",    "↔ Find & Replace",   ReplacePanel),
        ("prefix+seq", "← + ## Combined",    PrefixSeqPanel),
    ]

    def __init__(self, root):
        self.root = root
        self.root.title("FileSmith — Bulk File Renamer")
        self.root.configure(bg=BG)
        self.root.geometry("960x720")
        self.root.resizable(True, True)
        self.files = []
        self.current_panel = None
        self._build_ui()

    def _build_ui(self):
        # ── Header ──
        header = tk.Frame(self.root, bg=BG, pady=0)
        header.pack(fill="x", padx=0)
        hline = tk.Frame(header, bg=BG3, height=1)
        hline.pack(fill="x")
        inner = tk.Frame(header, bg=BG)
        inner.pack(fill="x", padx=20, pady=14)
        tk.Label(inner, text="FILESMITH", bg=BG, fg=ACCENT,
                 font=("Courier New", 22, "bold")).pack(side="left")
        tk.Label(inner, text="  //  bulk file renamer", bg=BG, fg=FG2,
                 font=("Courier New", 11)).pack(side="left", pady=4)
        self.status_label = tk.Label(inner, text="no files loaded", bg=BG, fg=FG2, font=FONT_SM)
        self.status_label.pack(side="right")

        # ── Folder section ──
        s1 = Section(self.root, "01 / TARGET FOLDER")
        s1.pack(fill="x", padx=16, pady=(10, 6))
        row = tk.Frame(s1.body, bg=BG2)
        row.pack(fill="x")
        self.folder_entry = DarkEntry(row, width=60)
        self.folder_entry.pack(side="left", ipady=4, fill="x", expand=True)
        DarkButton(row, text="Browse", command=self._browse).pack(side="left", padx=(8,0))
        DarkButton(row, text="Load Files", accent=True, command=self._load_files).pack(side="left", padx=(6,0))

        # Filter row
        frow = tk.Frame(s1.body, bg=BG2)
        frow.pack(fill="x", pady=(8,0))
        tk.Label(frow, text="Extensions (e.g. jpg,png — blank = all):", bg=BG2, fg=FG2, font=FONT).pack(side="left", padx=(0,8))
        self.ext_entry = DarkEntry(frow, width=22)
        self.ext_entry.pack(side="left")
        self.recursive_var = tk.BooleanVar()
        DarkCheckbutton(frow, text="Include subfolders", variable=self.recursive_var).pack(side="left", padx=16)

        # ── Mode section ──
        s2 = Section(self.root, "02 / RENAME MODE")
        s2.pack(fill="x", padx=16, pady=6)

        # Mode selector tabs
        tab_row = tk.Frame(s2.body, bg=BG2)
        tab_row.pack(fill="x", pady=(0, 10))
        self.mode_var = tk.StringVar(value="quick")
        self._tab_buttons = {}
        for key, label, _ in self.MODES:
            b = tk.Button(tab_row, text=label, bg=BG3, fg=FG2,
                          relief="flat", bd=0, font=FONT_SM, padx=10, pady=5,
                          cursor="hand2",
                          command=lambda k=key: self._select_mode(k))
            b.pack(side="left", padx=(0,2))
            self._tab_buttons[key] = b

        # Panel container
        self.panel_frame = tk.Frame(s2.body, bg=BG2)
        self.panel_frame.pack(fill="x")
        self._select_mode("quick")

        # ── Preview section ──
        s3 = Section(self.root, "03 / PREVIEW")
        s3.pack(fill="both", expand=True, padx=16, pady=6)

        # Toolbar
        tbar = tk.Frame(s3.body, bg=BG2)
        tbar.pack(fill="x", pady=(0,8))
        DarkButton(tbar, text="▶  Preview", command=self._preview).pack(side="left")
        DarkButton(tbar, text="✔  Apply Renames", accent=True, command=self._apply).pack(side="left", padx=8)
        DarkButton(tbar, text="✖  Clear", danger=True, command=self._clear).pack(side="left")
        self.count_label = tk.Label(tbar, text="", bg=BG2, fg=FG2, font=FONT_SM)
        self.count_label.pack(side="right")

        # Preview text box
        pf = tk.Frame(s3.body, bg=BORDER, bd=0)
        pf.pack(fill="both", expand=True)
        self.preview_box = tk.Text(pf, bg=BG, fg=FG, font=FONT_SM,
                                   relief="flat", bd=0, padx=12, pady=10,
                                   insertbackground=ACCENT, wrap="none",
                                   state="disabled")
        sb = tk.Scrollbar(pf, command=self.preview_box.yview, bg=BG2,
                          troughcolor=BG3, relief="flat")
        self.preview_box.configure(yscrollcommand=sb.set)
        sb.pack(side="right", fill="y")
        self.preview_box.pack(fill="both", expand=True)

        # Tag colours
        self.preview_box.tag_config("head",    foreground=ACCENT,  font=("Courier New", 9, "bold"))
        self.preview_box.tag_config("old",     foreground=FG2)
        self.preview_box.tag_config("arrow",   foreground=ACCENT2)
        self.preview_box.tag_config("new",     foreground=FG)
        self.preview_box.tag_config("ok",      foreground=ACCENT2)
        self.preview_box.tag_config("warn",    foreground=RED)
        self.preview_box.tag_config("divider", foreground=BORDER)

        # ── Footer ──
        foot = tk.Frame(self.root, bg=BG3, pady=6)
        foot.pack(fill="x", side="bottom")
        tk.Label(foot, text="FileSmith v2.0  //  made with Broddy's chaos energy",
                 bg=BG3, fg=FG2, font=FONT_SM).pack()

    def _select_mode(self, key):
        self.mode_var.set(key)
        # Update tab highlight
        for k, b in self._tab_buttons.items():
            if k == key:
                b.config(bg=ACCENT, fg=BG)
            else:
                b.config(bg=BG3, fg=FG2)
        # Swap panel
        if self.current_panel:
            self.current_panel.destroy()
        _, _, PanelClass = next(m for m in self.MODES if m[0] == key)
        self.current_panel = PanelClass(self.panel_frame)
        self.current_panel.pack(fill="x")

    def _browse(self):
        folder = filedialog.askdirectory()
        if folder:
            self.folder_entry.delete(0, tk.END)
            self.folder_entry.insert(0, folder)

    def _load_files(self):
        folder = self.folder_entry.get().strip()
        if not os.path.isdir(folder):
            messagebox.showerror("FileSmith", "Folder not found.")
            return
        ext_raw = self.ext_entry.get().strip().lower()
        extensions = None if (not ext_raw or ext_raw == "all") else [e.strip() for e in ext_raw.split(",")]
        self.files = get_files(folder, extensions, self.recursive_var.get())
        n = len(self.files)
        self.status_label.config(text=f"{n} file{'s' if n != 1 else ''} loaded", fg=ACCENT2)
        self._write_preview(f"  {n} file(s) loaded from:\n  {folder}\n", [("ok", f"  {n} file(s) loaded from:\n")])

    def _build_renames(self):
        if not self.files:
            return []
        mode   = self.mode_var.get()
        params = self.current_panel.get_params()
        renames = []

        if mode == "quick":
            base = params["base"]
            renames = [(f, sequential_rename(f.name, i+1, base, 3)) for i, f in enumerate(self.files)]
        elif mode == "prefix":
            renames = [(f, add_prefix(f.name, params["prefix"])) for f in self.files]
        elif mode == "suffix":
            renames = [(f, add_suffix(f.name, params["suffix"])) for f in self.files]
        elif mode == "sequential":
            renames = [(f, sequential_rename(f.name, params["start"]+i, params["base"], params["pad"])) for i, f in enumerate(self.files)]
        elif mode == "date":
            renames = [(f, date_rename(f.name, params["date_mode"])) for f in self.files]
        elif mode == "replace":
            renames = [(f, replace_text(f.name, params["find"], params["replace"], params["use_regex"])) for f in self.files]
        elif mode == "prefix+seq":
            renames = [(f, add_prefix(sequential_rename(f.name, params["start"]+i, params["base"], params["pad"]), params["prefix"])) for i, f in enumerate(self.files)]

        return [(f, n) for f, n in renames if f.name != n]

    def _write_preview(self, text, tag_spans=None):
        self.preview_box.config(state="normal")
        self.preview_box.delete(1.0, tk.END)
        self.preview_box.insert(tk.END, text)
        self.preview_box.config(state="disabled")

    def _preview(self):
        renames = self._build_renames()
        self.preview_box.config(state="normal")
        self.preview_box.delete(1.0, tk.END)

        if not renames:
            self.preview_box.insert(tk.END, "  No files would be renamed.\n", "warn")
            self.count_label.config(text="")
        else:
            self.preview_box.insert(tk.END,
                f"  {'ORIGINAL FILE':<45}   NEW NAME\n", "head")
            self.preview_box.insert(tk.END,
                "  " + "─"*75 + "\n", "divider")
            for f, n in renames:
                self.preview_box.insert(tk.END, f"  {f.name:<45}", "old")
                self.preview_box.insert(tk.END, "→  ", "arrow")
                self.preview_box.insert(tk.END, f"{n}\n", "new")
            self.preview_box.insert(tk.END, "\n  " + "─"*75 + "\n", "divider")
            self.preview_box.insert(tk.END, f"  {len(renames)} file(s) will be renamed\n", "ok")
            self.count_label.config(text=f"{len(renames)} to rename")

        self.preview_box.config(state="disabled")

    def _apply(self):
        renames = self._build_renames()
        if not renames:
            messagebox.showinfo("FileSmith", "Nothing to rename.")
            return
        confirm = messagebox.askyesno("FileSmith",
            f"Rename {len(renames)} file(s)?\nThis cannot be undone.")
        if not confirm:
            return
        success, skipped = apply_renames(renames)
        messagebox.showinfo("FileSmith", f"✔ Renamed: {success}\n⚠ Skipped (name exists): {skipped}")
        self._load_files()
        self._preview()

    def _clear(self):
        self.preview_box.config(state="normal")
        self.preview_box.delete(1.0, tk.END)
        self.preview_box.config(state="disabled")
        self.files = []
        self.status_label.config(text="no files loaded", fg=FG2)
        self.count_label.config(text="")

# ───────────────────────────────────────────────
#  ENTRY POINT
# ───────────────────────────────────────────────

if __name__ == "__main__":
    root = tk.Tk()
    app = FileSmith(root)
    root.mainloop()