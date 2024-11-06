import math

class CalculatorModelTk:
    def __init__(self):
        self.current_expression = ""

    def append_character(self, char):
        self.current_expression += str(char)

    def clear(self):
        self.current_expression = ""

    def eval_trig(self, expression):
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

        local_scope = {name: func for name, func in allowed_functions.items()}

        try:
            result = eval(expression, {"__builtins__": None}, local_scope)
            return result
        except Exception as e:
            return f"Error: {e}"
