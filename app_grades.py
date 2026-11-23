import os
import subprocess
import sys
from About import AboutWindow
import matplotlib.pyplot as plt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QHBoxLayout,
    QHeaderView,
    QLabel,
    QLineEdit,
    QMainWindow,
    QPushButton,
    QTableWidget,
    QTableWidgetItem,
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QIntValidator, QPixmap

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grades")

        with open("style.qss", "r") as f:
            self.setStyleSheet(f.read())

        self.student_ids = []
        self.original_grades = []
        self.corrected_grades = []
        self.selected_file = ""

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        layout.addWidget(load_button)

        correction_layout = QHBoxLayout()
        correction_layout.addWidget(QLabel("Correction points:"))
        self.correction_input = QLineEdit()
        self.correction_input.setValidator(QIntValidator(self))
        self.correction_input.returnPressed.connect(self.apply_correction)
        correction_layout.addWidget(self.correction_input)

        update_button = QPushButton("Update File")
        update_button.clicked.connect(self.update_file)
        correction_layout.addWidget(update_button)

        stats_button = QPushButton("Grade Breakdown")
        stats_button.clicked.connect(self.show_breakdown)
        correction_layout.addWidget(stats_button)

        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        correction_layout.addWidget(about_button)
        layout.addLayout(correction_layout)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        self.table.setEditTriggers(QTableWidget.NoEditTriggers)
        layout.addWidget(self.table)

        self.setCentralWidget(central_widget)

    def apply_correction(self):
        text = self.correction_input.text()
        if text == "" or text == "-":
            return

        points = int(text)
        self.corrected_grades = []

        for i in range(len(self.original_grades)):
            temp = self.original_grades[i] + points
            if temp > 100:
                temp = 100
            elif temp < 0:
                temp = 0
            self.corrected_grades.append(temp)

        self.update_table()
        

    def update_file(self):
        if not self.selected_file:
            return

        with open(self.selected_file, "w") as f:
            f.write("ID,Grade\n")
            for i in range(len(self.student_ids)):
                f.write(f"{self.student_ids[i]},{self.corrected_grades[i]}\n")

        self.open_file()

    def update_table(self):
        self.table.clearContents()
        for row, student_id in enumerate(self.student_ids):
            self.table.setItem(row, 0, QTableWidgetItem(str(student_id)))

            if row < len(self.original_grades):
                self.table.setItem(
                    row,
                    1,
                    QTableWidgetItem(str(self.original_grades[row])),
                )

            if row < len(self.corrected_grades):
                self.table.setItem(
                    row,
                    2,
                    QTableWidgetItem(str(self.corrected_grades[row])),
                )

    def open_file(self):
        if not self.selected_file:
            return

        if sys.platform == "win32":
            os.startfile(self.selected_file)
        elif sys.platform == "darwin":
            subprocess.Popen(["open", self.selected_file])
        else:
            subprocess.Popen(["xdg-open", self.selected_file])

    def show_about(self):
        self.about_window = AboutWindow()
        self.about_window.show()

    def load_data(self):
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data",
            "",
            "CSV files (*.csv)",
        )
        if selected_file:
            self.selected_file = selected_file
            self.student_ids = []
            self.original_grades = []
            self.corrected_grades = []

            with open(self.selected_file, "r") as f:
                lines = f.readlines()

            for i in range(1, len(lines)):
                line = lines[i].strip()
                if line:
                    temp = line.split(",")
                    self.student_ids.append(temp[0])
                    grade = int(temp[1])
                    self.original_grades.append(grade)
                    self.corrected_grades.append(grade)

            self.update_table()

    def show_breakdown(self):
        if not self.corrected_grades:
            return

        counts = [0, 0, 0, 0, 0]
        labels = ["< 60", "60-69", "70-79", "80-89", "90-100"]

        for i in range(len(self.corrected_grades)):
            temp = self.corrected_grades[i]
            if temp < 60:
                counts[0] += 1
            elif temp < 70:
                counts[1] += 1
            elif temp < 80:
                counts[2] += 1
            elif temp < 90:
                counts[3] += 1
            else:
                counts[4] += 1
        plt.figure("Grade Distribution")
        plt.bar(labels, counts)
        plt.xlabel("Grade Range")
        plt.ylabel("Number of Students")
        plt.title("Grade Distribution")
        plt.yticks(range(0, max(counts) + 2))
        plt.show()

app = QApplication([])
window = MainWindow()
window.resize(800, 600)
window.show()
app.exec()
