'''
from tkinter import *

root = Tk()


root.title("test")
root.geometry("350x200")

lbl = Label(root, text="test")
lbl.grid()


root.mainloop()
'''
import math


def eval_trig(expression):
    # Definiowanie dostępnych funkcji trygonometrycznych
    allowed_functions = {
        'sin': math.sin,
        'cos': math.cos,
        'tan': math.tan,
        'asin': math.asin,
        'acos': math.acos,
        'atan': math.atan,
        'pi': math.pi,
        'e': math.e
    }

    #Dodawanie wszystkich funkcji trygonometrycznych z modułu math do lokalnego zakresu
    local_scope = {name: func for name, func in allowed_functions.items()}

    try:
        #Ocena wyrażenia w kontekście lokalnego zakresu
        result = eval(expression, {"__builtins__": None}, local_scope)
        return result
    except Exception as e:
        return f"Error: {e}"