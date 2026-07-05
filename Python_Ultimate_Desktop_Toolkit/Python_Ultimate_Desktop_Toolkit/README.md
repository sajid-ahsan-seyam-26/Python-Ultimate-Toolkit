# Python Ultimate Desktop Toolkit

A portfolio-ready all-in-one Python desktop application built with **PySide6**.

This project contains 10 main sections:

1. Python IDE
2. Camera Studio
3. Multimedia Player
4. Mini Game Center
5. Internet Toolkit
6. File Manager
7. AI Assistant
8. System Utilities
9. Productivity Suite
10. Creative Tools

It also includes:

- Dark/Light theme
- Plugin system
- Activity log
- Settings storage
- Modular folder structure
- Example plugin

> Note: Some advanced features need optional packages, internet, camera hardware, or API keys. The app handles missing packages safely and still runs.

---

## How to run

### 1. Create virtual environment

```bash
python -m venv .venv
```

### 2. Activate it

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

### 3. Install requirements

```bash
pip install -r requirements.txt
```

### 4. Run app

```bash
python main.py
```

---

## Recommended VS Code setup

Open the project folder in VS Code, then run:

```bash
python main.py
```

---

## Project Structure

```text
Python_Ultimate_Desktop_Toolkit/
│
├── main.py
├── requirements.txt
├── README.md
│
├── app/
│   ├── core/
│   ├── modules/
│   └── widgets/
│
├── assets/
├── database/
├── plugins/
├── themes/
├── logs/
└── user_data/
```

---

## Portfolio Description

**Python Ultimate Desktop Toolkit** is a modular all-in-one desktop application built using Python and PySide6. It includes a Python IDE, camera tools, multimedia player, mini games, file manager, system utilities, productivity tools, AI-style text tools, and creative tools. The project demonstrates GUI development, modular architecture, file handling, subprocess execution, optional hardware integration, plugin loading, local settings, and user-focused software design.
