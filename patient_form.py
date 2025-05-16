from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                               QLineEdit, QDateEdit, QComboBox, QSpinBox, 
                               QDoubleSpinBox, QTextEdit, QCheckBox, QPushButton,
                               QLabel, QGroupBox, QMessageBox)
from PyQt6.QtCore import Qt, QDate, pyqtSignal
import uuid
import re
import sqlite3

class PatientForm(QWidget):
    # Signal to notify main window when form needs to return
    return_to_main = pyqtSignal()
    
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.setup_database()
        
    def setup_database(self):
        self.conn = sqlite3.connect('patients.db')
        self.cursor = self.conn.cursor()
        
        # Create patients table if it doesn't exist
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS patients (
                id TEXT PRIMARY KEY,
                name TEXT NOT NULL,
                tc TEXT UNIQUE,
                gender TEXT,
                birth_date TEXT,
                phone TEXT,
                email TEXT,
                height INTEGER,
                weight REAL,
                foot_size INTEGER,
                dominant_foot TEXT,
                gait_type TEXT,
                posture_type TEXT,
                clinical_notes TEXT,
                surgery INTEGER,
                heel_spur INTEGER,
                hallux INTEGER,
                pes_planus INTEGER,
                pes_cavus INTEGER
            )
        ''')
        self.conn.commit()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
        # Navigation buttons
        nav_layout = QHBoxLayout()
        back_button = QPushButton("← Ana Menü")
        back_button.clicked.connect(self.return_to_main.emit)
        nav_layout.addWidget(back_button)
        nav_layout.addStretch()
        layout.addLayout(nav_layout)
        
        # Basic Information
        basic_group = QGroupBox("Temel Bilgiler")
        basic_layout = QFormLayout()
        
        self.name_edit = QLineEdit()
        self.tc_edit = QLineEdit()
        self.tc_edit.setMaxLength(11)
        self.tc_edit.setPlaceholderText("11 haneli TC kimlik no")
        
        self.gender_combo = QComboBox()
        self.gender_combo.addItems(["Erkek", "Kadın", "Diğer"])
        
        self.birth_date = QDateEdit()
        self.birth_date.setDisplayFormat("dd.MM.yyyy")
        self.birth_date.setMaximumDate(QDate.currentDate())
        self.birth_date.setCalendarPopup(True)
        
        self.phone_edit = QLineEdit()
        self.phone_edit.setPlaceholderText("05XX XXX XX XX")
        self.email_edit = QLineEdit()
        self.email_edit.setPlaceholderText("ornek@email.com")
        
        basic_layout.addRow("Ad Soyad:", self.name_edit)
        basic_layout.addRow("T.C. Kimlik No:", self.tc_edit)
        basic_layout.addRow("Cinsiyet:", self.gender_combo)
        basic_layout.addRow("Doğum Tarihi:", self.birth_date)
        basic_layout.addRow("Telefon:", self.phone_edit)
        basic_layout.addRow("E-posta:", self.email_edit)
        basic_group.setLayout(basic_layout)
        
        # Clinical Information
        clinical_group = QGroupBox("Klinik Bilgiler")
        clinical_layout = QFormLayout()
        
        self.height_spin = QSpinBox()
        self.height_spin.setRange(100, 250)
        self.height_spin.setSuffix(" cm")
        
        self.weight_spin = QDoubleSpinBox()
        self.weight_spin.setRange(20, 250)
        self.weight_spin.setSuffix(" kg")
        
        self.foot_size_spin = QSpinBox()
        self.foot_size_spin.setRange(30, 50)
        
        self.dominant_foot = QComboBox()
        self.dominant_foot.addItems(["Sağ", "Sol"])
        
        self.gait_type = QComboBox()
        self.gait_type.addItems(["Normal", "Supinasyon", "Pronasyon"])
        
        self.posture_type = QComboBox()
        self.posture_type.addItems(["Normal", "Lordoz", "Kifoz", "Skolyoz"])
        
        self.clinical_notes = QTextEdit()
        
        clinical_layout.addRow("Boy:", self.height_spin)
        clinical_layout.addRow("Kilo:", self.weight_spin)
        clinical_layout.addRow("Ayak Numarası:", self.foot_size_spin)
        clinical_layout.addRow("Dominant Ayak:", self.dominant_foot)
        clinical_layout.addRow("Yürüyüş Tipi:", self.gait_type)
        clinical_layout.addRow("Postür Tipi:", self.posture_type)
        clinical_layout.addRow("Klinik Notlar:", self.clinical_notes)
        clinical_group.setLayout(clinical_layout)
        
        # Orthopedic Conditions
        ortho_group = QGroupBox("Ortopedik Durum")
        ortho_layout = QVBoxLayout()
        
        self.surgery_check = QCheckBox("Geçmiş ayak/omurga cerrahisi")
        self.heel_spur_check = QCheckBox("Topuk dikeni")
        self.hallux_check = QCheckBox("Halluks valgus")
        self.pes_planus_check = QCheckBox("Pes planus (düz taban)")
        self.pes_cavus_check = QCheckBox("Pes cavus (yüksek ark)")
        
        ortho_layout.addWidget(self.surgery_check)
        ortho_layout.addWidget(self.heel_spur_check)
        ortho_layout.addWidget(self.hallux_check)
        ortho_layout.addWidget(self.pes_planus_check)
        ortho_layout.addWidget(self.pes_cavus_check)
        ortho_group.setLayout(ortho_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_patient)
        
        clear_button = QPushButton("Formu Temizle")
        clear_button.clicked.connect(self.clear_form)
        
        button_layout.addWidget(clear_button)
        button_layout.addWidget(save_button)
        
        # Add all groups to main layout
        layout.addWidget(basic_group)
        layout.addWidget(clinical_group)
        layout.addWidget(ortho_group)
        layout.addLayout(button_layout)
        
        self.setLayout(layout)
        
    def validate_tc(self, tc):
        if not tc.isdigit() or len(tc) != 11:
            return False
        return True
        
    def validate_phone(self, phone):
        phone_pattern = re.compile(r'^05\d{9}$')
        return bool(phone_pattern.match(phone.replace(" ", "")))
        
    def validate_email(self, email):
        email_pattern = re.compile(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$')
        return bool(email_pattern.match(email))
        
    def validate_form(self):
        if not self.name_edit.text().strip():
            QMessageBox.warning(self, "Hata", "Ad Soyad alanı boş bırakılamaz!")
            return False
            
        tc = self.tc_edit.text().strip()
        if tc and not self.validate_tc(tc):
            QMessageBox.warning(self, "Hata", "Geçersiz TC Kimlik numarası!")
            return False
            
        phone = self.phone_edit.text().strip()
        if phone and not self.validate_phone(phone):
            QMessageBox.warning(self, "Hata", "Geçersiz telefon numarası!")
            return False
            
        email = self.email_edit.text().strip()
        if email and not self.validate_email(email):
            QMessageBox.warning(self, "Hata", "Geçersiz e-posta adresi!")
            return False
            
        return True
        
    def clear_form(self):
        self.name_edit.clear()
        self.tc_edit.clear()
        self.gender_combo.setCurrentIndex(0)
        self.birth_date.setDate(QDate.currentDate())
        self.phone_edit.clear()
        self.email_edit.clear()
        self.height_spin.setValue(170)
        self.weight_spin.setValue(70)
        self.foot_size_spin.setValue(40)
        self.dominant_foot.setCurrentIndex(0)
        self.gait_type.setCurrentIndex(0)
        self.posture_type.setCurrentIndex(0)
        self.clinical_notes.clear()
        self.surgery_check.setChecked(False)
        self.heel_spur_check.setChecked(False)
        self.hallux_check.setChecked(False)
        self.pes_planus_check.setChecked(False)
        self.pes_cavus_check.setChecked(False)
        
    def save_patient(self):
        if not self.validate_form():
            return
            
        # Generate unique patient ID
        patient_id = str(uuid.uuid4())
        
        try:
            self.cursor.execute('''
                INSERT INTO patients VALUES (
                    ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?
                )
            ''', (
                patient_id,
                self.name_edit.text().strip(),
                self.tc_edit.text().strip(),
                self.gender_combo.currentText(),
                self.birth_date.date().toString("dd.MM.yyyy"),
                self.phone_edit.text().strip(),
                self.email_edit.text().strip(),
                self.height_spin.value(),
                self.weight_spin.value(),
                self.foot_size_spin.value(),
                self.dominant_foot.currentText(),
                self.gait_type.currentText(),
                self.posture_type.currentText(),
                self.clinical_notes.toPlainText().strip(),
                self.surgery_check.isChecked(),
                self.heel_spur_check.isChecked(),
                self.hallux_check.isChecked(),
                self.pes_planus_check.isChecked(),
                self.pes_cavus_check.isChecked()
            ))
            
            self.conn.commit()
            QMessageBox.information(self, "Başarılı", "Hasta kaydı başarıyla oluşturuldu!")
            self.clear_form()
            
        except sqlite3.IntegrityError as e:
            if "UNIQUE constraint failed: patients.tc" in str(e):
                QMessageBox.warning(self, "Hata", "Bu TC Kimlik numarası ile kayıtlı hasta bulunmaktadır!")
            else:
                QMessageBox.warning(self, "Hata", "Veritabanı hatası oluştu!")
        except Exception as e:
            QMessageBox.warning(self, "Hata", f"Beklenmeyen bir hata oluştu: {str(e)}")
            
    def closeEvent(self, event):
        self.conn.close()
        super().closeEvent(event)