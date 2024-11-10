import tkinter as tk
from tkinter import *
from tkinter import filedialog
import csv
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import A4
from components.functions import read_yaml, edit_yaml
from controller.Settings.Appearance import detect_darkmode_in_windows

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Ustawienia")
        self.geometry("800x800")

        self.menu_frame = Frame(self, width=200, bg="lightgrey")
        self.menu_frame.pack(side=LEFT, fill=Y)

        self.display_frame = Frame(self, bg="white")
        self.display_frame.pack(side=RIGHT, fill=BOTH, expand=True)

        self.create_menu_buttons()

    def create_menu_buttons(self):
        button_general = Button(self.menu_frame, text="Wygląd i zachowanie", command=self.show_general_settings)
        button_general.pack(pady=10, fill=X)

        button_history = Button(self.menu_frame, text="Historia obliczeń", command=self.show_history_settings)
        button_history.pack(pady=11, fill=X)

        button_precision = Button(self.menu_frame, text="Precyzja obliczeń", command=self.show_precision_settings)
        button_precision.pack(pady=12, fill=X)

    def show_general_settings(self):
        color = StringVar(value=read_yaml("backgroundColor"))

        for widget in self.display_frame.winfo_children():
            widget.destroy()

        label = Label(self.display_frame, text="Wygląd", font=("Arial", 14))
        label.place(x=10, y=10)

        label_theme = Label(self.display_frame, text="motyw", font=("Arial", 12))
        label_theme.place(x=10, y=50)

        def on_theme_change():
            selected_theme = color.get()
            if selected_theme == "system":
                system_theme = detect_darkmode_in_windows()
                edit_yaml("backgroundColor", system_theme)
            else:
                edit_yaml("backgroundColor", selected_theme)

        Radiobutton(self.display_frame, text="Ciemny", variable=color, value="dark", command=on_theme_change).place(x=10, y=80)
        Radiobutton(self.display_frame, text="Jasny", variable=color, value="white", command=on_theme_change).place(x=80, y=80)
        Radiobutton(self.display_frame, text="Systemowy", variable=color, value="system", command=on_theme_change).place(x=138, y=80)

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


        label = Label(self.display_frame, text="Ustawienia historii obliczeń", font=("Arial", 14))
        label.place(x=10, y=10)


        date_format_options = [
            "R-M-D G:M:S",  # Rok-miesiąc-dzień godzina:minuta:sekunda
            "D-M-R G:M:S",  # Dzień-miesiąc-rok godzina:minuta:sekunda
            "R/M/D",  # Rok/miesiąc/dzień
            "D/M/R",  # Dzień/miesiąc/rok
            "M-D-R",  # Miesiąc-dzień-rok
        ]

        selected_date_format = StringVar(value=read_yaml("dateFormat"))

        label_date_format = Label(self.display_frame, text="Format zapisu daty:", font=("Arial", 12))
        label_date_format.place(x=10, y=50)

        date_format_menu = OptionMenu(
            self.display_frame,
            selected_date_format,
            selected_date_format.get(),
            *date_format_options
        )
        date_format_menu.place(x=10, y=80)

        def on_date_format_change():
            edit_yaml("dateFormat", selected_date_format.get())

        button_save = Button(self.display_frame, text="Zapisz", command=on_date_format_change)
        button_save.place(x=10, y=150)

        button_export_pdf = Button(self.display_frame, text="Eksportuj do PDF", command=self.export_to_pdf)
        button_export_pdf.place(x=10, y=200)

        button_export_csv = Button(self.display_frame, text="Eksportuj do CSV", command=self.export_to_csv)
        button_export_csv.place(x=10, y=250)

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

                # Dodanie rekordu do PDF
                pdf.drawString(100, y_position, str(record))
                y_position -= 20

            pdf.save()

    def export_to_csv(self):
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])

        if file_path:
            history_data = read_yaml("history")

            with open(file_path, mode="w", newline="") as file:
                writer = csv.writer(file)
                writer.writerow(["Data i czas", "Operacja", "Wynik"])  # Nagłówki kolumn, jeśli istnieją
                for record in history_data:
                    writer.writerow(record)

    def save_settings(self):
        self.destroy()
