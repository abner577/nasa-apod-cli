# NASA APOD CLI

A developer-facing, interactive command-line application that wraps the [NASA Astronomy Picture of the Day (APOD) API](https://api.nasa.gov/) and adds local tooling for:

- requesting APOD data (today, date-based, or random batch),
- logging APOD metadata to JSONL and CSV,
- generating local HTML viewer pages for each APOD entry,
- optionally downloading APOD media files to your global **Downloads** folder,
- optionally setting APOD images as your desktop wallpaper (Windows, macOS, Linux, and WSL-aware flows).

---

## Table of Contents

- [Project Overview](#project-overview)
- [Feature Summary](#feature-summary)
- [Project Structure](#project-structure)
- [Prerequisites](#prerequisites)
- [Setup](#setup)
  - [1) Verify Python is installed](#1-verify-python-is-installed)
  - [2) Verify pip is installed](#2-verify-pip-is-installed)
  - [3) Verify Git is installed](#3-verify-git-is-installed)
  - [4) Clone the repository](#4-clone-the-repository)
  - [5) Create and activate a virtual environment](#5-create-and-activate-a-virtual-environment)
  - [6) Install dependencies](#6-install-dependencies)
  - [7) Configure environment variables](#7-configure-environment-variables)
  - [8) Run the CLI](#8-run-the-cli)
- [OS-Specific Setup Notes](#os-specific-setup-notes)
  - [Windows](#windows)
  - [macOS](#macos)
  - [Linux](#linux)
- [Configuration](#configuration)
  - [Environment Variables (`.env`)](#environment-variables-env)
  - [Runtime User Settings (`data/settings.jsonl`)](#runtime-user-settings-datasettingsjsonl)
  - [How Auto-Save Works](#how-auto-save-works)
  - [How Auto-Wallpaper Works](#how-auto-wallpaper-works)
- [How to Use the CLI](#how-to-use-the-cli)
  - [Startup and Main Menu](#startup-and-main-menu)
  - [NASA APOD Requests](#nasa-apod-requests)
  - [Log & File Tools](#log--file-tools)
  - [Preferences](#preferences)
  - [Global Commands (available from prompts)](#global-commands-available-from-prompts)
- [Output Files and Data](#output-files-and-data)
- [Troubleshooting](#troubleshooting)

---

## Project Overview

This project is a terminal application that sits on top of NASA's APOD API and provides a complete local workflow instead of just raw API calls.

When you request APOD data, the CLI:

1. calls the APOD API,
2. normalizes the response,
3. generates a local HTML viewer page for the entry,
4. logs the entry to JSONL and CSV (with duplicate-date protection),
5. optionally opens the result in your browser,
6. optionally downloads media locally,
7. optionally sets wallpaper for image APODs.

It is designed for developers who want a usable CLI wrapper with persistent logs and local OS integrations.

---

## Feature Summary

- Interactive menus for:
  - Today's APOD
  - APOD by date
  - Random APOD batch (1-20)
- Persistent logs:
  - `data/output.jsonl`
  - `data/output.csv`
- APOD-local HTML viewer generation in `data/viewer/`.
- Log exploration utilities:
  - first N, last N, all
  - delete by date
  - most recent date
  - oldest date
  - clear logs
  - count entries
- Settings controls for:
  - auto-open APOD in browser,
  - auto-set wallpaper,
  - auto-save APOD media files.
- Global command shortcuts like `--help`, `--settings`, `--auto-save`, `--auto-wallpaper <path>`, etc.

---

## Project Structure

| Path | Purpose |
|---|---|
| `src/main.py` | Program entry point and top-level menu routing. |
| `src/startup/` | Startup UI, Rich console themes, startup checks, and menu renderers. |
| `src/nasa/` | APOD API request logic and APOD date input/validation helpers. |
| `src/storage/` | JSONL/CSV logging, read/delete/list utilities, and local-path update logic. |
| `src/utils/` | CLI command parser, browser helpers, APOD media download, viewer generation, data formatting. |
| `src/wallpaper/` | Cross-platform wallpaper services (Windows/macOS/Linux/WSL-aware). |
| `src/config.py` | Paths, constants, APOD date bounds, and README URL constant. |
| `src/user_settings.py` | Creation, reading, normalization, and update of runtime settings. |
| `data/` | Runtime-generated logs/settings/viewer files (`output.jsonl`, `output.csv`, `settings.jsonl`, `viewer/`). |
| `.env.example` | Template for `NASA_API_KEY` and `BASE_URL`. |

---

## Prerequisites

- Python 3.10+ recommended
- `pip`
- Git
- Internet access (for NASA API requests and media downloads)

---

## Setup

### 1) Verify Python is installed

```bash
python --version
```

If your system maps Python 3 to `python3`, run:

```bash
python3 --version
```

### 2) Verify pip is installed

```bash
pip --version
```

If needed:

```bash
python -m pip --version
```

### 3) Verify Git is installed

```bash
git --version
```

### 4) Clone the repository

```bash
git clone <your-repo-url>
cd nasa-apod-cli
```

### 5) Create and activate a virtual environment

Create:

```bash
python -m venv .venv
```

Activate:

- **Windows (PowerShell):**
  ```powershell
  .\.venv\Scripts\Activate.ps1
  ```
- **Windows (Command Prompt):**
  ```bat
  .venv\Scripts\activate.bat
  ```
- **macOS/Linux (bash/zsh):**
  ```bash
  source .venv/bin/activate
  ```

### 6) Install dependencies

```bash
pip install -r requirements.txt
```

### 7) Configure environment variables

Create `.env` in the repository root and add:

```env
NASA_API_KEY="YOUR_API_KEY_HERE"
BASE_URL="https://api.nasa.gov/planetary/apod"
```

Notes:

- You can use `DEMO_KEY` for light usage, but a personal NASA key is recommended.
- `BASE_URL` should remain the APOD endpoint unless you intentionally proxy it.

### 8) Run the CLI

```bash
python src/main.py
```

On first run, startup checks create missing runtime files under `data/` automatically.

---

## OS-Specific Setup Notes

### Windows

1. Install Python from python.org and make sure **"Add Python to PATH"** is enabled.
2. Confirm tools:
   ```powershell
   python --version
   pip --version
   git --version
   ```
3. Create venv and activate in PowerShell:
   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```
4. If script execution is blocked, run once in your user scope:
   ```powershell
   Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
   ```
5. Install dependencies, configure `.env`, and run:
   ```powershell
   pip install -r requirements.txt
   python src/main.py
   ```

Wallpaper uses native Windows API flow; auto-saved APOD media goes to your global `Downloads` folder.

### macOS

1. Verify Apple-provided tools or install Homebrew equivalents.
2. Confirm tools:
   ```bash
   python3 --version
   pip3 --version
   git --version
   ```
3. Create and activate venv:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   python src/main.py
   ```

Wallpaper integration uses AppleScript (`osascript`) and supports image APODs.

### Linux

1. Ensure Python, pip, and Git are installed from your distro package manager.
2. Confirm tools:
   ```bash
   python3 --version
   pip3 --version
   git --version
   ```
3. Create and activate venv:
   ```bash
   python3 -m venv .venv
   source .venv/bin/activate
   ```
4. Install dependencies and run:
   ```bash
   pip install -r requirements.txt
   python src/main.py
   ```

On WSL, browser and Downloads-path handling is WSL-aware so files/opened viewer URIs map to Windows-friendly paths where possible.

---

## Configuration

### Environment Variables (`.env`)

The app loads `.env` during NASA client initialization.

| Variable | Required | Description |
|---|---|---|
| `NASA_API_KEY` | Yes | NASA APOD API key used in each request. |
| `BASE_URL` | Yes | APOD endpoint base URL (default: `https://api.nasa.gov/planetary/apod`). |
| `RESOLUTION_TYPE` | Optional | Wallpaper mode hint used by WSL wallpaper tooling (`fit` default). |

### Runtime User Settings (`data/settings.jsonl`)

The app stores user behavior flags in `data/settings.jsonl` and auto-creates this file at startup.

Default values:

- `automatically_redirect = yes`
- `automatically_set_wallpaper = no`
- `automatically_save_apod_files = no`
- `launch_count = 0` (incremented per main menu cycle)

You can change settings from:

1. **Main Menu → Change Setting**, or
2. **Global commands** from any prompt:
   - `--auto-redirect`
   - `--auto-wallpaper`
   - `--auto-save`
   - `--settings`

Accepted command prefixes: `--`, `-`, and `/`.

### How Auto-Save Works

When `automatically_save_apod_files` is ON:

- the app attempts to download APOD media after a successful fetch,
- files are saved into your **global Downloads directory**,
- naming convention is `apod-YYYY-MM-DD.<ext>` (with `-1`, `-2`, etc. suffixes if needed),
- `local_file_path` is updated in both CSV and JSONL logs,
- existing date-matching files are reused/skipped to avoid duplicates.

For APOD videos hosted on YouTube, automatic file download is skipped gracefully.

### How Auto-Wallpaper Works

When `automatically_set_wallpaper` is ON:

- image APODs are reused/downloaded and set as wallpaper,
- video APODs are skipped (wallpaper update not attempted),
- platform-specific implementations are used:
  - Windows native API,
  - macOS AppleScript,
  - Linux desktop command flow,
  - WSL bridge to Windows wallpaper flow.

You can also set wallpaper manually from a local path:

```text
--auto-wallpaper <absolute-or-resolvable-image-path>
```

Supported manual image types include: `.jpg`, `.jpeg`, `.png`, `.bmp`, `.gif`, `.webp`, `.tif`, `.tiff`.

---

## How to Use the CLI

### Startup and Main Menu

At startup the app:

- renders startup art,
- checks/creates required runtime files,
- shows current setting status,
- opens an entry menu (`Get started` or `Quit`).

Main menu options:

1. **Make a NASA APOD Request**
2. **View/Manage saved logs**
3. **Change Setting**
4. **Goodbye**

### NASA APOD Requests

Inside **NASA APOD Requests**:

1. **Today's APOD**
2. **APOD by date**
3. **Random APODs**
4. **Return to Main Menu**

Notes:

- Date requests prompt `Year / Month / Day`.
- APOD availability starts at `1995-06-16`.
- Random batch supports **1 to 20** APODs per request.

### Log & File Tools

Inside **Log & File Tools**:

1. View first N entries
2. View last N entries
3. View all entries
4. Delete entry by date
5. Show most recent entry (by date)
6. Show oldest entry (by date)
7. Clear logs (CSV + JSONL)
8. Count logged entries
9. Return to Main Menu

Log clear also removes generated APOD viewer HTML files under `data/viewer/`.

### Preferences

Inside **Preferences**:

1. View settings
2. Change auto-redirect setting
3. Change auto-set-wallpaper setting
4. Change auto-save-apod-files setting
5. Return to Main Menu

### Global Commands (available from prompts)

These can be entered from menu prompts:

- `--help` → show global command help
- `--readme` → open README in browser
- `--quit` / `q` / `quit` → exit app
- `--settings` → display current settings
- `--auto-redirect` → toggle redirect behavior
- `--auto-wallpaper` → toggle wallpaper behavior
- `--auto-wallpaper <filepath>` → set wallpaper from a local file path
- `--auto-save` → toggle media auto-save behavior

Supported prefixes: `--command`, `-command`, `/command`.

---

## Output Files and Data

Runtime files are kept under `data/`:

- `output.jsonl`: one JSON object per logged APOD
- `output.csv`: tabular log with columns:
  - `date`, `title`, `url`, `explanation`, `logged_at`, `local_file_path`
- `settings.jsonl`: user preference flags and launch count
- `viewer/apod-YYYY-MM-DD.html`: generated local APOD viewer pages

The stored `url` field points to the generated local APOD viewer file URI so opening logged entries takes you to the local viewer page.

---

## Troubleshooting

- **API errors (403/404):** verify `NASA_API_KEY` and `BASE_URL` in `.env`.
- **No auto-download for some videos:** YouTube-hosted APOD videos are intentionally skipped.
- **Wallpaper not changing:** verify OS wallpaper permissions and use an image APOD (not video).
- **Browser launch issues in WSL:** ensure `wslview` is available or that `cmd.exe /c start` can be invoked.
- **Missing runtime files:** relaunch the app; startup checks recreate required files in `data/`.
