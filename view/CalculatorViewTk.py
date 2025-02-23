import tkinter as tk
from tkinter import ttk, Menu, filedialog
from tkinter.ttk import Style
from components.functions import read_yaml
from view.SettingsWindowTk import SettingsWindow
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt
import numpy as np
import datetime



class CalculatorViewTk(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Kalkulator")
        self.geometry("1000x600")
        self.wm_minsize(800, 400)
        self.menu_visible = True
        self.current_font = read_yaml("font") or "Arial"
        self.font_color = read_yaml("fontColor") or "black"
        colorBackground = read_yaml("backgroundColor") or "white"
        self.memory = []

        s = Style()

        s.configure('My.TFrame', background=colorBackground)

        self.main_frame = ttk.Frame(self, style='My.TFrame')
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        self.create_menu()

        self.top_frame = ttk.Frame(self.main_frame, style='My.TFrame')
        self.top_frame.grid(row=0, column=0, columnspan=3, sticky="ew")

        self.menu_toggle_button = tk.Button(self.top_frame, text="≡", command=self.toggle_menu, fg=self.font_color)
        self.menu_toggle_button.pack(side=tk.LEFT, padx=5, pady=5)

        self.menu_frame = ttk.Frame(self.main_frame, width=150, style='My.TFrame')
        self.menu_frame.grid(row=1, column=0, sticky="ns")

        self.create_menu()
        self.create_menu_buttons()

        self.calc_frame = ttk.Frame(self.main_frame, style='My.TFrame')
        self.calc_frame.grid(row=1, column=1, sticky="nsew", padx=10, pady=10)


        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(1, weight=1)
        self.display = self.create_calculator_display()

        self.standard_calculator_buttons = [
            ('%', 1, 0), ('CE', 1, 1), ('C', 1, 2), ('<-', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3),
            ('RPN', 6, 0), ('MS', 6, 1), ('MR', 6, 2), ('M-', 6, 3),
            ('M+', 7, 0), ('MC', 7, 1)
        ]

        self.scientific_calculator_buttons = [
            ('sin', 1, 0), ('cos', 1, 1), ('tan', 1, 2), ('log', 1, 3),
            ('π', 2, 0), ('e', 2, 1), ('^', 2, 2), ('√', 2, 3),
            ('(', 3, 0), (')', 3, 1), ('%', 3, 2), ('CE', 3, 3),
            ('7', 4, 0), ('8', 4, 1), ('9', 4, 2), ('/', 4, 3),
            ('4', 5, 0), ('5', 5, 1), ('6', 5, 2), ('*', 5, 3),
            ('1', 6, 0), ('2', 6, 1), ('3', 6, 2), ('-', 6, 3),
            ('0', 7, 0), ('.', 7, 1), ('=', 7, 2), ('+', 7, 3),
            ('MS', 8, 0), ('MR', 8, 1), ('M-', 8, 2), ('M+', 8, 3),
            ('Mc', 9, 0)


        ]

        self.current_buttons = self.standard_calculator_buttons
        self.create_calculator_buttons()

        self.notebook = ttk.Notebook(self.main_frame, style='My.TFrame')
        self.notebook.grid(row=1, column=2, rowspan=2, sticky="nsew", padx=10, pady=10)

        self.history_tab = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.history_tab, text="Ostatnie wyrażenia")
        self.create_history_view(self.history_tab)

        self.memory_tab = ttk.Frame(self.notebook, style='My.TFrame')
        self.notebook.add(self.memory_tab, text="Pamięć")
        self.create_memory_view(self.memory_tab)

        self.main_frame.rowconfigure(1, weight=1)
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.columnconfigure(1, weight=2)
        self.main_frame.columnconfigure(2, weight=1)

    def create_memory_view(self, parent):
        self.memory_label = ttk.Label(parent, text="Zapisana wartość: None")
        self.memory_label.pack()

    def create_history_view(self, parent):
        self.history_label = ttk.Label(parent, text="Historia obliczeń", foreground=self.font_color)
        self.history_label.pack(anchor="n", pady=5)
        tree_frame = ttk.Frame(parent)
        tree_frame.pack(fill=tk.BOTH, expand=True, pady=5)

        self.history_tree = ttk.Treeview(
            tree_frame,
            columns=("Date", "Expression", "Result"),
            show="headings",
        )
        self.history_tree.heading("Date", text="Data")
        self.history_tree.heading("Expression", text="Wyrażenie")
        self.history_tree.heading("Result", text="Wynik")
        self.history_tree.column("Date", width=100, anchor="center")
        self.history_tree.column("Expression", width=200, anchor="center")
        self.history_tree.column("Result", width=100, anchor="center")

        scrollbar = ttk.Scrollbar(
            tree_frame, orient=tk.VERTICAL, command=self.history_tree.yview
        )
        self.history_tree.configure(yscrollcommand=scrollbar.set)

        self.history_tree.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        save_button_txt = tk.Button(
            parent, text="Zapisz historię", command=self.save_history_to_file, fg=self.font_color
        )
        save_button_txt.pack(pady=5)
        save_button_csv = tk.Button(
            parent, text="Zapisz historię do csv", command=self.save_history_to_csv, fg=self.font_color
        )
        save_button_csv.pack(pady=5)

        self.history_context_menu = tk.Menu(self, tearoff=0)
        self.history_context_menu.add_command(label="Skopiuj wyrażenie", command=self.copy_expression_from_history)
        self.history_tree.bind("<Button-3>", self.show_history_context_menu)

    def show_history_context_menu(self, event):
        row_id = self.history_tree.identify_row(event.y)

        if row_id:
            self.history_tree.selection_set(row_id)
            self.history_context_menu.post(event.x_root, event.y_root)
        else:
            tk.messagebox.showwarning("Brak wyboru", "Wybierz wiersz, aby skopiować wyrażenie.")

    def copy_expression_from_history(self):
        selected_item = self.history_tree.selection()
        if selected_item:
            expression = self.history_tree.item(selected_item, "values")[1]
            self.clipboard_clear()
            self.clipboard_append(expression)
            tk.messagebox.showinfo("Skopiowano", f"Skopiowano wyrażenie: {expression}")
        else:
            tk.messagebox.showwarning("Brak wyboru", "Wybierz wiersz, aby skopiować wyrażenie.")

    def add_to_history(self, expression, result):
        date_format = read_yaml("dateFormat") or "R-M-D G:i:s"
        formatted_date_format = self.format_date(date_format)

        try:
            current_time = datetime.datetime.now().strftime(formatted_date_format)
        except ValueError as e:
            print(f"Error formatting date with format '{formatted_date_format}': {e}")
            current_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        self.history_tree.insert("", 0, values=(current_time, expression, result))

    def format_date(self, date_format):
        mapping = {
            "R": "%Y",
            "M": "%m",
            "D": "%d",
            "G": "%H",
            "i": "%M",
            "S": "%S",
        }

        for key, value in sorted(mapping.items(), key=lambda x: -len(x[0])):
            date_format = date_format.replace(key, value)

        return date_format

    def save_history_to_file(self):
        file_path = filedialog.asksaveasfilename(
            defaultextension=".txt",
            filetypes=[("Pliki tekstowe", "*.txt"), ("Wszystkie pliki", "*.*")]
        )
        if not file_path:
            return

        try:
            with open(file_path, 'w', encoding='utf-8') as file:
                file.write("Historia obliczeń:\n")
                file.write("{:<20} {:<20} {:<20}\n".format("Data", "Wyrażenie", "Wynik"))
                file.write("=" * 60 + "\n")
                for item in self.history_tree.get_children():
                    date, expression, result = self.history_tree.item(item, "values")
                    file.write(f"{date:<20} {expression:<20} {result:<20}\n")
            tk.messagebox.showinfo("Zapisano", f"Historia została zapisana do pliku: {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Błąd zapisu", f"Wystąpił błąd podczas zapisywania pliku: {e}")

    def save_history_to_csv(self):
        """Zapisuje historię obliczeń do pliku CSV."""
        file_path = filedialog.asksaveasfilename(
            defaultextension=".csv",
            filetypes=[("Pliki CSV", "*.csv"), ("Wszystkie pliki", "*.*")]
        )
        if not file_path:
            return

        try:
            import csv
            with open(file_path, 'w', newline='', encoding='utf-8') as csvfile:
                writer = csv.writer(csvfile)
                writer.writerow(["Data", "Wyrażenie", "Wynik"])
                for item in self.history_tree.get_children():
                    writer.writerow(self.history_tree.item(item, "values"))
            tk.messagebox.showinfo("Zapisano", f"Historia została zapisana do pliku: {file_path}")
        except Exception as e:
            tk.messagebox.showerror("Błąd zapisu", f"Wystąpił błąd podczas zapisywania pliku: {e}")

    def create_menu(self):
        menu = Menu(self)
        self.config(menu=menu)

        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Plik', menu=filemenu)
        filemenu.add_command(label='Nowy')
        filemenu.add_command(label='Otwórz...')
        filemenu.add_separator()
        filemenu.add_command(label='Wyjście', command=self.quit)

        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Pomoc', menu=helpmenu)
        helpmenu.add_command(label='Informacje...')

        settings_menu = Menu(menu, tearoff=0)
        menu.add_cascade(label="Ustawienia", menu=settings_menu)
        settings_menu.add_command(label="Otwórz ustawienia", command=self.open_settings)

    def open_settings(self):
        SettingsWindow(self)

    def create_menu_buttons(self):
        self.menu_buttons = ["Standardowy", "Naukowy", "Tworzenie wykresów"]
        for btn_text in self.menu_buttons:
            btn = tk.Button(self.menu_frame, text=btn_text,fg=self.font_color , command=lambda t=btn_text: self.switch_mode(t))
            btn.pack(fill=tk.X, pady=2)

    def create_calculator_display(self):
        display = tk.Entry(self.calc_frame, font=(self.current_font, 20), justify="right")
        display.grid(row=0, column=0, columnspan=4, pady=10, sticky="nsew")
        return display


    def create_calculator_buttons(self):
        for widget in self.calc_frame.winfo_children():
            if isinstance(widget, tk.Button):
                widget.destroy()

        for row in range(6):
            self.calc_frame.grid_rowconfigure(row, weight=1)
        for col in range(4):
            self.calc_frame.grid_columnconfigure(col, weight=1)


        for (text, row, col) in self.current_buttons:
            button = tk.Button(
                self.calc_frame,
                text=text,
                font=(self.current_font, 18),
                fg=self.font_color,
                command=lambda t=text: self.on_button_click(t)
            )
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def switch_mode(self, mode):
        if mode == "Standardowy":
            self.current_buttons = self.standard_calculator_buttons
        elif mode == "Naukowy":
            self.current_buttons = self.scientific_calculator_buttons
        elif mode == "Tworzenie wykresów":
            self.open_plot_window()
            return

        self.create_calculator_buttons()

    def open_plot_window(self):
        PlotWindow(self)

    def on_button_click(self, button_text):
        self.display.insert(tk.END, button_text)

    def toggle_menu(self):
        if self.menu_visible:
            self.menu_frame.grid_remove()
        else:
            self.menu_frame.grid()
        self.menu_visible = not self.menu_visible


