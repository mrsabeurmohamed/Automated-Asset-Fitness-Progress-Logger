# VIDEO DEMO PRESENTATION SCRIPT

This script is designed for a **2-3 minute video demonstration** of your final project. Follow the visual prompts and read the spoken dialogue naturally.

---

## ⏱️ Video Overview & Timeline
- **0:00 - 0:30**: Introduction & Purpose
- **0:30 - 1:00**: Terminal CLI Mode Demo (Options 1 & 2)
- **1:00 - 2:00**: Web Dashboard Mode Demo (Option 3, Stats, Chart, Live Sync, Export)
- **2:00 - 2:30**: Code Architecture, Automated Testing & Outro

---

## 🎙️ Step-by-Step Script

### Part 1: Introduction (0:00 - 0:30)
* **[VISUAL]**: Show the project main screen on terminal or the README file, with your web camera on (optional).
* **[TALKING]**:
  > *"Hello everyone! My name is **[Your Name]**, and today I am excited to demonstrate my final project for CS50's Introduction to Programming with Python: the **Automated Fitness Progress Logger and Analytics Dashboard**.*
  >
  > *This application solves a major problem for athletes: the friction of logging workouts. It standardizes raw textual workout entries into clean datasets, calculates progressive overload, and visualizes progress through both a clean command-line interface and a premium, responsive web dashboard."*

---

### Part 2: Terminal Mode Demo (0:30 - 1:00)
* **[VISUAL]**: Open your terminal and run `python project.py`. Show the colored CLI menu.
* **[TALKING]**:
  > *"Let's start the script. As you can see, we are presented with a styled terminal menu showing three options. First, let's select Option 1 to enter a workout line manually.*
  >
  > *[Type `1` and press Enter]*
  >
  > *I will input a date, exercise name, sets, reps, and weight, separated by commas. For example: `2026-06-27, Bench Press, 4, 8, 85`.*
  >
  > *[Type `2026-06-27, Bench Press, 4, 8, 85` and press Enter]*
  >
  > *The program parses the entry, calculates a total volume of 2720 kilograms for this movement, and displays a clean, formatted summary table.*
  >
  > *Next, we can run Option 2 to process an entire workout log file, which parses historical text logs in batch."*

---

### Part 3: Web Dashboard Mode Demo (1:00 - 2:00)
* **[VISUAL]**: Run `python project.py` again, select Option `3`. Show the terminal printing the success logs, and watch the browser open `http://localhost:8000` automatically.
* **[TALKING]**:
  > *"Now, let's look at the main feature: Option 3, which launches our Visual Web Dashboard.*
  >
  > *[Type `3` and press Enter. Let the browser open]*
  >
  > *The python script starts a lightweight web server in the background and automatically opens this premium Glassmorphism UI in my browser. No external frameworks or pip libraries are needed to host this!*
  >
  > *At the top, we have real-time statistics automatically parsed from our local `workout_log.txt` file, displaying total training volume, logged sets, and our top exercise.*
  >
  > *On the right, we have an interactive Chart.js line graph showing progressive overload. We can select different exercises from the dropdown, like Back Squat or Deadlift, to visualize our session volume and working weights over time.*
  >
  > *On the left, we can add new workouts or paste raw text lists to bulk import. At the bottom, we have an interactive database table. We can search for exercises, edit any entry inline to change sets or reps, delete logs, and click **Sync to File** to save updates directly back to our local text database.*
  >
  > *We also have an **Export Copy** button that copies our formatted logs to the clipboard with visual toast feedback."*

---

### Part 4: Testing & Conclusion (2:00 - 2:30)
* **[VISUAL]**: Switch back to the terminal. Run `pytest test_project.py`. Show the 7 tests passing.
* **[TALKING]**:
  > *"Under the hood, the project is structured to separate concern. Core logic functions like parsing and volume calculations are isolated to allow robust unit testing.*
  >
  > *Let's run our test suite using pytest.*
  >
  > *[Type `pytest test_project.py` and run it]*
  >
  > *All seven tests pass successfully, validating date boundaries, negative weights, and volume conversions.*
  >
  > *Thank you for watching the demo of the Automated Fitness Progress Logger. This was CS50!"*

---

## 💡 Recording Tips:
1. **Resolution**: Record your screen at `1080p` (1920x1080) for clear readability.
2. **Audio**: Use a headset microphone in a quiet room to ensure clear voice output.
3. **Pacing**: Speak at a steady, calm pace. Take short pauses between transitions.
4. **Tooling**: You can use free software like **OBS Studio** or browser extensions like **Loom** to record.
