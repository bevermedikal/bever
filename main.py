import sys
from PyQt6.QtWidgets import QApplication, QMainWindow, QWidget, QVBoxLayout, QPushButton, QLabel, QStackedWidget
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon
from patient_form import PatientForm

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("BEVER GAIT ANALYZER")
        self.setMinimumSize(1024, 768)
        
        # Create stacked widget for multiple pages
        self.stacked_widget = QStackedWidget()
        self.setCentralWidget(self.stacked_widget)
        
        # Create main menu page
        self.main_menu = QWidget()
        self.setup_main_menu()
        self.stacked_widget.addWidget(self.main_menu)
        
        # Create patient form page
        self.patient_form = PatientForm()
        self.patient_form.return_to_main.connect(self.show_main_menu)
        self.stacked_widget.addWidget(self.patient_form)
        
    def setup_main_menu(self):
        layout = QVBoxLayout(self.main_menu)
        
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
        
    def show_main_menu(self):
        self.stacked_widget.setCurrentWidget(self.main_menu)
        
    def new_patient(self):
        self.stacked_widget.setCurrentWidget(self.patient_form)
        
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