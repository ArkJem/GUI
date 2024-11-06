#launcher.py
import sys
import subprocess
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton

class Launcher(QWidget):
    def __init__(self):
        super().__init__()
        self.initUI()

    def initUI(self):
        self.setWindowTitle("Launcher")
        self.setGeometry(100, 100, 300, 200)

        layout = QVBoxLayout()

        pyqt_button = QPushButton("Run PyQt Calculator")
        pyqt_button.clicked.connect(self.run_pyqt_calculator)
        layout.addWidget(pyqt_button)

        tkinter_button = QPushButton("Run Tkinter App")
        tkinter_button.clicked.connect(self.run_tkinter_app)
        layout.addWidget(tkinter_button)

        self.setLayout(layout)

    def run_pyqt_calculator(self):
        subprocess.Popen([sys.executable, "./controller/CalculatorControllerPy.py"])

    def run_tkinter_app(self):
        subprocess.Popen([sys.executable, "./controller/CalculatorControllerTk.py"])

if __name__ == "__main__":
    app = QApplication(sys.argv)
    launcher = Launcher()
    launcher.show()
    sys.exit(app.exec_())
