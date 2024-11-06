from PyQt5.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QApplication, QMenuBar, QAction
from PyQt5.QtCore import Qt
from view.SettingsWindowPy import SettingsWindow

class CalculatorViewPy(QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle('Kalkulator')
        self.setGeometry(100, 100, 300, 400)

        central_widget = QWidget(self)
        main_layout = QVBoxLayout()

        menubar = self.menuBar()
        filemenu = menubar.addMenu('Plik')
        editmenu = menubar.addMenu('Edytuj')
        settings_menu = menubar.addMenu('Ustawienia')
        helpmenu = menubar.addMenu('Pomoc')

        exit_action = QAction('Wyjście', self)
        exit_action.triggered.connect(self.close)
        filemenu.addAction(exit_action)

        clear_action = QAction('Wyczyść', self)
        clear_action.triggered.connect(self.clear_display)
        editmenu.addAction(clear_action)

        about_action = QAction('Informacje', self)
        about_action.triggered.connect(self.show_about)
        helpmenu.addAction(about_action)

        settings_action = QAction('Opcje...', self)
        settings_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(settings_action)

        self.display = QLineEdit()
        self.display.setReadOnly(True)
        self.display.setFixedHeight(50)
        self.display.setAlignment(Qt.AlignRight)
        main_layout.addWidget(self.display)

        button_layout = QGridLayout()
        buttons = [
            ('%', 0, 0), ('CE', 0, 1), ('C', 0, 2), ('<-', 0, 3),
            ('7', 1, 0), ('8', 1, 1), ('9', 1, 2), ('/', 1, 3),
            ('4', 2, 0), ('5', 2, 1), ('6', 2, 2), ('*', 2, 3),
            ('1', 3, 0), ('2', 3, 1), ('3', 3, 2), ('-', 3, 3),
            ('0', 4, 0), ('.', 4, 1), ('=', 4, 2), ('+', 4, 3)
        ]

        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            button.setFixedSize(60, 60)
            button_layout.addWidget(button, row, col)

        main_layout.addLayout(button_layout)

        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def update_display(self, text):
        self.display.setText(text)

    def get_display_text(self):
        return self.display.text()

    def clear_display(self):
        self.display.clear()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.show()

    def show_about(self):
        self.display.setText("Kalkulator wersja 0.1 by Arkadiusz Jemioło")

    def create_buttons(self, on_button_click):
        for button in self.findChildren(QPushButton):
            button.clicked.connect(lambda _, b=button: on_button_click(b.text()))
