import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv
from tkinter.colorchooser import askcolor
from tkinter.scrolledtext import ScrolledText

from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from components.functions import read_yaml, edit_yaml
from controller.Settings.Appearance import detect_darkmode_in_windows
from datetime import datetime

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ustawienia")
        self.geometry("800x800")
        colorBackground = read_yaml("backgroundColor")
        self.current_font = read_yaml("font") or "Arial"


        self.menu_frame = Frame(self, width=200, bg="lightgrey")
        self.menu_frame.pack(side=LEFT, fill=Y)

        self.display_frame = Frame(self, bg=colorBackground)
        self.display_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.create_menu_buttons()

    def create_menu_buttons(self):
        button_general = Button(self.menu_frame, text="Wygląd i zachowanie", font=(self.current_font, 12), command=self.show_general_settings)
        button_general.pack(pady=10, fill=X)

        button_history = Button(self.menu_frame, text="Historia obliczeń", font=(self.current_font, 12), command=self.show_history_settings)
        button_history.pack(pady=11, fill=X)

        button_precision = Button(self.menu_frame, text="Precyzja obliczeń", font=(self.current_font, 12), command=self.show_precision_settings)
        button_precision.pack(pady=12, fill=X)

        button_font = Button(self.menu_frame, text="Czcionka", font=(self.current_font, 12), command=self.show_font_settings)
        button_font.pack(pady=13, fill=X)


    def show_general_settings(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        current_background_color = read_yaml("backgroundColor") or "white"


        label = Label(self.display_frame, text="Wygląd", font=(self.current_font, 14))
        label.place(x=10, y=10)

        label_theme = Label(self.display_frame, text="Wybierz motyw lub kolor:", font=(self.current_font, 12))
        label_theme.place(x=10, y=50)

        color_display = Frame(self.display_frame,bg=current_background_color ,width=50, height=25, relief="solid", borderwidth=1)
        color_display.place(x=200, y=80)

        def set_background_color(color_value):
            if color_value:
                self.configure(bg=color_value)
                edit_yaml("backgroundColor", color_value)
                color_display.config(bg=color_value)

        def open_color_picker():
            color_code = askcolor(title="Wybierz kolor tła")[1]
            if color_code:
                set_background_color(color_code)

        button_color_picker = Button(self.display_frame, text="Wybierz kolor", font=(self.current_font, 10),
                                     command=open_color_picker)
        button_color_picker.place(x=10, y=80)

        selected_theme = StringVar(value="system")


        def on_theme_change():
            theme = selected_theme.get()
            if theme == "dark":
                color_value = "#2E2E2E"
            elif theme == "light":
                color_value = "#FFFFFF"
            elif theme == "system":
                color_value = detect_darkmode_in_windows()
            else:
                color_value = "#FFFFFF"
            set_background_color(color_value)

        Radiobutton(self.display_frame, text="Ciemny", variable=selected_theme, value="dark", command=on_theme_change,
                    font=(self.current_font, 12)).place(x=10, y=120)
        Radiobutton(self.display_frame, text="Jasny", variable=selected_theme, value="light", command=on_theme_change,
                    font=(self.current_font, 12)).place(x=80, y=120)
        Radiobutton(self.display_frame, text="Systemowy", variable=selected_theme, value="system",
                    command=on_theme_change,
                    font=(self.current_font, 12)).place(x=150, y=120)

    def show_precision_settings(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        label = Label(self.display_frame, text="Precyzja obliczeń", font=("Arial", 14))
        label.place(x=10, y=10)

        precision_var = IntVar(value=read_yaml("calculationPrecision"))

        label_precision = Label(self.display_frame, text="Poziom precyzji (1-10):", font=("Arial", 12))
        label_precision.place(x=10, y=50)

        precision_scale = Scale(self.display_frame, from_=1, to=10, orient=HORIZONTAL, variable=precision_var)
        precision_scale.place(x=10, y=80)

        def on_precision_change():
            edit_yaml("calculationPrecision", precision_var.get())

        button_save = Button(self.display_frame, text="Zapisz", command=on_precision_change)
        button_save.place(x=10, y=150)

    def show_history_settings(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        label = Label(self.display_frame, text="Ustawienia historii obliczeń", font=(self.current_font, 14))
        label.place(x=10, y=10)

        date_format_options = [
            "R-M-D G:M:S",
            "D-M-R G:M:S",
            "R/M/D",
            "D/M/R",
            "M-D-R",
        ]

        selected_date_format = StringVar(value=read_yaml("dateFormat"))

        label_date_format = Label(self.display_frame, text="Format zapisu daty:", font=(self.current_font, 12))
        label_date_format.place(x=10, y=50)

        date_format_menu = OptionMenu(
            self.display_frame,
            selected_date_format,
            selected_date_format.get(),
            *date_format_options
        )
        date_format_menu.place(x=10, y=80)

        label_examples = Label(self.display_frame, text="Przykłady formatów daty:", font=(self.current_font, 12))
        label_examples.place(x=10, y=120)

        example_text = ScrolledText(self.display_frame, width=50, height=10)
        example_text.place(x=10, y=150)

        def update_example_text():
            examples = [
                f"{selected_date_format.get()}: {self.format_example_date(selected_date_format.get())}"
                for _ in range(5)
            ]
            example_text.delete(1.0, END)
            example_text.insert(END, "\n".join(examples))

        selected_date_format.trace("w", lambda *args: update_example_text())
        update_example_text()

        button_save = Button(self.display_frame, text="Zapisz", command=lambda: edit_yaml("dateFormat", selected_date_format.get()))
        button_save.place(x=10, y=330)

    def show_font_settings(self):
        for widget in self.display_frame.winfo_children():
            widget.destroy()

        label = Label(self.display_frame, text="Rodzaje czcionek", font=(self.current_font, 14))
        label.place(x=10, y=10)

        font_options = ["Arial", "Courier New", "Times New Roman", "Comic Sans MS", "Verdana"]
        font_listbox = Listbox(self.display_frame, selectmode=SINGLE, height=len(font_options),
                               font=(self.current_font, 14))
        font_listbox.place(x=10, y=50, width=200)
        for font in font_options:
            font_listbox.insert("end", font)

        label_color = Label(self.display_frame, text="Kolor czcionki:", font=(self.current_font, 14))
        label_color.place(x=10, y=250)

        color_display = Frame(self.display_frame, width=50, height=25, bg="black", relief="solid", borderwidth=1)
        color_display.place(x=150, y=250)

        def choose_font_color():
            color_code = askcolor(title="Wybierz kolor czcionki")[1]
            if color_code:
                color_display.config(bg=color_code)
                self.font_color = color_code

        self.font_color = read_yaml("fontColor") or "#000000"
        color_display.config(bg=self.font_color)

        button_color_picker = Button(self.display_frame, text="Wybierz kolor", font=(self.current_font, 10),
                                     command=choose_font_color)
        button_color_picker.place(x=10, y=290)

        def apply_font_settings():
            try:
                if not font_listbox.curselection():
                    label.config(text="Proszę wybrać czcionkę!", font=("Arial", 14))
                    return

                selected_font = font_listbox.get(font_listbox.curselection())
                self.current_font = selected_font
                label.config(text=f"Wybrana czcionka: {selected_font}", font=(selected_font, 14))
                edit_yaml("font", selected_font)

                edit_yaml("fontColor", self.font_color)
            except Exception as e:
                print(f"Error occurred: {e}")

        apply_button = Label(self.display_frame, text="Zapisz", bg="lightblue", font=(self.current_font, 12),
                             cursor="hand2")
        apply_button.place(x=10, y=350)
        apply_button.bind("<Button-1>", lambda event: apply_font_settings())

    def format_example_date(self, date_format):
        """Zwraca przykład daty w podanym formacie."""
        sample_date = datetime(2023, 11, 28, 15, 45, 30)
        mapping = {
            "R": "%Y",
            "M": "%m",
            "D": "%d",
            "G": "%H",
            "i": "%M",
            "s": "%S",
        }
        for key, value in mapping.items():
            date_format = date_format.replace(key, value)
        return sample_date.strftime(date_format)

    def export_to_pdf(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".pdf", filetypes=[("PDF files", "*.pdf")])

        if file_path:
            pdf = canvas.Canvas(file_path, pagesize=A4)
            pdf.drawString(100, 800, "Historia obliczeń")

            history_data = read_yaml("history")

            y_position = 750
            for record in history_data:
                if y_position < 50:
                    pdf.showPage()
                    y_position = 750

                pdf.drawString(100, y_position, str(record))
                y_position -= 20

            pdf.save()

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            history_data = read_yaml("history")

            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Data i czas", "Operacja", "Wynik"])
                for record in history_data:
                    writer.writerow(record)

    def save_settings(self):
        self.destroy()
