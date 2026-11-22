import os
import sys

from PySide6.QtCore import QTimer, Qt
from PySide6.QtWidgets import (
    QApplication,
    QFileDialog,
    QGridLayout,
    QLabel,
    QPushButton,
    QScrollArea,
    QVBoxLayout,
    QWidget,
)


class Grade_Students(QWidget):
    def __init__(self):
        super().__init__()

        self.selected_csv_path = ""
        self.setWindowTitle("מערכת ציוני תלמידים")
        self.resize(1000, 720)
        self.setMinimumSize(720, 560)

        self.scroll_area = QScrollArea(self)               #מיקום גלילה אוטמטיS
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setObjectName("pageScroll")

        page = QWidget()
        page.setObjectName("page")
        page_layout = QVBoxLayout(page)
        page_layout.setContentsMargins(48, 40, 48, 48)
        page_layout.setSpacing(28)

        welcome_card = QWidget()
        welcome_card.setObjectName("welcomeCard")
        welcome_layout = QVBoxLayout(welcome_card)
        welcome_layout.setContentsMargins(44, 42, 44, 42)
        welcome_layout.setSpacing(16)

        eyebrow = QLabel("מערכת ניהול ציונים")
        eyebrow.setObjectName("eyebrow")
        eyebrow.setAlignment(Qt.AlignmentFlag.AlignCenter)

        title = QLabel("ברוך הבא למערכת ציוני תלמידים")
        title.setObjectName("welcomeTitle")
        title.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title.setWordWrap(True)

        description = QLabel("בחר קובץ CSV כדי לפתוח את טבלת הציונים.")
        description.setObjectName("welcomeDescription")
        description.setAlignment(Qt.AlignmentFlag.AlignCenter)
        description.setWordWrap(True)

        self.upload_button = QPushButton("בחירת קובץ CSV")
        self.upload_button.setObjectName("uploadButton")
        self.upload_button.setCursor(Qt.CursorShape.PointingHandCursor)
        self.upload_button.clicked.connect(self.choose_csv_file)

        self.file_status_label = QLabel("")
        self.file_status_label.setObjectName("fileStatus")
        self.file_status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.file_status_label.hide()

        welcome_layout.addWidget(eyebrow)
        welcome_layout.addWidget(title)
        welcome_layout.addWidget(description)
        welcome_layout.addSpacing(8)
        welcome_layout.addWidget(self.upload_button, alignment=Qt.AlignmentFlag.AlignCenter)
        welcome_layout.addWidget(self.file_status_label)

        self.table_card = QWidget()
        self.table_card.setObjectName("tableCard")
        self.table_card.hide()
        table_layout = QVBoxLayout(self.table_card)
        table_layout.setContentsMargins(28, 28, 28, 28)
        table_layout.setSpacing(18)

        table_title = QLabel("טבלת ציונים")
        table_title.setObjectName("tableTitle")
        table_title.setAlignment(Qt.AlignmentFlag.AlignRight)

        table = QWidget()
        table.setObjectName("gradesTable")
        table.setLayoutDirection(Qt.LayoutDirection.LeftToRight)
        table_grid = QGridLayout(table)
        table_grid.setContentsMargins(0, 0, 0, 0)
        table_grid.setHorizontalSpacing(1)
        table_grid.setVerticalSpacing(1)
        table_grid.setColumnStretch(0, 1)
        table_grid.setColumnStretch(1, 1)

        student_id_header = QLabel("ID Student")
        student_id_header.setObjectName("tableHeader")
        student_id_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grade_header = QLabel("Grade")
        grade_header.setObjectName("tableHeader")
        grade_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        empty_state = QLabel("הטבלה מוכנה להצגת הנתונים")
        empty_state.setObjectName("tableEmptyState")
        empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)

        table_grid.addWidget(student_id_header, 0, 0)
        table_grid.addWidget(grade_header, 0, 1)
        table_grid.addWidget(empty_state, 1, 0, 1, 2)

        table_layout.addWidget(table_title)
        table_layout.addWidget(table)

        page_layout.addWidget(welcome_card)
        page_layout.addWidget(self.table_card)
        page_layout.addStretch(1)
        self.scroll_area.setWidget(page)

        window_layout = QVBoxLayout(self)
        window_layout.setContentsMargins(0, 0, 0, 0)
        window_layout.addWidget(self.scroll_area)

        stylesheet_path = os.path.join(os.path.dirname(__file__), "Grade students.qss")
        with open(stylesheet_path, encoding="utf-8") as stylesheet_file:
            self.setStyleSheet(stylesheet_file.read())

    def choose_csv_file(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "בחירת קובץ ציונים",
            "",
            "CSV files (*.csv)",
        )
        if not file_path:
            return

        self.selected_csv_path = file_path
        self.file_status_label.setText(f"קובץ נבחר: {os.path.basename(file_path)}")
        self.file_status_label.show()
        self.table_card.show()
        QTimer.singleShot(
            0,
            lambda: self.scroll_area.ensureWidgetVisible(self.table_card, 0, 16),
        )


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Grade_Students()
    window.show()
    sys.exit(app.exec())
