import os
from datetime import datetime

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QFont, QColor
from PyQt5.QtMultimedia import QSound
from PyQt5.QtWidgets import (
    QDialog, QFormLayout, QSpinBox, QCheckBox, QVBoxLayout,
    QPushButton, QHBoxLayout, QFrame, QLabel, QStackedWidget, QComboBox, QButtonGroup, QRadioButton, QColorDialog,
    QMessageBox, QSlider, QLineEdit, QFileDialog, QFontDialog
)

from components.functions import edit_yaml, read_yaml


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Ustawienia')
        self.setGeometry(200, 200, 600, 400)
        self.initUI()

    def initUI(self):
        main_layout = QHBoxLayout()


        self.menu_frame = QFrame()
        self.menu_frame.setFixedWidth(200)
        self.menu_layout = QVBoxLayout()
        self.menu_frame.setLayout(self.menu_layout)

        self.general_settings_button = QPushButton('Ogólne ustawienia')
        self.general_settings_button.clicked.connect(self.show_general_settings)
        self.menu_layout.addWidget(self.general_settings_button)

        self.appearance_button = QPushButton('Wygląd i zachowanie')
        self.appearance_button.clicked.connect(self.show_appearance_settings)
        self.menu_layout.addWidget(self.appearance_button)

        self.history_button = QPushButton('Ustawienia historii')
        self.history_button.clicked.connect(self.show_history_settings)
        self.menu_layout.addWidget(self.history_button)

        self.font_button = QPushButton('Kolor i rodzaj czcionki')
        self.font_button.clicked.connect(self.show_font_settings)
        self.menu_layout.addWidget(self.font_button)

        self.about_button = QPushButton('Autorzy')
        self.about_button.clicked.connect(self.show_about)
        self.menu_layout.addWidget(self.about_button)

        self.menu_layout.addStretch()

        self.content_stack = QStackedWidget()
        self.general_settings_page = self.create_general_settings_page()
        self.about_page = self.create_about_page()
        self.appearance_page = self.create_appearance_page()
        self.history_page = self.create_history_page()
        self.font_page = self.create_font_page()


        self.content_stack.addWidget(self.general_settings_page)
        self.content_stack.addWidget(self.about_page)
        self.content_stack.addWidget(self.appearance_page)
        self.content_stack.addWidget(self.history_page)
        self.content_stack.addWidget(self.font_page)
        self.content_stack.setCurrentWidget(self.general_settings_page)

        main_layout.addWidget(self.menu_frame)
        main_layout.addWidget(self.content_stack)

        self.setLayout(main_layout)

    def create_general_settings_page(self):
        frame = QFrame()
        layout = QFormLayout()

        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setRange(0, 10)
        set_prec = read_yaml("calculationPrecision")
        self.precision_spinbox.setValue(int(set_prec))
        layout.addRow('Precyzja obliczeń:', self.precision_spinbox)

        self.sound_checkbox = QCheckBox('Włącz dźwięk klawiszy')
        self.sound_checkbox.setChecked(True)
        layout.addRow(self.sound_checkbox)

        self.volume_slider = QSlider(Qt.Horizontal)
        self.volume_slider.setRange(0, 100)
        self.volume_slider.setValue(50)
        self.volume_slider.setEnabled(self.sound_checkbox.isChecked())
        layout.addRow('Głośność dźwięku:', self.volume_slider)


        self.sound_file_label = QLabel("Plik dźwiękowy:")
        self.sound_file_button = QPushButton("Wybierz plik")
        self.sound_file_path = QLineEdit()
        self.sound_file_path.setReadOnly(True)


        sound_file_layout = QHBoxLayout()
        sound_file_layout.addWidget(self.sound_file_path)
        sound_file_layout.addWidget(self.sound_file_button)
        layout.addRow(self.sound_file_label, sound_file_layout)

        self.sound_file_name_label = QLabel("")
        layout.addRow(QLabel("Nazwa pliku dźwiękowego:"), self.sound_file_name_label)

        saved_sound_file_path = read_yaml("soundFilePath")
        if saved_sound_file_path:
            sound_file_name = os.path.basename(saved_sound_file_path)
            self.sound_file_path.setText(sound_file_name)

        def toggle_sound_settings():
            self.volume_slider.setEnabled(self.sound_checkbox.isChecked())
            self.sound_file_button.setEnabled(self.sound_checkbox.isChecked())

        self.sound_checkbox.stateChanged.connect(toggle_sound_settings)

        def choose_sound_file():
            file_dialog = QFileDialog()
            file_path, _ = file_dialog.getOpenFileName(
                frame, "Wybierz plik dźwiękowy", "", "Pliki dźwiękowe (*.wav)"
            )
            if file_path:
                self.sound_file_path.setText(file_path)

        self.sound_file_button.clicked.connect(choose_sound_file)

        saved_sound_file_path = read_yaml("soundFilePath")
        if saved_sound_file_path:
            sound_file_name = os.path.basename(saved_sound_file_path)
            self.sound_file_path.setText(saved_sound_file_path)
            self.sound_file_name_label.setText(sound_file_name)

        test_sound_button = QPushButton("Przetestuj dźwięk")
        layout.addRow(test_sound_button)

        def test_sound():
            if not self.sound_checkbox.isChecked():
                QMessageBox.warning(frame, "Brak dźwięku", "Opcja dźwięku jest wyłączona.")
                return

            sound_path = self.sound_file_path.text()
            if not sound_path:
                QMessageBox.warning(frame, "Brak pliku", "Wybierz plik dźwiękowy przed testowaniem.")
                return

            try:
                sound = QSound(sound_path)
                sound.play()
            except Exception as e:
                QMessageBox.critical(frame, "Błąd", f"Nie udało się odtworzyć dźwięku: {str(e)}")

        test_sound_button.clicked.connect(test_sound)

        save_settings_general_button = QPushButton('Zapisz Ustawienia')
        layout.addRow(save_settings_general_button)

        reset_button = QPushButton('Resetuj ustawienia')
        layout.addRow(reset_button)

        def reset_settings():
            reply = QMessageBox.question(
                frame,
                'Resetuj ustawienia',
                'Czy na pewno chcesz zresetować wszystkie ustawienia?',
                QMessageBox.Yes | QMessageBox.No
            )
            if reply == QMessageBox.Yes:
                self.precision_spinbox.setValue(2)
                self.sound_checkbox.setChecked(True)
                self.volume_slider.setValue(50)
                self.sound_file_path.clear()
                QMessageBox.information(frame, 'Reset', 'Ustawienia zostały zresetowane!')

        reset_button.clicked.connect(reset_settings)

        save_settings_general_button.clicked.connect(self.save_general_settings)

        frame.setLayout(layout)
        return frame

    def save_general_settings(self):

        precision = self.precision_spinbox.value()
        sound_file_path = self.sound_file_path.text()

        reply = QMessageBox.question(
            self,
            "Zapisz ustawienia",
            f"Czy na pewno chcesz zapisać ustawienia?\nPrecyzja: {precision}\nŚcieżka dźwięku: {sound_file_path}",
            QMessageBox.Yes | QMessageBox.No
        )

        if reply == QMessageBox.Yes:
            try:
                edit_yaml('calculationPrecision', precision)
                edit_yaml('soundFilePath', sound_file_path)

                QMessageBox.information(self, "Zapisano",
                                        f"Ustawienia zostały zapisane:\nPrecyzja: {precision}\nŚcieżka dźwięku: {sound_file_path}")
            except Exception as e:
                QMessageBox.critical(self, "Błąd", f"Nie udało się zapisać ustawień: {str(e)}")


    def create_about_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        about_label = QLabel('Wykonane przez Arkadiusza Jemioło')
        layout.addWidget(about_label)

        frame.setLayout(layout)
        return frame

    def create_appearance_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        appearance_label = QLabel('Wybierz motyw kalkulatora')
        appearance_label.setAlignment(Qt.AlignCenter)
        appearance_label.setStyleSheet("font-size: 14px; font-weight: bold;")
        layout.addWidget(appearance_label)

        preview_label = QLabel('Podgląd motywu')
        preview_label.setAlignment(Qt.AlignCenter)
        preview_label.setStyleSheet("background-color: white; border: 1px solid black; padding: 20px;")
        layout.addWidget(preview_label)

        choose_color_button = QPushButton("Wybierz kolor tła")
        layout.addWidget(choose_color_button)

        selected_color = QColor("white")

        save_button = QPushButton("Zapisz motyw")
        layout.addWidget(save_button)

        success_label = QLabel("")
        success_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(success_label)

        def choose_color():
            nonlocal selected_color
            color = QColorDialog.getColor()
            if color.isValid():
                selected_color = color
                preview_label.setStyleSheet(f"background-color: {color.name()}; border: 1px solid black; padding: 20px;")

        choose_color_button.clicked.connect(choose_color)

        def save_theme():
            if selected_color.isValid():
                edit_yaml("backgroundColor", selected_color.name())
                success_label.setText(f"Zapisano motyw z kolorem: {selected_color.name()}")
                success_label.setStyleSheet("color: green;")
            else:
                success_label.setText("Nie wybrano koloru!")
                success_label.setStyleSheet("color: red;")

        save_button.clicked.connect(save_theme)

        frame.setLayout(layout)
        return frame

    def create_history_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        history_label = QLabel('Historia obliczeń')
        layout.addWidget(history_label)

        self.show_date_checkbox = QCheckBox('Pokazuj datę w historii')
        self.show_date_checkbox.setChecked(True)
        layout.addWidget(self.show_date_checkbox)

        date_format_label = QLabel('Wybierz format daty:')
        layout.addWidget(date_format_label)

        date_format_options = [
            "R-M-D G:M:S",
            "D-M-R G:M:S",
            "R/M/D",
            "D/M/R",
            "M-D-R",
        ]
        self.date_format_dropdown = QComboBox()
        self.date_format_dropdown.addItems(date_format_options)
        layout.addWidget(self.date_format_dropdown)

        save_button = QPushButton("Zapisz ustawienia historii")
        layout.addWidget(save_button)

        success_label = QLabel("")
        layout.addWidget(success_label)

        def save_history_settings():
            show_date = self.show_date_checkbox.isChecked()
            edit_yaml('showDateInHistory', show_date)

            selected_format = self.date_format_dropdown.currentText()
            edit_yaml('dateFormat', selected_format)

            success_label.setText(f"Ustawienia historii zapisane.")
            success_label.setStyleSheet("color: green;")
            success_label.setAlignment(Qt.AlignCenter)

        save_button.clicked.connect(save_history_settings)

        frame.setLayout(layout)
        return frame

    def create_font_page(self):
        frame = QFrame()
        layout = QVBoxLayout()

        font_label = QLabel('Wybierz czcionkę i kolor tekstu')
        font_label.setFont(QFont("Arial", 14))
        layout.addWidget(font_label)

        example_label = QLabel('Przykład tekstu w wybranej czcionce')
        example_label.setFont(QFont("Arial", 12))
        example_label.setAlignment(Qt.AlignCenter)
        layout.addWidget(example_label)

        choose_font_button = QPushButton("Wybierz czcionkę")
        layout.addWidget(choose_font_button)

        selected_font = QFont("Arial")

        def choose_font():
            nonlocal selected_font
            font, ok = QFontDialog.getFont(selected_font, self, "Wybierz czcionkę")
            if ok:
                selected_font = font
                example_label.setFont(selected_font)

        choose_font_button.clicked.connect(choose_font)

        choose_color_button = QPushButton("Wybierz kolor tekstu")
        layout.addWidget(choose_color_button)

        selected_color = QColor("black")

        def choose_color():
            nonlocal selected_color
            color = QColorDialog.getColor(selected_color, self, "Wybierz kolor tekstu")
            if color.isValid():
                selected_color = color
                example_label.setStyleSheet(f"color: {color.name()};")

        choose_color_button.clicked.connect(choose_color)

        save_button = QPushButton("Zapisz ustawienia czcionki")
        layout.addWidget(save_button)

        success_label = QLabel("")
        layout.addWidget(success_label)

        def save_font_settings():
            try:
                edit_yaml("font", selected_font.family())
                edit_yaml("fontColor", selected_color.name())
                success_label.setText(f"Zapisano czcionkę: {selected_font.family()}, Kolor: {selected_color.name()}")
                success_label.setStyleSheet("color: green;")
                success_label.setAlignment(Qt.AlignCenter)
            except Exception as e:
                success_label.setText(f"Błąd zapisu ustawień: {str(e)}")
                success_label.setStyleSheet("color: red;")
                success_label.setAlignment(Qt.AlignCenter)

        save_button.clicked.connect(save_font_settings)

        frame.setLayout(layout)
        return frame

    def show_general_settings(self):
        self.content_stack.setCurrentWidget(self.general_settings_page)


    def show_about(self):

        self.content_stack.setCurrentWidget(self.about_page)

    def show_appearance_settings(self):

        self.content_stack.setCurrentWidget(self.appearance_page)

    def show_history_settings(self):
        self.content_stack.setCurrentWidget(self.history_page)

    def show_font_settings(self):
        self.content_stack.setCurrentWidget(self.font_page)

