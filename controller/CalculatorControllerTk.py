import math
import tkinter as tk
from tkinter import messagebox

from model.CalculatorModelTk import CalculatorModelTk
from view.CalculatorViewTk import CalculatorViewTk

class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.on_button_click = self.on_button_click

    def on_button_click(self, char):
        if char == '=':
            expression = self.view.display.get()

            if ' ' in expression:
                try:
                    result = self.model.evaluateRNP(expression)
                except Exception as e:
                    messagebox.showerror("Error", f"Nieprawidłowe wyrażanie ONP {e}")
                    return
            else:
                expression = self.replace_sqrt(expression)
                expression = expression.replace("π", "pi")
                try:
                    result = self.model.eval_trig(expression)
                except Exception as e:
                    messagebox.showerror("Error", f"Nieprawidłowe wyrażenie {e}")
                    return

            self.view.display.delete(0, tk.END)
            self.view.display.insert(tk.END, result)
            self.view.add_to_history(expression, result)

            self.model.clear()

        elif char == '<-':
            current_text = self.view.display.get()
            if current_text:
                updated_text = current_text[:-1]
                self.view.display.delete(0, tk.END)
                self.view.display.insert(tk.END, updated_text)

        elif char == '%':
            try:
                value = float(self.view.display.get())
                result = value / 100
                self.view.display.delete(0, tk.END)
                self.view.display.insert(tk.END, result)
            except ValueError:
                messagebox.showerror("Error", "Nieprawidłowa wartość dla operacji procentowej")
        elif char in ['sin', 'cos', 'tan']:
            try:
                value = float(self.view.display.get())
                if char == 'sin':
                    result = math.sin(math.radians(value))
                elif char == 'cos':
                    result = math.cos(math.radians(value))
                elif char == 'tan':
                    result = math.tan(math.radians(value))
                self.view.display.delete(0, tk.END)
                self.view.display.insert(tk.END, result)
            except ValueError:
                messagebox.showerror("Error", f"Nieprawidłowa wartość dla funkcji {char}")
        elif char == 'log':
            try:
                value = float(self.view.display.get())
                result = math.log10(value)
                self.view.display.delete(0, tk.END)
                self.view.display.insert(tk.END, result)
            except ValueError:
                messagebox.showerror("Error", "Nieprawidłowa wartość dla logarytmu")
        elif char == '√':
            try:
                value = float(self.view.display.get())
                result = math.sqrt(value)
                self.view.display.delete(0, tk.END)
                self.view.display.insert(tk.END, result)
            except ValueError:
                messagebox.showerror("Error", "Nieprawidłowa wartość dla pierwiastka kwadratowego")
        elif char == 'C':
            self.view.display.delete(0, tk.END)
            self.model.clear()
        elif char == 'CE':
            current_text = self.view.display.get()
            self.view.display.delete(0, tk.END)
            self.view.display.insert(0, current_text[:-1])
        elif char == 'RPN':
            expression = self.view.display.get()
            try:
                result = self.model.evaluateRNP(expression)
            except Exception as e:
                messagebox.showerror("Error", f"Nieprawidłowe wyrażenie ONP: {e}")
                return

            self.view.display.delete(0, tk.END)
            self.view.display.insert(tk.END, result)
            self.view.add_to_history(expression, result)
        elif char == 'MS':
            value = self.view.display.get()
            try:
                self.model.save_to_memory(value)
                print(f"Zapisano w pamięci: {value}")
            except ValueError:
                messagebox.showerror("Error", "Nieprawidłowa wartość do zapisania w pamięci")
        elif char == 'MR':
            memory_value = self.model.recall_memory()
            self.view.display.delete(0, tk.END)
            self.view.display.insert(tk.END, memory_value)
            print(f"Przywrócono z pamięci: {memory_value}")
        elif char == 'MC':
            self.model.clear_memory()
            print("Wyczyszczono pamięć")
        elif char == 'M+':
            value = self.view.display.get()
            try:
                self.model.add_to_memory(value)
                print(f"Dodano do pamięci: {value}")
            except ValueError:
                messagebox.showerror("Error", "Nieprawidłowa wartość do dodania do pamięci")
        elif char == 'M-':
            value = self.view.display.get()
            try:
                self.model.subtract_from_memory(value)
                print(f"Odjęto o: {value}")
            except ValueError:
                messagebox.showerror("Error", "Nieprawidłowa wartość do odjęcia od pamięci")
        else:
            self.model.append_character(char)
            self.view.display.insert(tk.END, char)

    def replace_sqrt(self, expression):
        import re
        return re.sub(r'√(\d+|\(.+?\))', r'math.sqrt(\1)', expression)

if __name__ == "__main__":
    model = CalculatorModelTk()
    view = CalculatorViewTk()
    controller = CalculatorController(view, model)
    view.mainloop()
