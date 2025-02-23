from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure
import numpy as np
from PyQt5.QtWidgets import (
    QMainWindow, QWidget, QVBoxLayout, QLineEdit, QPushButton, QGridLayout, QHBoxLayout, QFrame,
    QStackedWidget, QLabel, QAction, QTableWidget, QHeaderView, QAbstractItemView, QMenu,
    QApplication, QSizePolicy, QTabWidget
)
from PyQt5.QtCore import Qt, pyqtSignal
from view.SettingsWindowPy import SettingsWindow
from components.functions import read_yaml


class CalculatorViewPy(QMainWindow):
    button_clicked = pyqtSignal(str)
    def __init__(self):
        super().__init__()
        self.setWindowTitle('Kalkulator')
        self.setGeometry(200, 200, 1000, 400)
        self.initUI()
        self.set_background_color()

    def initUI(self):
        self.create_menu_bar()
        main_layout = QHBoxLayout()

        menu_content_layout = QVBoxLayout()
        left_section_layout = QVBoxLayout()

        self.menu_frame = QFrame()
        self.menu_frame.setFixedWidth(200)
        self.menu_layout = QVBoxLayout()
        self.menu_frame.setLayout(self.menu_layout)

        self.toggle_menu_button = QPushButton('≡')
        self.toggle_menu_button.setFixedHeight(30)
        self.toggle_menu_button.setFixedWidth(150)
        self.toggle_menu_button.clicked.connect(self.toggle_menu)
        left_section_layout.addWidget(self.toggle_menu_button)

        toggle_menu_layout = QVBoxLayout()
        toggle_menu_layout.addWidget(self.toggle_menu_button)
        toggle_menu_layout.addWidget(self.menu_frame)
        toggle_menu_layout.setContentsMargins(0, 0, 0, 0)

        self.menu_layout.addWidget(self.toggle_menu_button)
        self.standard_frame_button = QPushButton('Standardowy')
        self.standard_frame_button.clicked.connect(self.show_standard_frame)
        self.menu_layout.addWidget(self.standard_frame_button)

        self.scientific_frame_button = QPushButton('Naukowy')
        self.scientific_frame_button.clicked.connect(self.show_scientific_frame)
        self.menu_layout.addWidget(self.scientific_frame_button)

        self.plot_frame_button = QPushButton('Tworzenie wykresów')
        self.plot_frame_button.clicked.connect(self.show_plot_frame)
        self.menu_layout.addWidget(self.plot_frame_button)
        self.menu_layout.addStretch()

        left_section_layout.addWidget(self.menu_frame)

        main_layout.addLayout(left_section_layout)

        self.content_stack = QStackedWidget()

        self.standard_frame_page = self.create_standard_frame_page()
        self.scientific_frame_page = self.create_scientific_frame_page()
        self.plot_frame_page = self.create_plot_frame_page()
        self.content_stack.addWidget(self.standard_frame_page)
        self.content_stack.addWidget(self.scientific_frame_page)
        self.content_stack.addWidget(self.plot_frame_page)
        self.content_stack.setCurrentWidget(self.standard_frame_page)

        self.content_stack.setCurrentWidget(self.standard_frame_page)

        main_layout.addWidget(self.content_stack)

        main_layout.addLayout(menu_content_layout)

        self.toggle_widget = QTabWidget()
        self.toggle_widget.setFixedWidth(400)

        self.memory_widget = QLabel("Zapisane:brak")
        self.memory_widget.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
        self.memory_widget.setStyleSheet("background-color: lightgray; padding: 5px; border: 1px solid gray;")
        memory_tab = QVBoxLayout()
        memory_tab.addWidget(self.memory_widget)
        memory_tab_container = QWidget()
        memory_tab_container.setLayout(memory_tab)
        self.toggle_widget.addTab(memory_tab_container, "Pamięć")

        history_tab = QVBoxLayout()

        self.history_table = QTableWidget()
        self.history_table.setColumnCount(3)
        self.history_table.setHorizontalHeaderLabels(["Data", "Wyrażenie", "Wynik"])
        self.history_table.horizontalHeader().setStretchLastSection(True)
        self.history_table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.history_table.setEditTriggers(QAbstractItemView.NoEditTriggers)
        self.history_table.setSelectionBehavior(QAbstractItemView.SelectRows)
        self.history_table.setSelectionMode(QAbstractItemView.SingleSelection)
        self.history_table.setContextMenuPolicy(Qt.CustomContextMenu)

        self.history_table.customContextMenuRequested.connect(self.show_history_context_menu)

        history_tab.addWidget(self.history_table)

        self.save_history_button = QPushButton('Zapisz do plik tekstowego')
        self.save_history_button.clicked.connect(lambda: self.button_clicked.emit("SAVE_HISTORY"))
        history_tab.addWidget(self.save_history_button)

        self.export_csv_button = QPushButton('Zapisz do pliku CSV')
        self.export_csv_button.clicked.connect(lambda: self.button_clicked.emit("EXPORT_CSV"))
        history_tab.addWidget(self.export_csv_button)

        self.clear_history_button = QPushButton('Wyczyść historię')
        self.clear_history_button.clicked.connect(lambda: self.button_clicked.emit("CLEAR_HISTORY"))
        history_tab.addWidget(self.clear_history_button)

        history_tab_container = QWidget()
        history_tab_container.setLayout(history_tab)
        self.toggle_widget.addTab(history_tab_container, "Historia")

        main_layout.addWidget(self.toggle_widget)

        central_widget = QWidget()
        central_widget.setLayout(main_layout)
        self.setCentralWidget(central_widget)

    def show_history_context_menu(self, position):
        menu = QMenu()
        copy_action = QAction("Kopiuj", self)
        copy_action.triggered.connect(self.copy_expression)
        menu.addAction(copy_action)

        menu.exec_(self.history_table.viewport().mapToGlobal(position))

    def copy_expression(self):
        selected_items = self.history_table.selectedItems()
        if selected_items:
            expression = selected_items[1].text()
            clipboard = QApplication.clipboard()
            clipboard.setText(expression)

    def plot_function(self):
        function_text = self.plot_input.text()

        if not function_text.strip():
            self.plot_input.setPlaceholderText("Wpisz poprawną funkcję!")
            return

        try:
            x = np.linspace(-10, 10, 1000)
            y = eval(function_text)
            ax = self.plot_canvas.figure.subplots()
            ax.clear()

            ax.plot(x, y, label=f"y = {function_text}", color="blue")
            ax.axhline(0, color="black", linewidth=0.5, linestyle="--")
            ax.axvline(0, color="black", linewidth=0.5, linestyle="--")
            ax.grid(True, linestyle="--", alpha=0.6)
            ax.legend()
            ax.set_title("Tworzenie wykresu")
            ax.set_xlabel("x")
            ax.set_ylabel("y")

            self.plot_canvas.draw()

        except Exception as e:
            self.plot_input.setText("")
            self.plot_input.setPlaceholderText(f"Błąd: {str(e)}")

    def set_background_color(self):
        background_color = read_yaml("backgroundColor")
        font_color = read_yaml("fontColor")

        if background_color or font_color:
            style = f"""
                QMainWindow {{
                    background-color: {background_color or 'white'};
                }}
                QLineEdit {{
                    background-color: white;
                    color: black;
                }}
                QListWidget {{
                    background-color: white;
                    color: black;
                }}
            """
            self.setStyleSheet(style)

            if font_color:
                for button in self.findChildren(QPushButton):
                    button.setStyleSheet(f"color: {font_color};")
        else:
            self.setStyleSheet("")

    def create_standard_frame_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        self.standard_display = QLineEdit()
        self.standard_display.setReadOnly(False)
        self.standard_display.setAlignment(Qt.AlignRight)
        self.standard_display.setFixedHeight(50)
        self.standard_display.setContextMenuPolicy(Qt.CustomContextMenu)
        self.standard_display.customContextMenuRequested.connect(self.show_entry_context_menu)
        layout.addWidget(self.standard_display)

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
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, b=btn_text: self.button_clicked.emit(b))
            button_layout.addWidget(button, row, col)

        memory_buttons = [
            ('MS', 5, 0), ('M+', 5, 1), ('M-', 5, 2), ('MC', 5, 3), ('MR', 6, 0)
        ]

        for btn_text, row, col in memory_buttons:
            button = QPushButton(btn_text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, b=btn_text: self.button_clicked.emit(b))
            button_layout.addWidget(button, row, col)

        layout.addLayout(button_layout)
        frame.setLayout(layout)
        return frame

    def show_standard_frame(self):
        self.content_stack.setCurrentWidget(self.standard_frame_page)

    def create_scientific_frame_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        self.scientific_display = QLineEdit()
        self.scientific_display.setReadOnly(False)
        self.scientific_display.setAlignment(Qt.AlignRight)
        self.scientific_display.setFixedHeight(50)
        self.scientific_display.setContextMenuPolicy(Qt.CustomContextMenu)
        self.scientific_display.customContextMenuRequested.connect(self.show_entry_context_menu)
        layout.addWidget(self.scientific_display)

        button_layout = QGridLayout()

        buttons = [
            ('sin', 0, 0), ('cos', 0, 1), ('tan', 0, 2), ('ln', 0, 3),
            ('log', 1, 0), ('sqrt', 1, 1), ('^', 1, 2), ('pi', 1, 3),
            ('%', 2, 0), ('CE', 2, 1), ('C', 2, 2), ('<-', 2, 3),
            ('7', 3, 0), ('8', 3, 1), ('9', 3, 2), ('/', 3, 3),
            ('4', 4, 0), ('5', 4, 1), ('6', 4, 2), ('*', 4, 3),
            ('1', 5, 0), ('2', 5, 1), ('3', 5, 2), ('-', 5, 3),
            ('0', 6, 0), ('.', 6, 1), ('=', 6, 2), ('+', 6, 3),
            ('MS', 7, 0), ('M+', 7, 1), ('M-', 7, 2), ('MC', 7, 3),
            ('MR', 8, 0)
        ]

        for btn_text, row, col in buttons:
            button = QPushButton(btn_text)
            button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
            button.clicked.connect(lambda _, b=btn_text: self.button_clicked.emit(b))
            button_layout.addWidget(button, row, col)

        for i in range(8):
            button_layout.setRowStretch(i, 1)
        for j in range(4):
            button_layout.setColumnStretch(j, 1)

        layout.addLayout(button_layout)
        frame.setLayout(layout)
        return frame

    def show_entry_context_menu(self, position):
        menu = self.standard_display.createStandardContextMenu()

        paste_action = QAction("Wklej", self)
        paste_action.triggered.connect(self.paste_expression)
        menu.addAction(paste_action)

        menu.exec_(self.standard_display.mapToGlobal(position))

    def paste_expression(self):
        clipboard = QApplication.clipboard()
        self.standard_display.setText(clipboard.text())

    def show_scientific_frame(self):
        self.content_stack.setCurrentWidget(self.scientific_frame_page)

    def create_plot_frame_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        self.plot_input = QLineEdit()
        self.plot_input.setPlaceholderText("Wpisz funkcje sin(x), x**2, exp(-x))")
        layout.addWidget(self.plot_input)

        self.plot_button = QPushButton("Stwórz wykres")
        self.plot_button.clicked.connect(self.plot_function)
        layout.addWidget(self.plot_button)

        self.plot_canvas = FigureCanvas(Figure(figsize=(5, 3)))
        layout.addWidget(self.plot_canvas)

        frame.setLayout(layout)
        return frame

    def show_plot_frame(self):
        self.content_stack.setCurrentWidget(self.plot_frame_page)

    def toggle_menu(self):
        if self.menu_frame.isVisible():
            self.menu_frame.hide()
            self.toggle_menu_button.setText('≡')
        else:
            self.menu_frame.show()
            self.toggle_menu_button.setText('≡')

    def create_menu_bar(self):
        menu_bar = self.menuBar()

        file_menu = menu_bar.addMenu('Plik')
        exit_action = QAction('Wyjdź', self)
        exit_action.triggered.connect(self.close)
        file_menu.addAction(exit_action)

        edit_menu = menu_bar.addMenu('Edycja')
        clear_action = QAction('Wyczyść', self)
        clear_action.triggered.connect(self.clear_display)
        edit_menu.addAction(clear_action)

        settings_menu = menu_bar.addMenu('Opcje')
        settings_action = QAction('Ustawienia', self)
        settings_action.triggered.connect(self.open_settings_window)
        settings_menu.addAction(settings_action)

        help_menu = menu_bar.addMenu('Pomoc')
        about_action = QAction('Informacje o...', self)
        about_action.triggered.connect(self.show_about)
        help_menu.addAction(about_action)

    def clear_display(self):
        if self.content_stack.currentWidget() == self.standard_frame_page:
            self.standard_display.clear()
        elif self.content_stack.currentWidget() == self.scientific_frame_page:
            self.scientific_display.clear()

    def open_settings_window(self):
        self.settings_window = SettingsWindow(self)
        self.settings_window.exec_()

    def show_about(self):
        about_dialog = QLabel("Kalkulator")
        about_dialog.setWindowTitle("Kalkulator")
        about_dialog.setAlignment(Qt.AlignCenter)
        about_dialog.setFixedSize(300, 150)
        about_dialog.show()

    def on_button_click(self, button_text):
        print(f"Wysłano przycisk: {button_text}")
        self.button_clicked.emit(button_text)



