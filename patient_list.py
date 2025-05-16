from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QTableWidget, 
                            QTableWidgetItem, QPushButton, QLineEdit, QLabel,
                            QMessageBox, QHeaderView)
from PyQt6.QtCore import Qt, pyqtSignal
import sqlite3
from contextlib import contextmanager

class DatabaseConnection:
    def __init__(self, db_name='patients.db'):
        self.db_name = db_name

    @contextmanager
    def connect(self):
        conn = sqlite3.connect(self.db_name)
        try:
            yield conn
        finally:
            conn.close()

class PatientList(QWidget):
    return_to_main = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.db = DatabaseConnection()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Navigation
        nav_layout = QHBoxLayout()
        back_button = QPushButton("← Ana Menü")
        back_button.clicked.connect(self.return_to_main.emit)
        nav_layout.addWidget(back_button)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
        
        # Search
        search_layout = QHBoxLayout()
        self.search_input = QLineEdit()
        self.search_input.setPlaceholderText("Hasta Ara (Ad, TC, Telefon)")
        self.search_input.textChanged.connect(self.filter_patients)
        search_layout.addWidget(self.search_input)
        layout.addLayout(search_layout)
        
        # Table
        self.table = QTableWidget()
        self.table.setColumnCount(7)
        self.table.setHorizontalHeaderLabels([
            "Ad Soyad", "TC No", "Telefon", "Cinsiyet", 
            "Doğum Tarihi", "Boy", "Kilo"
        ])
        header = self.table.horizontalHeader()
        header.setSectionResizeMode(0, QHeaderView.ResizeMode.Stretch)
        for i in range(1, 7):
            header.setSectionResizeMode(i, QHeaderView.ResizeMode.ResizeToContents)
        
        layout.addWidget(self.table)
        
        # Buttons
        button_layout = QHBoxLayout()
        edit_button = QPushButton("Düzenle")
        edit_button.clicked.connect(self.edit_patient)
        delete_button = QPushButton("Sil")
        delete_button.clicked.connect(self.delete_patient)
        button_layout.addWidget(edit_button)
        button_layout.addWidget(delete_button)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        self.load_patients()
        
    def load_patients(self):
        try:
            with self.db.connect() as conn:
                cursor = conn.cursor()
                cursor.execute('''
                    SELECT name, tc, phone, gender, birth_date, height, weight 
                    FROM patients ORDER BY name
                ''')
                patients = cursor.fetchall()
                
                self.table.setRowCount(len(patients))
                for row, patient in enumerate(patients):
                    for col, value in enumerate(patient):
                        item = QTableWidgetItem(str(value) if value else "")
                        self.table.setItem(row, col, item)
                        
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Hasta listesi yüklenirken hata: {str(e)}")
            
    def filter_patients(self):
        search_text = self.search_input.text().lower()
        for row in range(self.table.rowCount()):
            show_row = False
            for col in range(3):  # Search in name, TC, phone columns
                item = self.table.item(row, col)
                if item and search_text in item.text().lower():
                    show_row = True
                    break
            self.table.setRowHidden(row, not show_row)
            
    def edit_patient(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçin")
            return
            
        tc = self.table.item(current_row, 1).text()
        # TODO: Implement edit functionality
        QMessageBox.information(self, "Bilgi", f"{tc} TC nolu hasta düzenlenecek")
        
    def delete_patient(self):
        current_row = self.table.currentRow()
        if current_row < 0:
            QMessageBox.warning(self, "Uyarı", "Lütfen bir hasta seçin")
            return
            
        tc = self.table.item(current_row, 1).text()
        name = self.table.item(current_row, 0).text()
        
        reply = QMessageBox.question(self, "Onay", 
            f"{name} isimli hastayı silmek istediğinize emin misiniz?",
            QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
            
        if reply == QMessageBox.StandardButton.Yes:
            try:
                with self.db.connect() as conn:
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM patients WHERE tc = ?", (tc,))
                    conn.commit()
                    self.load_patients()
                    QMessageBox.information(self, "Başarılı", "Hasta kaydı silindi")
            except Exception as e:
                QMessageBox.warning(self, "Hata", f"Silme işlemi başarısız: {str(e)}")