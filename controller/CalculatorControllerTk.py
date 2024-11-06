import tkinter as tk
from model.CalculatorModelTk import CalculatorModelTk
from view.CalculatorViewTk import CalculatorViewTk

class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.create_calculator_buttons(self.on_button_click)

    def on_button_click(self, char):
        if char == '=':
            expression = self.view.display.get()
            result = self.model.eval_trig(expression)

            self.view.display.delete(0, tk.END)
            self.view.display.insert(tk.END, result)
            self.model.clear()
        elif char == 'C':
            self.view.display.delete(0, tk.END)
            self.model.clear()
        else:
            self.model.append_character(char)
            self.view.display.insert(tk.END, char)


if __name__ == "__main__":
    model = CalculatorModelTk()
    view = CalculatorViewTk()
    controller = CalculatorController(view, model)
    view.mainloop()
