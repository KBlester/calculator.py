import tkinter as tk
from tkinter import ttk, messagebox
from calculator import Calculator, CalculatorError
from history import HistoryManager


class CalculatorUI:
    COLORS = {
        "bg": "#0a0a0a",
        "surface": "#141414",
        "surface_elevated": "#1e1e1e",
        "text_primary": "#ffffff",
        "text_secondary": "#a0a0a0",
        "accent": "#00ff88",
        "accent_hover": "#00e67a",
        "accent_active": "#00cc66",
        "operator": "#bb86fc",
        "operator_hover": "#a76ff2",
        "operator_active": "#9359dc",
        "danger": "#cf6679",
        "danger_hover": "#b95368",
        "warning": "#ffb74d",
        "warning_hover": "#ffa726",
        "border": "#2a2a2a",
    }

    BUTTONS = [
        [("C", "clear", "danger"), ("CE", "clear_entry", "danger"), ("⌫", "backspace", "warning"), ("÷", "divide", "operator")],
        [("7", "digit_7", "numeric"), ("8", "digit_8", "numeric"), ("9", "digit_9", "numeric"), ("×", "multiply", "operator")],
        [("4", "digit_4", "numeric"), ("5", "digit_5", "numeric"), ("6", "digit_6", "numeric"), ("-", "subtract", "operator")],
        [("1", "digit_1", "numeric"), ("2", "digit_2", "numeric"), ("3", "digit_3", "numeric"), ("+", "add", "operator")],
        [("+/-", "negate", "numeric"), ("0", "digit_0", "numeric"), (".", "decimal", "numeric"), ("=", "compute", "accent")],
        [("%", "percent", "scientific"), ("√", "sqrt", "scientific"), ("x²", "square", "scientific"), ("M+", "memory_add", "scientific")],
        [("MR", "memory_recall", "scientific"), ("M-", "memory_subtract", "scientific"), ("MC", "memory_clear", "scientific"), ("H", "history", "operator")],
    ]

    def __init__(self, root: tk.Tk):
        self.root = root
        self.calculator = Calculator()
        self.history_manager = HistoryManager()
        self.history_visible = False

        self._setup_window()
        self._setup_styles()
        self._build_ui()
        self._bind_keys()

    def _setup_window(self):
        self.root.title("Calculadora Neon")
        self.root.geometry("400x650")
        self.root.resizable(False, False)
        self.root.configure(bg=self.COLORS["bg"])

    def _setup_styles(self):
        style = ttk.Style()
        style.theme_use("clam")

    def _build_ui(self):
        self.container = tk.Frame(self.root, bg=self.COLORS["bg"])
        self.container.pack(fill="both", expand=True, padx=20, pady=20)

        self._build_display()
        self._build_buttons()
        self._build_history_panel()

    def _build_display(self):
        display_frame = tk.Frame(self.container, bg=self.COLORS["surface"], height=180)
        display_frame.pack(fill="x", pady=(0, 20))
        display_frame.pack_propagate(False)

        self.previous_label = tk.Label(
            display_frame,
            text="",
            bg=self.COLORS["surface"],
            fg=self.COLORS["text_secondary"],
            font=("Segoe UI", 12),
            anchor="e",
            justify="right",
        )
        self.previous_label.pack(fill="x", padx=20, pady=(25, 5))

        self.current_label = tk.Label(
            display_frame,
            text="0",
            bg=self.COLORS["surface"],
            fg=self.COLORS["text_primary"],
            font=("Segoe UI", 44, "bold"),
            anchor="e",
            justify="right",
        )
        self.current_label.pack(fill="x", padx=20, pady=(0, 20))

        self.memory_indicator = tk.Label(
            display_frame,
            text="",
            bg=self.COLORS["surface"],
            fg=self.COLORS["accent"],
            font=("Segoe UI", 10),
            anchor="w",
            justify="left",
        )
        self.memory_indicator.pack(fill="x", padx=20, pady=(0, 15))

    def _build_buttons(self):
        self.btn_frame = tk.Frame(self.container, bg=self.COLORS["bg"])
        self.btn_frame.pack(fill="both", expand=True)

        for i in range(4):
            self.btn_frame.grid_columnconfigure(i, weight=1)
        for i in range(len(self.BUTTONS)):
            self.btn_frame.grid_rowconfigure(i, weight=1)

        self.buttons = {}
        for row_idx, row in enumerate(self.BUTTONS):
            for col_idx, (label, action, btype) in enumerate(row):
                btn = self._create_button(label, action, btype)
                btn.grid(row=row_idx, column=col_idx, sticky="nsew", padx=4, pady=4)
                self.buttons[action] = btn

    def _create_button(self, label, action, btype):
        color_map = {
            "numeric": self.COLORS["surface_elevated"],
            "operator": self.COLORS["operator"],
            "accent": self.COLORS["accent"],
            "danger": self.COLORS["danger"],
            "warning": self.COLORS["warning"],
            "scientific": self.COLORS["surface_elevated"],
        }
        text_color_map = {
            "numeric": self.COLORS["text_primary"],
            "operator": self.COLORS["text_primary"],
            "accent": self.COLORS["bg"],
            "danger": self.COLORS["text_primary"],
            "warning": self.COLORS["bg"],
            "scientific": self.COLORS["text_secondary"],
        }

        bg = color_map.get(btype, self.COLORS["surface_elevated"])
        fg = text_color_map.get(btype, self.COLORS["text_primary"])

        btn = tk.Button(
            self.btn_frame,
            text=label,
            bg=bg,
            fg=fg,
            activebackground=self._lighten(bg),
            activeforeground=fg,
            font=("Segoe UI", 16, "bold"),
            bd=0,
            relief="flat",
            cursor="hand2",
        )

        btn.bind("<Enter>", lambda e: self._on_enter(btn, btype))
        btn.bind("<Leave>", lambda e: self._on_leave(btn, btype, bg, fg))

        command = lambda a=action: self._on_button(action)
        btn.configure(command=command)
        return btn

    def _lighten(self, hex_color):
        hex_color = hex_color.lstrip("#")
        rgb = tuple(int(hex_color[i:i+2], 16) for i in (0, 2, 4))
        lighter = tuple(min(255, int(c * 1.2)) for c in rgb)
        return f"#{lighter[0]:02x}{lighter[1]:02x}{lighter[2]:02x}"

    def _on_enter(self, btn, btype):
        hover_map = {
            "numeric": self.COLORS["surface_elevated"],
            "operator": self.COLORS["operator_hover"],
            "accent": self.COLORS["accent_hover"],
            "danger": self.COLORS["danger_hover"],
            "warning": self.COLORS["warning_hover"],
            "scientific": self.COLORS["surface_elevated"],
        }
        btn.configure(bg=hover_map.get(btype, btn.cget("bg")))

    def _on_leave(self, btn, btype, bg, fg):
        btn.configure(bg=bg, fg=fg)

    def _build_history_panel(self):
        self.history_panel = tk.Frame(self.root, bg=self.COLORS["surface"], width=300)
        self.history_panel.pack_propagate(False)

        hist_header = tk.Frame(self.history_panel, bg=self.COLORS["surface_elevated"])
        hist_header.pack(fill="x")

        tk.Label(
            hist_header,
            text="HISTÓRICO",
            bg=self.COLORS["surface_elevated"],
            fg=self.COLORS["accent"],
            font=("Segoe UI", 12, "bold"),
        ).pack(side="left", padx=15, pady=10)

        tk.Button(
            hist_header,
            text="×",
            bg=self.COLORS["surface_elevated"],
            fg=self.COLORS["text_secondary"],
            bd=0,
            font=("Segoe UI", 12),
            cursor="hand2",
            command=self.toggle_history,
        ).pack(side="right", padx=10, pady=5)

        self.history_list = tk.Listbox(
            self.history_panel,
            bg=self.COLORS["surface"],
            fg=self.COLORS["text_primary"],
            font=("Consolas", 12),
            bd=0,
            highlightthickness=0,
            selectbackground=self.COLORS["accent"],
            selectforeground=self.COLORS["bg"],
            activestyle="none",
        )
        self.history_list.pack(fill="both", expand=True, padx=10, pady=10)
        self.history_list.bind("<Double-Button-1>", self._on_history_double_click)

        btn_frame = tk.Frame(self.history_panel, bg=self.COLORS["surface"])
        btn_frame.pack(fill="x", padx=10, pady=(0, 10))

        tk.Button(
            btn_frame,
            text="Limpar",
            bg=self.COLORS["danger"],
            fg=self.COLORS["text_primary"],
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self._clear_history,
        ).pack(side="left", padx=5)

        tk.Button(
            btn_frame,
            text="Fechar",
            bg=self.COLORS["surface_elevated"],
            fg=self.COLORS["text_primary"],
            bd=0,
            font=("Segoe UI", 10, "bold"),
            cursor="hand2",
            command=self.toggle_history,
        ).pack(side="right", padx=5)

        self.history_panel.place_forget()

    def _bind_keys(self):
        self.root.bind("<Key>", self._on_key)
        self.root.bind("<Return>", lambda e: self._on_button("compute"))
        self.root.bind("<KP_Enter>", lambda e: self._on_button("compute"))
        self.root.bind("<Escape>", lambda e: self._on_button("clear"))
        self.root.bind("<BackSpace>", lambda e: self._on_button("backspace"))

    def _on_key(self, event):
        key = event.char
        if key in "0123456789":
            self._on_button(f"digit_{key}")
        elif key == ".":
            self._on_button("decimal")
        elif key == "+":
            self._on_button("add")
        elif key == "-":
            self._on_button("subtract")
        elif key == "*":
            self._on_button("multiply")
        elif key == "/":
            self._on_button("divide")
        elif key == "%":
            self._on_button("percent")

    def _on_button(self, action):
        try:
            if action.startswith("digit_"):
                digit = action.split("_")[1]
                self.calculator.input_digit(digit)
            elif action == "decimal":
                self.calculator.input_decimal()
            elif action == "clear":
                self.calculator.clear()
            elif action == "clear_entry":
                self.calculator.clear_entry()
            elif action == "backspace":
                self.calculator.backspace()
            elif action == "negate":
                self.calculator.negate()
            elif action == "percent":
                self.calculator.percent()
            elif action == "sqrt":
                self.calculator.square_root()
            elif action == "square":
                self.calculator.power(2)
            elif action == "add":
                self.calculator.set_operation("add")
            elif action == "subtract":
                self.calculator.set_operation("subtract")
            elif action == "multiply":
                self.calculator.set_operation("multiply")
            elif action == "divide":
                self.calculator.set_operation("divide")
            elif action == "compute":
                self.calculator.compute()
            elif action == "memory_add":
                self.calculator.memory_add()
            elif action == "memory_subtract":
                self.calculator.memory_subtract()
            elif action == "memory_recall":
                self.calculator.memory_recall()
            elif action == "memory_clear":
                self.calculator.memory_clear()
            elif action == "history":
                self.toggle_history()
            self._update_display()
        except CalculatorError as e:
            messagebox.showerror("Erro", str(e))
            self.calculator.clear()
            self._update_display()

    def _update_display(self):
        self.current_label.config(text=self.calculator.current)
        if self.calculator.previous is not None and self.calculator.operation:
            op_symbols = {"add": "+", "subtract": "-", "multiply": "×", "divide": "÷"}
            symbol = op_symbols.get(self.calculator.operation, self.calculator.operation)
            self.previous_label.config(text=f"{self.calculator.previous} {symbol}")
        else:
            self.previous_label.config(text="")

        if self.calculator.memory != 0:
            self.memory_indicator.config(text=f"M: {self.calculator.memory}")
        else:
            self.memory_indicator.config(text="")

    def toggle_history(self):
        self.history_visible = not self.history_visible
        if self.history_visible:
            self._refresh_history_list()
            self.history_panel.place(relx=1, rely=0, anchor="ne", width=300)
            self.root.geometry("700x650")
        else:
            self.history_panel.place_forget()
            self.root.geometry("400x650")

    def _refresh_history_list(self):
        self.history_list.delete(0, tk.END)
        for entry in reversed(self.calculator.get_history()):
            self.history_list.insert(tk.END, entry)

    def _on_history_double_click(self, event):
        selection = self.history_list.curselection()
        if selection:
            index = selection[0]
            entries = self.calculator.get_history()
            entry = entries[len(entries) - 1 - index]
            result = entry.split("=")[-1].strip()
            self.calculator.current = result
            self.calculator.should_reset = True
            self._update_display()

    def _clear_history(self):
        self.calculator.clear_history()
        self.history_list.delete(0, tk.END)
