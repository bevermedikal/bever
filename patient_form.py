from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QHBoxLayout, QFormLayout, 
                               QLineEdit, QDateEdit, QComboBox, QSpinBox, 
                               QDoubleSpinBox, QTextEdit, QCheckBox, QPushButton,
                               QLabel, QGroupBox)
from PyQt6.QtCore import Qt, QDate
import uuid

class PatientForm(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        
    def init_ui(self):
        layout = QVBoxLayout()
        
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
        self.email_edit = QLineEdit()
        
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
        
        # Save Button
        save_button = QPushButton("Kaydet")
        save_button.clicked.connect(self.save_patient)
        
        # Add all groups to main layout
        layout.addWidget(basic_group)
        layout.addWidget(clinical_group)
        layout.addWidget(ortho_group)
        layout.addWidget(save_button)
        
        self.setLayout(layout)
        
    def save_patient(self):
        # Generate unique patient ID
        patient_id = str(uuid.uuid4())
        
        # Collect patient data
        patient_data = {
            "id": patient_id,
            "name": self.name_edit.text(),
            "tc": self.tc_edit.text(),
            "gender": self.gender_combo.currentText(),
            "birth_date": self.birth_date.date().toString("dd.MM.yyyy"),
            "phone": self.phone_edit.text(),
            "email": self.email_edit.text(),
            "height": self.height_spin.value(),
            "weight": self.weight_spin.value(),
            "foot_size": self.foot_size_spin.value(),
            "dominant_foot": self.dominant_foot.currentText(),
            "gait_type": self.gait_type.currentText(),
            "posture_type": self.posture_type.currentText(),
            "clinical_notes": self.clinical_notes.toPlainText(),
            "conditions": {
                "surgery": self.surgery_check.isChecked(),
                "heel_spur": self.heel_spur_check.isChecked(),
                "hallux": self.hallux_check.isChecked(),
                "pes_planus": self.pes_planus_check.isChecked(),
                "pes_cavus": self.pes_cavus_check.isChecked()
            }
        }
        
        print("Patient data saved:", patient_data)
        # TODO: Implement database storage