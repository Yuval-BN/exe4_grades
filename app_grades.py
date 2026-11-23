import csv
import sys
from pathlib import Path

from matplotlib.backends.backend_qtagg import FigureCanvasQTAgg
from matplotlib.figure import Figure
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QMainWindow,
    QPushButton,
    QVBoxLayout,
    QWidget,
)


class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Grades")
        self.filename = None

        central_widget = QWidget()
        layout = QVBoxLayout(central_widget)

        load_button = QPushButton("Load Data")
        load_button.clicked.connect(self.load_data)
        layout.addWidget(load_button)

        self.figure = Figure(figsize=(6, 4))
        self.canvas = FigureCanvasQTAgg(self.figure)
        layout.addWidget(self.canvas)

        self.setCentralWidget(central_widget)
        self.draw()

    def load_data(self):
        selected_file, _ = QFileDialog.getOpenFileName(
            self,
            "Load Data",
            "",
            "Data files (*.csv *.txt);;CSV files (*.csv);;Text files (*.txt);;All files (*)",
        )
        if selected_file:
            self.filename = selected_file
            self.draw()

    def draw(self):
        self.figure.clear()
        axes = self.figure.add_subplot(111)

        if self.filename:
            values = self._read_numeric_values(self.filename)
            if values:
                axes.hist(values, bins="auto", edgecolor="black")
                axes.set_title(Path(self.filename).name)
                axes.set_xlabel("Grade")
                axes.set_ylabel("Count")
            else:
                axes.text(
                    0.5,
                    0.5,
                    f"Could not find numeric data in:\n{self.filename}",
                    ha="center",
                    va="center",
                    transform=axes.transAxes,
                )
        else:
            axes.text(
                0.5,
                0.5,
                "Load a data file to display a graph",
                ha="center",
                va="center",
                transform=axes.transAxes,
            )

        self.figure.tight_layout()
        self.canvas.draw()

    @staticmethod
    def _read_numeric_values(filename):
        values = []

        try:
            with open(filename, "r", newline="", encoding="utf-8-sig") as data_file:
                reader = csv.reader(data_file)
                for row in reader:
                    for item in row:
                        try:
                            values.append(float(item.strip()))
                        except (AttributeError, ValueError):
                            continue
        except (OSError, UnicodeDecodeError):
            return []

        return values


def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(800, 600)
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    main()
