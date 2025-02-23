import math, re

class CalculatorModelPy:
    def __init__(self):
        self.current_expression = ""
        self.memory = None

    def save_to_memory(self, value):
        try:
            self.memory = float(value)
        except ValueError:
            self.memory = None

    def recall_memory(self):
        return self.memory

    def clear_memory(self):
        self.memory = None

    def add_to_memory(self, value):
        if self.memory is not None:
            try:
                self.memory += float(value)
            except ValueError:
                pass

    def subtract_from_memory(self, value):
        if self.memory is not None:
            try:
                self.memory -= float(value)
            except ValueError:
                pass

    def save_calc(self, calc):
        with open("calcPy.txt", "a") as file:
            file.write(calc + "\n")

    def append_character(self, char):
        self.current_expression += str(char)

    def clear(self):
        self.current_expression = ""

    def is_rpn(self, expression):
        tokens = expression.split()
        stack = 0
        for token in tokens:
            if token in {'+', '-', '*', '/', '^', 'sin', 'cos', 'tan'}:
                stack -= 1
            else:
                stack += 1

            if stack < 1:
                return False

        return stack == 1

    def eval_rpn(self, expression):
        tokens = expression.split()
        stack = []

        allowed_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan
        }

        for token in tokens:
            if token in {'+', '-', '*', '/', '^'}:
                b = stack.pop()
                a = stack.pop()

                if token == '+':
                    stack.append(a + b)
                elif token == '-':
                    stack.append(a - b)
                elif token == '*':
                    stack.append(a * b)
                elif token == '/':
                    if b == 0:
                        return "Błąd: Dzielenie przez zero!"
                    stack.append(a / b)
                elif token == '^':
                    stack.append(a ** b)

            elif token in allowed_functions:
                a = stack.pop()
                stack.append(allowed_functions[token](a))

            else:
                try:
                    stack.append(float(token))
                except ValueError:
                    return f"Error: Invalid token '{token}'"

        return stack[0] if len(stack) == 1 else "Błąd: niepoprawny ciąg ONP"

    def eval_trig(self, expression):
        import math

        allowed_functions = {
            'sin': math.sin,
            'cos': math.cos,
            'tan': math.tan,
            'asin': math.asin,
            'acos': math.acos,
            'atan': math.atan,
            'pi': math.pi,
            'e': math.e,
        }

        local_scope = {name: func for name, func in allowed_functions.items()}
        local_scope.update({'abs': abs, 'round': round})

        def is_rpn(expression):
            tokens = expression.split()
            numbers = sum(1 for token in tokens if token.replace('.', '', 1).isdigit())
            operators = sum(1 for token in tokens if token in ('+', '-', '*', '/', '^'))
            return numbers > operators and all(
                token.isdigit() or token in ('+', '-', '*', '/', '^') for token in tokens
            )

        def evaluate_rpn(rpn_expression):
            stack = []
            operators = {
                '+': lambda a, b: a + b,
                '-': lambda a, b: a - b,
                '*': lambda a, b: a * b,
                '/': lambda a, b: a / b if b != 0 else float('inf'),
                '^': lambda a, b: a ** b,
            }

            for token in rpn_expression.split():
                if token.replace('.', '', 1).isdigit():
                    stack.append(float(token))
                elif token in operators:
                    if len(stack) < 2:
                        raise ValueError("Niepoprawny ciąg ONP")
                    b = stack.pop()
                    a = stack.pop()
                    stack.append(operators[token](a, b))
                else:
                    raise ValueError(f"Błąd: {token}")

            if len(stack) != 1:
                raise ValueError("niepoprawny ciąg ONP")
            return stack[0]

        try:
            if is_rpn(expression):
                result = evaluate_rpn(expression)
            else:
                result = eval(expression, {"__builtins__": None}, local_scope)

            self.save_calc(f"{expression} = {result}")
            return str(result)

        except ZeroDivisionError:
            return "Błąd: Dzielenie przez zero!"
        except Exception as e:
            return f"Błąd: {str(e)}"

    def calculate(self):
        return self.eval_trig(self.current_expression)
