import tkinter as tk
from tkinter import ttk, Menu

class CalculatorApp(tk.Tk):
    def __init__(self):
        super().__init__()

        self.title("Demo Kalkulatora")
        self.geometry("600x400")

        # Create the main container (frame)
        self.main_frame = ttk.Frame(self)
        self.main_frame.pack(fill=tk.BOTH, expand=True)

        # MENU (menu should be set on the root window, not on the frame)
        menu = Menu(self)
        self.config(menu=menu)

        # File section
        filemenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Plik', menu=filemenu)
        filemenu.add_command(label='Nowy')
        filemenu.add_command(label='Otwórz...')
        filemenu.add_separator()
        filemenu.add_command(label='Wyjście', command=self.quit)  # Command to close the application

        # Help section
        helpmenu = Menu(menu, tearoff=0)
        menu.add_cascade(label='Pomoc', menu=helpmenu)
        helpmenu.add_command(label='Informacje...')

        # Create a menu toggle button
        self.menu_toggle_button = tk.Button(self.main_frame, text="≡", command=self.toggle_menu)
        self.menu_toggle_button.pack(side=tk.TOP,anchor='nw', padx=5, pady=5)

        # Create the menu panel (left-side menu)
        self.menu_frame = ttk.Frame(self.main_frame, width=150)
        self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)

        self.menu_buttons = ["ABC", "ABC2", "ABC3", "ABC4"]
        for btn_text in self.menu_buttons:
            btn = tk.Button(self.menu_frame, text=btn_text)
            btn.pack(fill=tk.X, pady=2)

        # Create the calculator area
        self.calc_frame = ttk.Frame(self.main_frame)
        self.calc_frame.pack(side=tk.RIGHT, fill=tk.BOTH, expand=True, padx=10, pady=10)

        self.create_calculator()

        # Track menu visibility
        self.menu_visible = True

    def create_calculator(self):
        # Create the display entry (for showing input and results)
        self.display = tk.Entry(self.calc_frame, font=("Arial", 20), justify="right")
        self.display.grid(row=0, column=0, columnspan=4, pady=10, sticky="nsew")

        # Create calculator buttons
        buttons = [
            ('%', 1, 0), ('CE', 1, 1), ('C', 1, 2), ('<-', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3)
        ]

        # Configure rows and columns
        for row in range(6):
            self.calc_frame.grid_rowconfigure(row, weight=1)
        for col in range(4):
            self.calc_frame.grid_columnconfigure(col, weight=1)

        # Add buttons to the calculator layout
        for (text, row, col) in buttons:
            button = tk.Button(self.calc_frame, text=text, font=("Arial", 18), command=lambda t=text: self.on_button_click(t))
            button.grid(row=row, column=col, sticky="nsew", padx=5, pady=5)

    def toggle_menu(self):
        """Toggles the visibility of the menu."""
        if self.menu_visible:
            self.menu_frame.pack_forget()  # Hide the menu
        else:
            self.menu_frame.pack(side=tk.LEFT, fill=tk.Y)  # Show the menu again
        self.menu_visible = not self.menu_visible

    def on_button_click(self, char):
        """Handle button clicks for the calculator."""
        if char == '=':
            # Simplified evaluation logic
            try:
                result = str(eval(self.display.get()))
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, result)
            except:
                self.display.delete(0, tk.END)
                self.display.insert(tk.END, "Error")
        elif char == 'C':
            self.display.delete(0, tk.END)
        else:
            self.display.insert(tk.END, char)


if __name__ == "__main__":
    app = CalculatorApp()
    app.mainloop()