class PlotWindow(tk.Toplevel):
    def __init__(self, master):
        super().__init__(master)
        self.current_font = read_yaml("font") or "Arial"
        self.title("Tworzenie wykresów")
        self.geometry("800x600")

        self.background_color = read_yaml("backgroundColor") or "white"
        self.configure(bg=self.background_color)

        self.label = tk.Label(self, text="Podaj funkcję (np. sin(x), x**2):", bg=self.background_color)
        self.label.pack(pady=5)
        self.function_entry = tk.Entry(self, font=(self.current_font, 14))
        self.function_entry.pack(fill=tk.X, padx=10, pady=5)

        self.plot_button = tk.Button(self, text="Rysuj wykres", command=self.plot_graph)
        self.plot_button.pack(pady=5)

        self.close_button = tk.Button(self, text="Zamknij", command=self.destroy)
        self.close_button.pack(pady=5)

        self.plot_frame = ttk.Frame(self)
        self.plot_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.figure, self.ax = plt.subplots()
        self.figure.patch.set_facecolor(self.background_color)
        self.canvas = FigureCanvasTkAgg(self.figure, self.plot_frame)
        self.canvas_widget = self.canvas.get_tk_widget()
        self.canvas_widget.pack(fill=tk.BOTH, expand=True)

    def plot_graph(self):
        func_str = self.function_entry.get()
        if not func_str:
            return

        try:
            x = np.linspace(-10, 10, 500)
            y = eval(func_str,
                     {"x": x, "np": np, "sin": np.sin, "cos": np.cos, "tan": np.tan, "exp": np.exp, "log": np.log,
                      "sqrt": np.sqrt})

            self.ax.clear()
            self.ax.plot(x, y, label=f"y = {func_str}")
            self.ax.axhline(0, color="black", linewidth=0.5)
            self.ax.axvline(0, color="black", linewidth=0.5)
            self.ax.legend()
            self.ax.grid()
            self.canvas.draw()
        except Exception as e:
            self.ax.clear()
            self.ax.text(0.5, 0.5, f"Błąd: {e}", fontsize=12, ha="center", va="center", transform=self.ax.transAxes)
            self.canvas.draw()
