import math
from datetime import datetime
from components.functions import read_yaml


class CalculatorModelTk:
    def __init__(self):
        self.current_expression = ""
        self.memory = 0

    def save_to_memory(self, value):
        try:
            self.memory = float(value)
        except ValueError:
            raise ValueError("Nieprawidłdowa wartość")

    def recall_memory(self):
        return self.memory

    def clear_memory(self):
        self.memory = 0

    def add_to_memory(self, value):
        try:
            self.memory += float(value)
        except ValueError:
            raise ValueError("Nieprawidłowa wartość")

    def subtract_from_memory(self, value):
        try:
            self.memory -= float(value)
        except ValueError:
            raise ValueError("Nieprawidłowa wartość")

    def save_calc(self, expression, calc):
        format_date = read_yaml("dateFormat")
        format_map = {
            "R": "%Y",
            "M": "%m",
            "D": "%d",
            "G": "%H",
            "i": "%M",
            "S": "%S",
        }

        for symbol, strftime_format in format_map.items():
            format_date = format_date.replace(symbol, strftime_format)

        current_date = datetime.now().strftime(format_date)

        with open("calcTk.txt", "a") as file:
            file.write(f"{current_date} | {expression} = {calc}\n")

    def append_character(self, char):
        self.current_expression += str(char)

    def clear(self):
        self.current_expression = ""

    def evaluateRNP(self, expression):
        expression = expression.split()
        stack = []
        for token in expression:
            if token not in '/*+-':
                stack.append(float(token))
            else:
                right = stack.pop()
                left = stack.pop()
                if token == '+':
                    stack.append(left + right)
                elif token == '-':
                    stack.append(left - right)
                elif token == '*':
                    stack.append(left * right)
                elif token == '/':
                    stack.append(left / right)
        return stack.pop()


    def eval_trig(self, expression):
        allowed_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'sqrt': math.sqrt,
            'pi': math.pi,
            'e': math.e
        }

        local_scope = {name: func for name, func in allowed_functions.items()}

        open_parentheses = expression.count('(')
        close_parentheses = expression.count(')')
        if open_parentheses > close_parentheses:
            expression += ')' * (open_parentheses - close_parentheses)

        try:
            result = eval(expression, {"__builtins__": None}, local_scope)
            self.save_calc(expression, str(result))
            return result
        except Exception as e:
            return f"Error: {e}"
