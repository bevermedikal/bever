import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BEVER GAIT ANALYZER")
        self.setMinimumSize(1024, 768)
        
        # Main widget and layout
        main_widget = QWidget()
        self.setCentralWidget(main_widget)
        layout = QVBoxLayout(main_widget)
        
        # Logo and title
        title_label = QLabel("BEVER GAIT ANALYZER")
        title_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        title_label.setFont(QFont('Arial', 24, QFont.Weight.Bold))
        layout.addWidget(title_label)
        
        # Menu buttons
        buttons = [
            ("➕ Yeni Kayıt", self.new_patient),
            ("📁 Kayıtlı Hastalar", self.view_patients),
            ("⚙️ Sistem Ayarları", self.settings),
            ("📊 Raporlar", self.reports)
        ]
        
        for text, handler in buttons:
            btn = QPushButton(text)
            btn.setFont(QFont('Arial', 14))
            btn.setMinimumHeight(60)
            btn.clicked.connect(handler)
            layout.addWidget(btn)
            
        layout.addStretch()
        
    def new_patient(self):
        print("New Patient")
        
    def view_patients(self):
        print("View Patients")
        
    def settings(self):
        print("Settings")
        
    def reports(self):
        print("Reports")

def main():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())

if __name__ == '__main__':
    main()