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
    QLineEdit,
)

import csv




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

        self.add_points=QLineEdit()
        self.add_points.setPlaceholderText("נקודות בונוס")
        self.add_points.setFixedSize(100, 36) 
        self.add_points.returnPressed.connect(self.add_points_bonus)

        
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
        self.table_grid = QGridLayout(table)
        self.table_grid.setContentsMargins(0, 0, 0, 0)
        self.table_grid.setHorizontalSpacing(1)
        self.table_grid.setVerticalSpacing(1)
        self.table_grid.setColumnStretch(0, 1)
        self.table_grid.setColumnStretch(1, 1)

        student_id_header = QLabel("ID Student")
        student_id_header.setObjectName("tableHeader")
        student_id_header.setAlignment(Qt.AlignmentFlag.AlignCenter)

        grade_header = QLabel("Grade")
        grade_header.setObjectName("tableHeader")
        grade_header.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.rows_widget = []


        self.empty_state = QLabel("הטבלה מוכנה להצגת הנתונים")
        self.empty_state.setObjectName("tableEmptyState")
        self.empty_state.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.table_grid.addWidget(student_id_header, 0, 0)
        self.table_grid.addWidget(grade_header, 0, 1)
        self.table_grid.addWidget(self.empty_state, 1, 0, 1, 2)

        table_layout.addWidget(table_title)
        table_layout.addWidget(self.add_points)
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
        
        with open (self.selected_csv_path , mode="r" ,encoding="utf-8-sig" , newline="") as f:
            reader = csv.reader(f)
            next(reader , None)

            self.empty_state.hide()
            grid_row=1

            for row in reader: 
                if len(row)<2:
                    continue

                student_id = row[0].strip()
                grade = row[1].strip()

                id_label=QLabel(student_id)
                id_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                grade_label = QLabel(grade)
                grade_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

                self.table_grid.addWidget(id_label,grid_row , 0)
                self.table_grid.addWidget(grade_label , grid_row ,1)


                self.rows_widget.append((student_id,grade_label))

                grid_row+=1

    def add_points_bonus(self):    
        num_point=int(self.add_points.text())       
        for _,grade_label in self.rows_widget:
            new_grade = int(float(grade_label.text()))+num_point
            grade_label.setText(str(new_grade))
    




if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = Grade_Students()
    window.show()
    sys.exit(app.exec())
