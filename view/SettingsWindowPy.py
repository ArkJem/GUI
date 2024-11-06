from PyQt5.QtWidgets import QDialog, QFormLayout, QSpinBox, QCheckBox


class SettingsWindow(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Settings')
        self.setGeometry(200, 200, 300, 200)
        self.initUI()

    def initUI(self):
        layout = QFormLayout()

        # Example settings options: precision control and sound toggle
        self.precision_spinbox = QSpinBox()
        self.precision_spinbox.setRange(0, 10)  # Set precision between 0 and 10 decimal places
        self.precision_spinbox.setValue(2)  # Default precision
        layout.addRow('Decimal Precision:', self.precision_spinbox)

        self.sound_checkbox = QCheckBox('Enable Sound')
        self.sound_checkbox.setChecked(True)  # Default is checked (sound enabled)
        layout.addRow(self.sound_checkbox)

        self.setLayout(layout)