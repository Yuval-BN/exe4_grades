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
    QVBoxLayout,
    QWidget,
)
from PySide6.QtGui import QIntValidator, QPixmap


class AboutWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("About")

        layout = QVBoxLayout(self)

        image_label = QLabel()
        image_label.setPixmap(QPixmap())
        layout.addWidget(image_label)

        layout.addWidget(QLabel("Name: [Your Name]"))
        layout.addWidget(QLabel("GitHub: [GitHub Repository URL]"))

        close_button = QPushButton("Close")
        close_button.clicked.connect(self.close)
        layout.addWidget(close_button)


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

        about_button = QPushButton("About")
        about_button.clicked.connect(self.show_about)
        correction_layout.addWidget(about_button)
        layout.addLayout(correction_layout)

        self.table = QTableWidget(50, 3)
        self.table.setHorizontalHeaderLabels(
            ["ID", "Original Grades", "Corrected Grades"]
        )
        self.table.horizontalHeader().setSectionResizeMode(QHeaderView.Stretch)
        layout.addWidget(self.table)

        self.setCentralWidget(central_widget)

    def apply_correction(self):
        pass

    def update_file(self):
        pass

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


app = QApplication([])
window = MainWindow()
window.resize(800, 600)
window.show()
app.exec()
