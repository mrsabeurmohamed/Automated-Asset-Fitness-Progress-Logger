# AUTOMATED FITNESS PROGRESS LOGGER & ANALYTICS

#### Video Demo: <https://youtu.be/hgIwCZUNA0M>
---

## 🏋️ Project Overview & Purpose
The **Automated Fitness Progress Logger** is a comprehensive tool designed to help athletes, coaches, and training enthusiasts parse inconsistent workout records and extract actionable metrics. Spreadsheets and mobile apps introduce heavy data-entry friction, which often leads to inconsistent tracking. By combining a **stylized CLI interface** with a **premium Glassmorphism Web Dashboard**, this project allows users to either input entries manually in the terminal, load/save text files, or manage their entire training history through a rich visual browser application.

The core math engine standardizes units (automatically converting pounds to kilograms), calculates session volume ($Sets \times Reps \times Weight$), and processes progressive overload data over time.

---

## ✨ Features

### 🖥️ 1. Stylized CLI Menu
- Designed with colored ANSI styling for clear options.
- Prompts for manual input or loads from a formatted log file (defaults to `workout_log.txt`).
- Safeguarded against encoding errors on Windows Command Prompt/PowerShell.

### 🌐 2. Premium Web Dashboard
- **Glassmorphic Design**: Futuristic semi-transparent cards, Outfit Google typography, and cyan-purple glowing gradients.
- **Analytics Charts**: Interactive double-axis line charts (volume in violet, weight in cyan) powered by Chart.js.
- **Real-Time Database Grid**: Search, filter, edit, or delete logs inline.
- **Bulk Import/Export**: Paste arbitrary training lists to bulk-import, or copy current records directly to your system clipboard using the **Export Copy** button.
- **Backend Sync**: Instantly saves Web UI updates back to your local `workout_log.txt` file.

---

## 📂 Codebase Structure & Files

- **`project.py`**: The backend and CLI execution core.
  - `main()`: Powers the terminal interface and runs options 1, 2, or starts the web server.
  - `parse_workout_line(line)`: Splits, trims, and validates text log rows.
  - `calculate_volume(sets, reps, weight, unit="kg")`: Calculates muscular tonnage in kg.
  - `format_summary(workout_data)`: Formats data into a structured CLI table.
  - `WorkoutHTTPRequestHandler`: Standard-library HTTP handler hosting the web dashboard and REST API.
  - `start_web_server()`: Starts the web server and opens the browser.
- **`web/index.html`**: A responsive, premium Single Page Application (SPA).
  - Handles the visual grid, stats cards, forms, and interactive Chart.js setup.
- **`workout_log.txt`**: The default text database. Pre-populated with realistic progressive overload logs (Back Squat, Bench Press, Pull-ups, etc.) to immediately populate analytics.
- **`test_project.py`**: Automated unit tests for validation.
  - Uses `pytest` to test core logic (validating correct/incorrect inputs, parsing margins, and mathematical tonnage calculations).
- **`requirements.txt`**: Defines project dependencies (e.g., `pytest`).

---

## 🚀 How to Run the Application

### 📋 Prerequisites
- Python 3.10 or newer.
- No external packages are required to run the application core or the web dashboard.
- Install `pytest` to run tests:
  ```bash
  pip install -r requirements.txt
  ```

### 1. Launching the Web Dashboard
Execute the project file:
```bash
python project.py
```
Type **`3`** and press **Enter**. The application will:
1. Fire up a lightweight HTTP server on `http://localhost:8000`.
2. Automatically launch your default web browser to display the interactive dashboard.
3. Access files locally to load and write workout records.
*To exit the server, press `Ctrl+C` in your terminal.*

### 2. Running in Terminal-Only Mode
Execute `python project.py` and choose:
- **`1`**: Key in a workout line manually (e.g., `2026-06-27, Back Squat, 4, 8, 100`).
- **`2`**: Load and print a summary table from a text file.

### 3. Running Unit Tests
Validate the backend's resilience using `pytest`:
```bash
pytest test_project.py
```

---

## 🧠 Architectural Design Decisions

1. **Self-Contained Local Web Server**: By utilizing Python's native `http.server` library, the application starts in seconds without requiring modern web frameworks (like Node.js, Flask, or FastAPI). This makes the project highly portable and grading-friendly.
2. **Text File as Single Source of Truth**: The Web Dashboard and CLI both interact with `workout_log.txt`. Standardizing the text format ensures that modifications done on the web UI sync immediately to disk, allowing the CLI to load them.
3. **Double-Axis Chart.js Visualization**: Standardizing all calculations to kilograms while displaying session volume and working weights on separate axes allows athletes to monitor progressive overload trends effectively.
