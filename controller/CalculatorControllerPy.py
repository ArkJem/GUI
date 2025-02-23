import csv
import sys
from datetime import datetime

from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QTableWidgetItem, QFileDialog, QMessageBox

from components.functions import read_yaml
from model.CalculatorModelPy import CalculatorModelPy
from view.CalculatorViewPy import CalculatorViewPy

DATE_FORMAT_MAPPING = {
    "R-M-D G:M:S": "%Y-%m-%d %H:%M:%S",
    "D-M-R G:M:S": "%d-%m-%Y %H:%M:%S",
    "R/M/D": "%Y/%m/%d",
    "D/M/R": "%d/%m/%Y",
    "M-D-R": "%m-%d-%Y",
}

class CalculatorControllerPy:
    def __init__(self):
        self.app = QApplication(sys.argv)
        self.view = CalculatorViewPy()
        self.model = CalculatorModelPy()
        self.setup_connections()
        self.history = []
        self.headers = ["Data", "Wyrażenie", "Wynik"]
        self.date_format = read_yaml("dateFormat")
        self.set_global_font()



        if self.date_format in DATE_FORMAT_MAPPING:
            self.date_format = DATE_FORMAT_MAPPING[self.date_format]
        else:
            print(f"Nieprawidłowy format daty: {self.date_format}. Przypisano wartości domyślne.")
            self.date_format = "%Y-%m-%d %H:%M:%S"

    def set_global_font(self):
        font_config = read_yaml("font")

        if isinstance(font_config, str):
            font_family = font_config
            font_size = 10
        else:
            font_family = "Arial"
            font_size = 10

        font = QFont(font_family, font_size)
        QApplication.setFont(font)

    def setup_connections(self):
        self.view.button_clicked.connect(self.command_router)

    def command_router(self, command):
        print(f"Otrzymana komenda {command}")

        if command == "=":
            current_display = self.get_current_display()
            try:
                result = self.model.eval_trig(current_display)
                self.update_display(str(result))
                timestamp = datetime.now().strftime("%H:%M:%S %d-%m-%Y")
                row_position = self.view.history_table.rowCount()
                self.view.history_table.insertRow(row_position)
                self.view.history_table.setItem(row_position, 0, QTableWidgetItem(timestamp))
                self.view.history_table.setItem(row_position, 1, QTableWidgetItem(current_display))
                self.view.history_table.setItem(row_position, 2, QTableWidgetItem(str(result)))

            except Exception as e:
                self.update_display("Nieznany błąd")
        elif command == "%":
            current_display = self.get_current_display()
            try:
                result = eval(current_display) / 100
                self.update_display(str(result))
            except Exception:
                self.update_display("Nieznany błąd")

        elif command == "<-":
            self.delete_last_character()

        elif command in ["sin", "cos", "tan", "ln", "log"]:
            current_display = self.get_current_display()
            try:
                if command == "sin":
                    result = self.model.eval_trig(f"sin({current_display})")
                elif command == "cos":
                    result = self.model.eval_trig(f"cos({current_display})")
                elif command == "tan":
                    result = self.model.eval_trig(f"tan({current_display})")
                elif command == "ln":
                    result = self.model.eval_trig(f"ln({current_display})")
                elif command == "log":
                    result = self.model.eval_trig(f"log10({current_display})")
                self.update_display(str(result))
            except Exception:
                self.update_display("Nieznany błąd")

        elif command == "MS":
            current_display = self.get_current_display()
            try:
                self.model.save_to_memory(current_display)
                self.view.memory_widget.setText(f"Memory: {current_display}")
            except Exception as e:
                self.view.memory_widget.setText("Memory: Error")

        elif command == "MR":
            memory_value = self.model.recall_memory()
            if memory_value is not None:
                self.update_display(str(memory_value))
                self.view.memory_widget.setText(f"Wartość: {memory_value}")
            else:
                self.view.memory_widget.setText("Wartość: brak")

        elif command == "MC":
            self.model.clear_memory()
            self.view.memory_widget.setText("Wartość")

        elif command == "M+":
            current_display = self.get_current_display()
            try:
                self.model.add_to_memory(current_display)
                memory_value = self.model.recall_memory()
                self.view.memory_widget.setText(f"Wartość: {memory_value}")
            except Exception:
                self.view.memory_widget.setText("Wartość: Błąd")

        elif command == "M-":
            current_display = self.get_current_display()
            try:
                self.model.subtract_from_memory(current_display)
                memory_value = self.model.recall_memory()
                self.view.memory_widget.setText(f"Wartość: {memory_value}")
            except Exception:
                self.view.memory_widget.setText("Wartość: Błąd")
        elif command == "C":
            self.clear_display()
        elif command == "<-":
            self.delete_last_character()
        elif command == "SAVE_HISTORY":
            self.save_history()
        elif command == "EXPORT_CSV":
            self.export_history_to_csv()
        elif command == "CLEAR_HISTORY":
            self.clear_history()
        else:
            self.append_to_expression(command)

    def clear_display(self):
        self.update_display("")

    def save_history(self):
        if self.view.history_table.rowCount() == 0:
            QMessageBox.information(self.view, "Eksport do pliku tekstowego", "Brak wyrażeń do eksportowania")
            return

        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Zapisz historię do pliku",
            "PlikTXT.txt",
            "Text Files (*.txt);;All Files (*)",
            options=options
        )
        if not file_path:
            return

        try:
            with open(file_path, "w") as file:
                file.write(" | ".join(self.headers) + "\n")

                for timestamp, expression, result in self.history:
                    formatted_date = datetime.strptime(timestamp, "%Y-%m-%d %H:%M:%S").strftime(self.date_format)
                    file.write(f"{formatted_date} | {expression} | {result}\n")

            QMessageBox.information(self.view, "Zapisano", f"Poprawnie zapisano historię do pliku:\n{file_path}")
        except Exception as e:
            QMessageBox.critical(self.view, "Błąd zapisu", f"Wystąpił błąd podczas zapisu: {e}")

    def export_history_to_csv(self):
        if self.view.history_table.rowCount() == 0:
            QMessageBox.information(self.view, "eksport do pliku CSV", "Brak .")
            return
        options = QFileDialog.Options()
        file_path, _ = QFileDialog.getSaveFileName(
            self.view,
            "Eksprotowanie pliku CSV",
            "PlikCSV.csv",
            "CSV Files (*.csv);;All Files (*)",
            options=options
        )
        if file_path:
            try:
                with open(file_path, mode='w', newline='', encoding='utf-8') as file:
                    writer = csv.writer(file)

                    headers = [self.view.history_table.horizontalHeaderItem(i).text()
                               for i in range(self.view.history_table.columnCount())]
                    writer.writerow(headers)

                    for row in range(self.view.history_table.rowCount()):
                        row_data = [
                            datetime.strptime(self.view.history_table.item(row, 0).text(),
                                              "%Y-%m-%d %H:%M:%S").strftime(self.date_format)
                            if col == 0 and self.view.history_table.item(row, 0) is not None else
                            self.view.history_table.item(row, col).text()
                            if self.view.history_table.item(row, col) is not None else ""
                            for col in range(self.view.history_table.columnCount())
                        ]
                        writer.writerow(row_data)

                print(f"Poprawnie zapisano {file_path}")
            except Exception as e:
                print(f"Błąd zapisu CSV: {e}")

    def calculate_result(self):
        current_display = self.get_current_display()
        try:
            result = self.model.eval_trig(current_display)
            self.update_display(result)
        except Exception as e:
            self.update_display("Nieznany błąd")

    def clear_history(self):
        self.view.history_table.setRowCount(0)
        self.history = []

    def delete_last_character(self):
        current_display = self.get_current_display()
        self.update_display(current_display[:-1])

    def append_to_expression(self, char):
        current_display = self.get_current_display()
        self.update_display(current_display + char)

    def get_current_display(self):
        if self.view.content_stack.currentWidget() == self.view.standard_frame_page:
            return self.view.standard_display.text()
        elif self.view.content_stack.currentWidget() == self.view.scientific_frame_page:
            return self.view.scientific_display.text()
        return ""

    def update_display(self, text):
        if self.view.content_stack.currentWidget() == self.view.standard_frame_page:
            self.view.standard_display.setText(text)
        elif self.view.content_stack.currentWidget() == self.view.scientific_frame_page:
            self.view.scientific_display.setText(text)

    def run(self):
        self.view.show()
        sys.exit(self.app.exec_())


if __name__ == "__main__":
    controller = CalculatorControllerPy()
    controller.run()