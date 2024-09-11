import sys
from PyQt5.QtWidgets import QApplication, QMainWindow, QWidget, QGridLayout, QPushButton, QLineEdit, QVBoxLayout, QScrollArea, QHBoxLayout, QFrame, QMenu
from PyQt5.QtCore import Qt
from Calculator import eval_trig


class Calculator(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Demo kalkulatora")
        self.resize(600, 400)

        central_widget = QWidget()
        self.setCentralWidget(central_widget)

        self.main_layout = QHBoxLayout(central_widget)

        self.menu_toggle_button = QPushButton("≡")
        self.menu_toggle_button.setFixedSize(30, 30)
        self.menu_toggle_button.clicked.connect(self.toggle_menu)

        self.menu_layout = QVBoxLayout()
        self.menu_buttons = [
            "ABC", "ABC2", "ABC3", "ABC4",
        ]

        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        self.menu_widget = QWidget()
        menu_layout = QVBoxLayout(self.menu_widget)

        for btn_text in self.menu_buttons:
            button = QPushButton(btn_text)
            button.setStyleSheet("font-size: 15px; padding: 10px;")
            menu_layout.addWidget(button)

        self.scroll_area.setWidget(self.menu_widget)
        self.menu_layout.addWidget(self.scroll_area)

        self.main_layout.addLayout(self.menu_layout)

        self.layout = QGridLayout()

        #Tworzy pole do wpisywania liczb
        self.display = QLineEdit()
        self.display.setAlignment(Qt.AlignRight)
        self.display.setReadOnly(True)
        self.display.setStyleSheet("font-size: 30px;")
        self.layout.addWidget(self.display, 0, 0, 1, 4)

        buttons = [
            ('%', 1, 0), ('CE', 1, 1), ('C', 1, 2), ('<-', 1, 3),
            ('7', 2, 0), ('8', 2, 1), ('9', 2, 2), ('/', 2, 3),
            ('4', 3, 0), ('5', 3, 1), ('6', 3, 2), ('*', 3, 3),
            ('1', 4, 0), ('2', 4, 1), ('3', 4, 2), ('-', 4, 3),
            ('0', 5, 0), ('.', 5, 1), ('=', 5, 2), ('+', 5, 3)
        ]

        for text, row, col in buttons:
            button = QPushButton(text)
            button.setStyleSheet("font-size: 20px; padding: 15px;")
            button.clicked.connect(lambda checked, t=text: self.on_button_click(t))
            self.layout.addWidget(button, row, col)

        calculator_frame = QFrame()
        calculator_frame.setLayout(self.layout)

        self.main_layout.addWidget(self.menu_toggle_button)
        self.main_layout.addWidget(calculator_frame)

        self.menu_visible = True
        self._create_menu_bar()

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&Plik")
        edit_menu = menu_bar.addMenu("&Edytuj")
        help_menu = menu_bar.addMenu("&Pomoc")

    def toggle_menu(self):
        if self.menu_visible:
            self.scroll_area.hide()
        else:
            self.scroll_area.show()
        self.menu_visible = not self.menu_visible

    def on_button_click(self, char):
        if char == '=':
            try:
                result = str(eval_trig(self.display.text()))
                self.display.setText(result)
            except:
                self.display.setText("Błąd")
        elif char == 'C':
            self.display.clear()
        else:
            self.display.setText(self.display.text() + char)


app = QApplication([])
window = Calculator()
window.show()
sys.exit(app.exec())
