import tkinter as tk
from tkinter import ttk, filedialog, messagebox, simpledialog
import subprocess
import tempfile
import os
import shutil
import zipfile
import webbrowser
import datetime

try:
    import psutil
except ImportError:
    psutil = None


APP_NAME = "Python Ultimate Desktop Toolkit"


class UltimateToolkitApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title(APP_NAME)
        self.geometry("1200x720")
        self.minsize(1000, 600)

        self.dark_mode = True

        self.configure_style()
        self.create_layout()
        self.show_dashboard()

    def configure_style(self):
        self.bg = "#111827" if self.dark_mode else "#f3f4f6"
        self.sidebar_bg = "#020617" if self.dark_mode else "#e5e7eb"
        self.card_bg = "#1f2937" if self.dark_mode else "#ffffff"
        self.text_color = "#f9fafb" if self.dark_mode else "#111827"
        self.sub_text = "#9ca3af" if self.dark_mode else "#4b5563"
        self.accent = "#38bdf8"

        self.configure(bg=self.bg)

    def create_layout(self):
        self.sidebar = tk.Frame(self, bg=self.sidebar_bg, width=230)
        self.sidebar.pack(side="left", fill="y")

        self.main_area = tk.Frame(self, bg=self.bg)
        self.main_area.pack(side="right", fill="both", expand=True)

        title = tk.Label(
            self.sidebar,
            text="ULTIMATE\nTOOLKIT",
            bg=self.sidebar_bg,
            fg=self.accent,
            font=("Arial", 20, "bold"),
            justify="left"
        )
        title.pack(pady=25, padx=20, anchor="w")

        buttons = [
            ("🏠 Dashboard", self.show_dashboard),
            ("📝 Python IDE", self.open_python_ide),
            ("📁 File Manager", self.open_file_manager),
            ("📊 Productivity", self.open_productivity),
            ("🛠 System Monitor", self.open_system_monitor),
            ("🎮 Game Center", self.open_game_center),
            ("🌐 Internet Tools", self.open_internet_tools),
            ("🎵 Multimedia", self.open_multimedia),
            ("📷 Camera Studio", self.open_camera_studio),
            ("🤖 AI Assistant", self.open_ai_assistant),
            ("🎨 Creative Tools", self.open_creative_tools),
        ]

        for text, command in buttons:
            btn = tk.Button(
                self.sidebar,
                text=text,
                command=command,
                bg=self.sidebar_bg,
                fg=self.text_color,
                activebackground=self.card_bg,
                activeforeground=self.accent,
                bd=0,
                font=("Arial", 12),
                anchor="w",
                padx=20,
                pady=10
            )
            btn.pack(fill="x", padx=8, pady=2)

        tk.Button(
            self.sidebar,
            text="🌙 Toggle Theme",
            command=self.toggle_theme,
            bg=self.accent,
            fg="#000000",
            bd=0,
            font=("Arial", 11, "bold"),
            pady=10
        ).pack(side="bottom", fill="x", padx=15, pady=20)

    def clear_main(self):
        for widget in self.main_area.winfo_children():
            widget.destroy()

    def page_title(self, title, subtitle=""):
        tk.Label(
            self.main_area,
            text=title,
            bg=self.bg,
            fg=self.text_color,
            font=("Arial", 24, "bold")
        ).pack(anchor="w", padx=30, pady=(25, 5))

        if subtitle:
            tk.Label(
                self.main_area,
                text=subtitle,
                bg=self.bg,
                fg=self.sub_text,
                font=("Arial", 12)
            ).pack(anchor="w", padx=30, pady=(0, 20))

    def create_card(self, parent, title, description, command):
        card = tk.Frame(parent, bg=self.card_bg, padx=18, pady=15)
        card.pack(fill="x", padx=30, pady=8)

        tk.Label(
            card,
            text=title,
            bg=self.card_bg,
            fg=self.text_color,
            font=("Arial", 15, "bold")
        ).pack(anchor="w")

        tk.Label(
            card,
            text=description,
            bg=self.card_bg,
            fg=self.sub_text,
            font=("Arial", 10),
            wraplength=750,
            justify="left"
        ).pack(anchor="w", pady=5)

        tk.Button(
            card,
            text="Open",
            command=command,
            bg=self.accent,
            fg="#000000",
            bd=0,
            padx=18,
            pady=6,
            font=("Arial", 10, "bold")
        ).pack(anchor="e")

    def show_dashboard(self):
        self.clear_main()
        self.page_title("Main Dashboard", "Operate all tools from this GUI dashboard.")

        container = tk.Frame(self.main_area, bg=self.bg)
        container.pack(fill="both", expand=True)

        self.create_card(
            container,
            "📝 Python IDE",
            "Write, open, save, and run Python code from inside the app.",
            self.open_python_ide
        )

        self.create_card(
            container,
            "📁 File Manager",
            "Browse folders, search files, create ZIP, and extract ZIP files.",
            self.open_file_manager
        )

        self.create_card(
            container,
            "📊 Productivity Suite",
            "Calculator, notes, to-do list, stopwatch, timer, and more.",
            self.open_productivity
        )

        self.create_card(
            container,
            "🛠 System Utilities",
            "View CPU, RAM, disk, battery, and basic system information.",
            self.open_system_monitor
        )

        self.create_card(
            container,
            "🎮 Game Center",
            "Snake, Tic Tac Toe, Hangman, 2048, Chess and more will be added here.",
            self.open_game_center
        )

    def toggle_theme(self):
        self.dark_mode = not self.dark_mode
        self.configure_style()
        self.sidebar.destroy()
        self.main_area.destroy()
        self.create_layout()
        self.show_dashboard()

    # ---------------- PYTHON IDE ----------------

    def open_python_ide(self):
        self.clear_main()
        self.page_title("Python IDE", "Code editor with run, open, save, and terminal output.")

        toolbar = tk.Frame(self.main_area, bg=self.bg)
        toolbar.pack(fill="x", padx=30)

        editor_frame = tk.Frame(self.main_area, bg=self.bg)
        editor_frame.pack(fill="both", expand=True, padx=30, pady=10)

        output_frame = tk.Frame(self.main_area, bg=self.bg)
        output_frame.pack(fill="both", expand=True, padx=30, pady=(0, 20))

        self.code_editor = tk.Text(
            editor_frame,
            bg="#0b1220",
            fg="#e5e7eb",
            insertbackground="white",
            font=("Consolas", 12),
            undo=True,
            wrap="none"
        )
        self.code_editor.pack(fill="both", expand=True)

        sample_code = """print("Hello from Ultimate Desktop Toolkit!")

for i in range(5):
    print("Number:", i)
"""
        self.code_editor.insert("1.0", sample_code)

        self.output_box = tk.Text(
            output_frame,
            bg="#020617",
            fg="#22c55e",
            insertbackground="white",
            font=("Consolas", 11),
            height=8
        )
        self.output_box.pack(fill="both", expand=True)

        tk.Button(toolbar, text="▶ Run", command=self.run_python_code, bg=self.accent, bd=0, padx=12, pady=6).pack(side="left", padx=5)
        tk.Button(toolbar, text="📂 Open", command=self.open_code_file, bg=self.card_bg, fg=self.text_color, bd=0, padx=12, pady=6).pack(side="left", padx=5)
        tk.Button(toolbar, text="💾 Save", command=self.save_code_file, bg=self.card_bg, fg=self.text_color, bd=0, padx=12, pady=6).pack(side="left", padx=5)
        tk.Button(toolbar, text="🔎 Find", command=self.find_text, bg=self.card_bg, fg=self.text_color, bd=0, padx=12, pady=6).pack(side="left", padx=5)

    def run_python_code(self):
        code = self.code_editor.get("1.0", "end")
        self.output_box.delete("1.0", "end")

        with tempfile.NamedTemporaryFile(delete=False, suffix=".py", mode="w", encoding="utf-8") as temp:
            temp.write(code)
            temp_path = temp.name

        try:
            result = subprocess.run(
                ["python", temp_path],
                capture_output=True,
                text=True,
                timeout=10
            )

            if result.stdout:
                self.output_box.insert("end", result.stdout)

            if result.stderr:
                self.output_box.insert("end", "\nERROR:\n" + result.stderr)

        except subprocess.TimeoutExpired:
            self.output_box.insert("end", "Error: Code took too long to run.")
        except Exception as e:
            self.output_box.insert("end", f"Error: {e}")
        finally:
            try:
                os.remove(temp_path)
            except Exception:
                pass

    def open_code_file(self):
        path = filedialog.askopenfilename(
            filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt"), ("All Files", "*.*")]
        )
        if path:
            with open(path, "r", encoding="utf-8") as file:
                self.code_editor.delete("1.0", "end")
                self.code_editor.insert("1.0", file.read())

    def save_code_file(self):
        path = filedialog.asksaveasfilename(
            defaultextension=".py",
            filetypes=[("Python Files", "*.py"), ("Text Files", "*.txt")]
        )
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.code_editor.get("1.0", "end"))
            messagebox.showinfo("Saved", "File saved successfully.")

    def find_text(self):
        word = simpledialog.askstring("Find", "Enter text to find:")
        if not word:
            return

        self.code_editor.tag_remove("found", "1.0", "end")
        start = "1.0"

        while True:
            pos = self.code_editor.search(word, start, stopindex="end")
            if not pos:
                break
            end = f"{pos}+{len(word)}c"
            self.code_editor.tag_add("found", pos, end)
            start = end

        self.code_editor.tag_config("found", background="yellow", foreground="black")

    # ---------------- FILE MANAGER ----------------

    def open_file_manager(self):
        self.clear_main()
        self.page_title("File Manager", "Browse, search, compress, and extract files.")

        top = tk.Frame(self.main_area, bg=self.bg)
        top.pack(fill="x", padx=30, pady=5)

        self.current_folder = os.getcwd()

        self.path_var = tk.StringVar(value=self.current_folder)
        path_entry = tk.Entry(top, textvariable=self.path_var, font=("Arial", 11))
        path_entry.pack(side="left", fill="x", expand=True, padx=5)

        tk.Button(top, text="Browse", command=self.choose_folder, bg=self.accent, bd=0, padx=12).pack(side="left", padx=5)
        tk.Button(top, text="Refresh", command=self.refresh_files, bg=self.card_bg, fg=self.text_color, bd=0, padx=12).pack(side="left", padx=5)
        tk.Button(top, text="ZIP Folder", command=self.zip_current_folder, bg=self.card_bg, fg=self.text_color, bd=0, padx=12).pack(side="left", padx=5)
        tk.Button(top, text="Extract ZIP", command=self.extract_zip, bg=self.card_bg, fg=self.text_color, bd=0, padx=12).pack(side="left", padx=5)

        self.file_list = tk.Listbox(
            self.main_area,
            bg="#0b1220",
            fg="#e5e7eb",
            font=("Consolas", 11)
        )
        self.file_list.pack(fill="both", expand=True, padx=30, pady=10)
        self.file_list.bind("<Double-Button-1>", self.open_selected_file)

        self.refresh_files()

    def choose_folder(self):
        folder = filedialog.askdirectory()
        if folder:
            self.current_folder = folder
            self.path_var.set(folder)
            self.refresh_files()

    def refresh_files(self):
        folder = self.path_var.get()
        self.file_list.delete(0, "end")

        try:
            items = os.listdir(folder)
            for item in items:
                full_path = os.path.join(folder, item)
                prefix = "📁 " if os.path.isdir(full_path) else "📄 "
                self.file_list.insert("end", prefix + item)
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def open_selected_file(self, event=None):
        selection = self.file_list.curselection()
        if not selection:
            return

        item = self.file_list.get(selection[0])[2:]
        path = os.path.join(self.path_var.get(), item)

        if os.path.isdir(path):
            self.current_folder = path
            self.path_var.set(path)
            self.refresh_files()
        else:
            try:
                os.startfile(path)
            except Exception:
                webbrowser.open(path)

    def zip_current_folder(self):
        folder = self.path_var.get()
        save_path = filedialog.asksaveasfilename(defaultextension=".zip")

        if not save_path:
            return

        try:
            with zipfile.ZipFile(save_path, "w", zipfile.ZIP_DEFLATED) as zipf:
                for root, dirs, files in os.walk(folder):
                    for file in files:
                        file_path = os.path.join(root, file)
                        arcname = os.path.relpath(file_path, folder)
                        zipf.write(file_path, arcname)

            messagebox.showinfo("Success", "ZIP created successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    def extract_zip(self):
        zip_path = filedialog.askopenfilename(filetypes=[("ZIP Files", "*.zip")])
        if not zip_path:
            return

        extract_to = filedialog.askdirectory()
        if not extract_to:
            return

        try:
            with zipfile.ZipFile(zip_path, "r") as zipf:
                zipf.extractall(extract_to)

            messagebox.showinfo("Success", "ZIP extracted successfully.")
        except Exception as e:
            messagebox.showerror("Error", str(e))

    # ---------------- PRODUCTIVITY ----------------

    def open_productivity(self):
        self.clear_main()
        self.page_title("Productivity Suite", "Calculator, notes, to-do list and daily tools.")

        container = tk.Frame(self.main_area, bg=self.bg)
        container.pack(fill="both", expand=True, padx=30, pady=10)

        left = tk.Frame(container, bg=self.card_bg, padx=15, pady=15)
        left.pack(side="left", fill="both", expand=True, padx=5)

        right = tk.Frame(container, bg=self.card_bg, padx=15, pady=15)
        right.pack(side="right", fill="both", expand=True, padx=5)

        tk.Label(left, text="Calculator", bg=self.card_bg, fg=self.text_color, font=("Arial", 16, "bold")).pack(anchor="w")
        self.calc_entry = tk.Entry(left, font=("Arial", 16))
        self.calc_entry.pack(fill="x", pady=10)

        tk.Button(left, text="Calculate", command=self.calculate, bg=self.accent, bd=0, pady=8).pack(fill="x")
        self.calc_result = tk.Label(left, text="", bg=self.card_bg, fg=self.accent, font=("Arial", 14))
        self.calc_result.pack(anchor="w", pady=10)

        tk.Label(right, text="Notes", bg=self.card_bg, fg=self.text_color, font=("Arial", 16, "bold")).pack(anchor="w")
        self.notes_box = tk.Text(right, bg="#0b1220", fg="#e5e7eb", font=("Arial", 11))
        self.notes_box.pack(fill="both", expand=True, pady=10)

        tk.Button(right, text="Save Notes", command=self.save_notes, bg=self.accent, bd=0, pady=8).pack(fill="x")

        todo_frame = tk.Frame(self.main_area, bg=self.card_bg, padx=15, pady=15)
        todo_frame.pack(fill="x", padx=30, pady=10)

        tk.Label(todo_frame, text="To-Do List", bg=self.card_bg, fg=self.text_color, font=("Arial", 16, "bold")).pack(anchor="w")

        self.todo_entry = tk.Entry(todo_frame, font=("Arial", 12))
        self.todo_entry.pack(side="left", fill="x", expand=True, padx=5, pady=10)

        tk.Button(todo_frame, text="Add Task", command=self.add_todo, bg=self.accent, bd=0, padx=12).pack(side="left", padx=5)

        self.todo_list = tk.Listbox(todo_frame, height=5, bg="#0b1220", fg="#e5e7eb")
        self.todo_list.pack(fill="x", padx=5, pady=5)

    def calculate(self):
        expression = self.calc_entry.get()
        try:
            result = eval(expression, {"__builtins__": {}})
            self.calc_result.config(text=f"Result: {result}")
        except Exception:
            self.calc_result.config(text="Invalid calculation")

    def save_notes(self):
        path = filedialog.asksaveasfilename(defaultextension=".txt")
        if path:
            with open(path, "w", encoding="utf-8") as file:
                file.write(self.notes_box.get("1.0", "end"))
            messagebox.showinfo("Saved", "Notes saved successfully.")

    def add_todo(self):
        task = self.todo_entry.get().strip()
        if task:
            self.todo_list.insert("end", "✅ " + task)
            self.todo_entry.delete(0, "end")

    # ---------------- SYSTEM MONITOR ----------------

    def open_system_monitor(self):
        self.clear_main()
        self.page_title("System Monitor", "CPU, RAM, disk, battery and system information.")

        self.system_box = tk.Text(
            self.main_area,
            bg="#0b1220",
            fg="#e5e7eb",
            font=("Consolas", 12)
        )
        self.system_box.pack(fill="both", expand=True, padx=30, pady=10)

        tk.Button(
            self.main_area,
            text="Refresh System Info",
            command=self.update_system_info,
            bg=self.accent,
            bd=0,
            pady=8
        ).pack(fill="x", padx=30, pady=10)

        self.update_system_info()

    def update_system_info(self):
        self.system_box.delete("1.0", "end")

        disk = shutil.disk_usage(os.getcwd())

        info = []
        info.append(f"Time: {datetime.datetime.now()}")
        info.append(f"Current Folder: {os.getcwd()}")
        info.append("")
        info.append(f"Disk Total: {disk.total // (1024 ** 3)} GB")
        info.append(f"Disk Used : {disk.used // (1024 ** 3)} GB")
        info.append(f"Disk Free : {disk.free // (1024 ** 3)} GB")

        if psutil:
            info.append("")
            info.append(f"CPU Usage: {psutil.cpu_percent()}%")
            info.append(f"RAM Usage: {psutil.virtual_memory().percent}%")

            battery = psutil.sensors_battery()
            if battery:
                info.append(f"Battery: {battery.percent}%")
            else:
                info.append("Battery: Not available")
        else:
            info.append("")
            info.append("For CPU/RAM/Battery info, install psutil:")
            info.append("pip install psutil")

        self.system_box.insert("end", "\n".join(info))

    # ---------------- PLACEHOLDER PAGES ----------------

    def placeholder_page(self, title, features):
        self.clear_main()
        self.page_title(title, "This section GUI is ready. Features can be added step by step.")

        box = tk.Frame(self.main_area, bg=self.card_bg, padx=25, pady=25)
        box.pack(fill="both", expand=True, padx=30, pady=10)

        for feature in features:
            tk.Label(
                box,
                text="✅ " + feature,
                bg=self.card_bg,
                fg=self.text_color,
                font=("Arial", 13),
                anchor="w"
            ).pack(fill="x", pady=4)

    def open_game_center(self):
        self.placeholder_page("Game Center", [
            "Snake",
            "Tic Tac Toe",
            "Hangman",
            "Rock Paper Scissors",
            "Pong",
            "Breakout",
            "Tetris",
            "2048",
            "Minesweeper",
            "Sudoku",
            "Chess",
            "Checkers",
            "Connect Four",
            "Memory Match",
            "Simon Says"
        ])

    def open_internet_tools(self):
        self.placeholder_page("Internet Toolkit", [
            "Mini Web Browser",
            "Speed Test",
            "QR Generator",
            "QR Scanner",
            "URL Shortener",
            "Download Manager"
        ])

    def open_multimedia(self):
        self.placeholder_page("Multimedia Player", [
            "MP3 Player",
            "Radio Streaming",
            "Video Player",
            "Playlist",
            "Equalizer",
            "Volume Control"
        ])

    def open_camera_studio(self):
        self.placeholder_page("Camera Studio", [
            "Webcam Preview",
            "Take Photo",
            "Record Video",
            "Face Detection",
            "QR Code Scanner",
            "Apply Filters"
        ])

    def open_ai_assistant(self):
        self.placeholder_page("AI Assistant", [
            "Chat Assistant",
            "Grammar Checker",
            "Text Summarizer",
            "Translator",
            "OCR Image to Text",
            "Voice Input",
            "Text-to-Speech"
        ])

    def open_creative_tools(self):
        self.placeholder_page("Creative Tools", [
            "Paint Application",
            "Image Editor",
            "Background Remover",
            "Color Picker",
            "Icon Generator",
            "PDF Creator",
            "Image to PDF"
        ])


if __name__ == "__main__":
    app = UltimateToolkitApp()
    app.mainloop()