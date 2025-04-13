from PyQt6.QtWidgets import (QDialog, QVBoxLayout, QHBoxLayout, QLabel,
                            QLineEdit, QTextEdit, QPushButton, QFileDialog)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap

class LessonCreationDialog(QDialog):
    def __init__(self, language: str):
        super().__init__()
        self.language = language
        self.image_path = ""
        self.video_path = ""
        self.init_ui()
        
    def init_ui(self):
        self.setWindowTitle("Create New Lesson")
        self.setMinimumSize(600, 800)
        self.setStyleSheet("""
            QDialog {
                background-color: #f0f2f5;
            }
            QLabel {
                color: #1a237e;
                font-size: 14px;
            }
            QLineEdit, QTextEdit {
                padding: 8px;
                border: 2px solid #b0bec5;
                border-radius: 4px;
                background-color: white;
                font-size: 14px;
            }
            QPushButton {
                background-color: #1a237e;
                color: white;
                border: none;
                padding: 10px;
                border-radius: 4px;
                font-size: 14px;
            }
            QPushButton:hover {
                background-color: #283593;
            }
        """)
        
        layout = QVBoxLayout(self)
        layout.setSpacing(20)
        
        # Title (English)
        self.title_en_label = QLabel("Title (English):")
        self.title_en_input = QLineEdit()
        layout.addWidget(self.title_en_label)
        layout.addWidget(self.title_en_input)
        
        # Title (Arabic)
        self.title_ar_label = QLabel("Title (Arabic):")
        self.title_ar_input = QLineEdit()
        layout.addWidget(self.title_ar_label)
        layout.addWidget(self.title_ar_input)
        
        # Description (English)
        self.desc_en_label = QLabel("Description (English):")
        self.desc_en_input = QTextEdit()
        layout.addWidget(self.desc_en_label)
        layout.addWidget(self.desc_en_input)
        
        # Description (Arabic)
        self.desc_ar_label = QLabel("Description (Arabic):")
        self.desc_ar_input = QTextEdit()
        layout.addWidget(self.desc_ar_label)
        layout.addWidget(self.desc_ar_input)
        
        # Image selection
        image_layout = QHBoxLayout()
        self.image_label = QLabel()
        self.image_label.setMinimumSize(200, 150)
        self.image_label.setStyleSheet("background-color: white; border: 2px solid #b0bec5; border-radius: 4px;")
        self.image_button = QPushButton("Select Image")
        self.image_button.clicked.connect(self.select_image)
        image_layout.addWidget(self.image_label)
        image_layout.addWidget(self.image_button)
        layout.addLayout(image_layout)
        
        # Video selection
        video_layout = QHBoxLayout()
        self.video_label = QLabel()
        self.video_button = QPushButton("Select Video")
        self.video_button.clicked.connect(self.select_video)
        video_layout.addWidget(self.video_label)
        video_layout.addWidget(self.video_button)
        layout.addLayout(video_layout)
        
        # Buttons
        button_layout = QHBoxLayout()
        self.cancel_button = QPushButton("Cancel")
        self.cancel_button.clicked.connect(self.reject)
        self.create_button = QPushButton("Create")
        self.create_button.clicked.connect(self.accept)
        button_layout.addWidget(self.cancel_button)
        button_layout.addWidget(self.create_button)
        layout.addLayout(button_layout)
        
        # Update text based on language
        self.update_text()
        
    def update_text(self):
        if self.language == "ar":
            self.setWindowTitle("إضافة درس جديد")
            self.title_en_label.setText("العنوان (بالإنجليزية):")
            self.title_ar_label.setText("العنوان (بالعربية):")
            self.desc_en_label.setText("الوصف (بالإنجليزية):")
            self.desc_ar_label.setText("الوصف (بالعربية):")
            self.image_button.setText("اختر صورة")
            self.video_button.setText("اختر فيديو")
            self.cancel_button.setText("إلغاء")
            self.create_button.setText("إنشاء")
        else:
            self.setWindowTitle("Create New Lesson")
            self.title_en_label.setText("Title (English):")
            self.title_ar_label.setText("Title (Arabic):")
            self.desc_en_label.setText("Description (English):")
            self.desc_ar_label.setText("Description (Arabic):")
            self.image_button.setText("Select Image")
            self.video_button.setText("Select Video")
            self.cancel_button.setText("Cancel")
            self.create_button.setText("Create")
            
    def select_image(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image",
            "",
            "Image Files (*.png *.jpg *.jpeg *.bmp *.gif)"
        )
        if file_name:
            self.image_path = file_name
            self.image_label.setPixmap(QPixmap(file_name).scaled(
                200, 150, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation
            ))
            
    def select_video(self):
        file_name, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            "",
            "Video Files (*.mp4 *.avi *.mov *.wmv)"
        )
        if file_name:
            self.video_path = file_name
            self.video_label.setText(file_name.split('/')[-1])
            
    def get_lesson_data(self):
        return {
            'title': self.title_en_input.text(),
            'title_ar': self.title_ar_input.text(),
            'description': self.desc_en_input.toPlainText(),
            'description_ar': self.desc_ar_input.toPlainText(),
            'image_path': self.image_path,
            'video_path': self.video_path
        } 