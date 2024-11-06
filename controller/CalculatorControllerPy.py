import sys
from PyQt5.QtWidgets import QApplication
from model.CalculatorModelPy import CalculatorModelPy
from view.CalculatorViewPy import CalculatorViewPy


class CalculatorController:
    def __init__(self, view, model):
        self.view = view
        self.model = model

        self.view.create_buttons(self.on_button_click)

    def on_button_click(self, char):
        if char == '=':
            result = self.model.calculate()
            self.view.update_display(result)
            self.model.clear()
        elif char == 'C':
            self.view.clear_display()
            self.model.clear()
        else:
            self.model.append_character(char)
            self.view.update_display(self.view.get_display_text() + char)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    model = CalculatorModelPy()
    view = CalculatorViewPy()

    controller = CalculatorController(view, model)

    view.show()

    sys.exit(app.exec_())
