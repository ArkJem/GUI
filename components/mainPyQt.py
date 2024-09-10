import sys
from PyQt5.QtWidgets import QApplication, QWidget, QGridLayout, QPushButton, QLineEdit
from PyQt5.QtCore import Qt


class Calculator(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo kalkulatora")

        self.layout = QGridLayout()

        #Tworzy pole do wpisywania liczb
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 30px;")
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        #for tworzący siatkę przycisków do wprowadzania działań
        for text, row, col in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 20px; padding: 15px;")
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            self.layout.addWidget(button, row, col)

        self.setLayout(self.layout)

    def on_button_click(self, char):
        if char == '=':
            try:
                result = str(eval(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Błąd")
        elif char == 'C':
            self.display.clear()
        else:
            self.display.setText(self.display.text() + char)

#main
app = QApplication([])
window = Calculator()
window.show()
sys.exit(app.exec())
