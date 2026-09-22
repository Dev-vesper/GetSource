<div align="center">

# Source Collector

Collect source files from selected folders and export them into a single Markdown document.

</div>

---

## Purpose

Source Collector is a PyQt desktop application that lets you browse your filesystem, pick folders, select files by hand or by extension, and export all selected sources into one Markdown file.

---

## Requirements

- Python 3.9+
- PyQt6 (version depends on your OS and hardware)
- pytest (only for running the tests)

---

## Setup

### 1. Clone the repository

```bash
git clone <repository-url>
cd GetSource
```

### 2. Create a virtual environment

```bash
python3 -m venv .venv
```

### 3. Activate the virtual environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows:

```bash
.venv\Scripts\activate
```

### 4. Install PyQt6

The PyQt6 version you install depends on your operating system and CPU. Newer builds require `SSE4.2` and `POPCNT`; if your CPU does not support them, install version `6.9.1` instead.

Standard install:

```bash
pip install "PyQt6>=6.5"
```

Fallback for older CPUs (no SSE4.2 / POPCNT):

```bash
pip install "PyQt6==6.9.1" "PyQt6-Qt6==6.9.1"
```

Install the remaining dependencies:

```bash
pip install -r requirements.txt
```

### 5. Run the application

```bash
python3 main.py
```

---

## Usage

1. Launch the app with `python3 main.py`.
2. Browse the filesystem tree on the left and select a folder.
3. Click **Add Folder** (or double-click the folder) to open the file picker.
4. Inside the picker:
   - Type extensions like `py, ml` and press Enter or **Select matching** to auto-check every matching file.
   - Or check files manually, use **Select all**, or **Clear selection**.
5. Press **OK** to add the selected files to the collection list.
6. Repeat for as many folders as you need.
7. Use **Remove Selected** or **Clear** to adjust the list.
8. Click **Export Markdown** and choose where to save the output `.md` file.

The exported Markdown contains one code block per file, with the file path as the language tag:

```src/main.py
<file content>
```

---

## Running Tests

```bash
pytest tests/
```
