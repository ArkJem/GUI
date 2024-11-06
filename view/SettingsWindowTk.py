import tkinter as tk
from tkinter import ttk, Menu

class SettingsWindow(tk.Toplevel):
    def __init__(self, parent):
        super().__init__(parent)
        self.title("Settings")
        self.geometry("300x200")

        tk.Label(self, text="Decimal Precision:").pack(pady=10)
        self.precision_spinbox = ttk.Spinbox(self, from_=0, to=10, width=5)
        self.precision_spinbox.pack(pady=10)


        self.sound_var = tk.IntVar(value=1)
        self.sound_checkbox = ttk.Checkbutton(self, text="Enable Sound", variable=self.sound_var)
        self.sound_checkbox.pack(pady=10)

        # Button to save the settings
        save_button = ttk.Button(self, text="Save", command=self.save_settings)
        save_button.pack(pady=10)

    def save_settings(self):
        precision = self.precision_spinbox.get()
        sound_enabled = bool(self.sound_var.get())
        tk.messagebox.showinfo("Settings Saved", f"Precision: {precision}\nSound Enabled: {sound_enabled}")
        self.destroy()