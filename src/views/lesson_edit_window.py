from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QTextEdit, QFrame,
                            QFileDialog, QMessageBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QPixmap
from src.models.database import Database, User, Lesson
from src.utils.navigation import NavigationManager
from src.utils.file_manager import FileManager
import os

class LessonEditWindow(QMainWindow):
    def __init__(self, db: Database, user: User, lesson: Lesson):
        super().__init__()
        self.db = db
        self.user = user
        self.lesson = lesson
        self.nav_manager = NavigationManager()
        self.file_manager = FileManager()
        self.selected_video_path = lesson.video_path
        self.selected_image_path = lesson.image_path
        self.current_language = user.language  # Get language from user
        self.init_ui()
        # Set initial language
        self.update_ui_text()
        
    def init_ui(self):
        self.setWindowTitle('Educational Platform - Edit Lesson' if self.current_language == "en" else 'منصة التعليم - تعديل الدرس')
        self.setMinimumSize(1000, 800)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
                font-size: 14px;
            }
            QLabel#titleLabel {
                color: #89b4fa;
                font-size: 32px;
                font-weight: bold;
            }
            QLineEdit, QTextEdit {
                padding: 12px;
                border: 2px solid #313244;
                border-radius: 6px;
                background-color: #313244;
                color: #cdd6f4;
                font-size: 14px;
                selection-background-color: #45475a;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #89b4fa;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                padding: 12px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            QFrame {
                background-color: #313244;
                border-radius: 10px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title_label = QLabel("Edit Lesson" if self.current_language == "en" else "تعديل الدرس")
        title_label.setObjectName("titleLabel")
        main_layout.addWidget(title_label)
        
        # Form container
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title (English)
        title_label = QLabel("Title (English)" if self.current_language == "en" else "العنوان (بالإنجليزية)")
        self.title_input = QLineEdit()
        self.title_input.setText(self.lesson.title)
        form_layout.addWidget(title_label)
        form_layout.addWidget(self.title_input)
        
        # Title (Arabic)
        title_ar_label = QLabel("Title (Arabic)" if self.current_language == "en" else "العنوان (بالعربية)")
        self.title_ar_input = QLineEdit()
        self.title_ar_input.setText(self.lesson.title_ar)
        form_layout.addWidget(title_ar_label)
        form_layout.addWidget(self.title_ar_input)
        
        # Description (English)
        desc_label = QLabel("Description (English)" if self.current_language == "en" else "الوصف (بالإنجليزية)")
        self.desc_input = QTextEdit()
        self.desc_input.setText(self.lesson.description)
        self.desc_input.setMinimumHeight(100)
        form_layout.addWidget(desc_label)
        form_layout.addWidget(self.desc_input)
        
        # Description (Arabic)
        desc_ar_label = QLabel("Description (Arabic)" if self.current_language == "en" else "الوصف (بالعربية)")
        self.desc_ar_input = QTextEdit()
        self.desc_ar_input.setText(self.lesson.description_ar)
        self.desc_ar_input.setMinimumHeight(100)
        form_layout.addWidget(desc_ar_label)
        form_layout.addWidget(self.desc_ar_input)
        
        # Image selection
        image_section = QWidget()
        image_layout = QHBoxLayout(image_section)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        self.image_preview = QLabel()
        self.image_preview.setFixedSize(200, 150)
        self.image_preview.setStyleSheet("border: 2px solid #45475a; border-radius: 6px;")
        self.update_image_preview()
        
        image_button = QPushButton("Change Image" if self.current_language == "en" else "تغيير الصورة")
        image_button.clicked.connect(self.select_image)
        
        image_layout.addWidget(self.image_preview)
        image_layout.addWidget(image_button)
        image_layout.addStretch()
        
        form_layout.addWidget(QLabel("Lesson Image" if self.current_language == "en" else "صورة الدرس"))
        form_layout.addWidget(image_section)
        
        # Video selection
        video_section = QWidget()
        video_layout = QHBoxLayout(video_section)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        self.video_path_label = QLabel(self.lesson.video_path)
        self.video_path_label.setStyleSheet("color: #89b4fa;")
        
        video_button = QPushButton("Change Video" if self.current_language == "en" else "تغيير الفيديو")
        video_button.clicked.connect(self.select_video)
        
        video_layout.addWidget(self.video_path_label)
        video_layout.addWidget(video_button)
        
        form_layout.addWidget(QLabel("Lesson Video" if self.current_language == "en" else "فيديو الدرس"))
        form_layout.addWidget(video_section)
        
        # Add form to main layout
        main_layout.addWidget(form_frame)
        
        # Buttons
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        save_button = QPushButton("Save Changes" if self.current_language == "en" else "حفظ التغييرات")
        save_button.clicked.connect(self.save_lesson)
        
        cancel_button = QPushButton("Cancel" if self.current_language == "en" else "إلغاء")
        cancel_button.setStyleSheet("""
            QPushButton {
                background-color: #45475a;
            }
            QPushButton:hover {
                background-color: #585b70;
            }
        """)
        cancel_button.clicked.connect(self.close)
        
        button_layout.addWidget(save_button)
        button_layout.addWidget(cancel_button)
        
        main_layout.addWidget(button_container)
        
    def update_image_preview(self):
        """Update the image preview with the current image."""
        try:
            pixmap = QPixmap(self.selected_image_path)
            if not pixmap.isNull():
                self.image_preview.setPixmap(pixmap.scaled(
                    200, 150,
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                ))
            else:
                self.image_preview.setText("No image" if self.current_language == "en" else "لا توجد صورة")
        except:
            self.image_preview.setText("No image" if self.current_language == "en" else "لا توجد صورة")
            
    def select_image(self):
        """Open file dialog to select a new image."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Image" if self.current_language == "en" else "اختر صورة",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.selected_image_path = file_path
            self.update_image_preview()
            
    def select_video(self):
        """Open file dialog to select a new video."""
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video" if self.current_language == "en" else "اختر فيديو",
            "",
            "Video Files (*.mp4 *.avi *.mov)"
        )
        if file_path:
            self.selected_video_path = file_path
            self.video_path_label.setText(file_path)
            
    def save_lesson(self):
        """Save the modified lesson."""
        # Validate inputs
        title = self.title_input.text().strip()
        title_ar = self.title_ar_input.text().strip()
        description = self.desc_input.toPlainText().strip()
        description_ar = self.desc_ar_input.toPlainText().strip()
        
        if not all([title, title_ar, description, description_ar]):
            QMessageBox.warning(self, 
                              "Error" if self.current_language == "en" else "خطأ", 
                              "Please fill in all fields" if self.current_language == "en" else "يرجى ملء جميع الحقول")
            return
            
        # Save media files if changed
        if self.selected_image_path != self.lesson.image_path:
            new_image_path = self.file_manager.save_image(self.selected_image_path, self.lesson.id)
            if new_image_path:
                self.selected_image_path = new_image_path
            
        if self.selected_video_path != self.lesson.video_path:
            new_video_path = self.file_manager.save_video(self.selected_video_path, self.lesson.id)
            if new_video_path:
                self.selected_video_path = new_video_path
        
        # Update lesson
        updated_lesson = Lesson(
            id=self.lesson.id,
            title=title,
            title_ar=title_ar,
            description=description,
            description_ar=description_ar,
            image_path=self.selected_image_path,
            video_path=self.selected_video_path,
            created_by=self.lesson.created_by,
            created_at=self.lesson.created_at
        )
        
        if self.db.update_lesson(updated_lesson):
            QMessageBox.information(self, 
                                  "Success" if self.current_language == "en" else "نجاح", 
                                  "Lesson updated successfully" if self.current_language == "en" else "تم تحديث الدرس بنجاح")
            self.close()
            # Refresh the dashboard
            self.nav_manager.show_dashboard(self.user)
        else:
            QMessageBox.critical(self, 
                               "Error" if self.current_language == "en" else "خطأ", 
                               "Failed to update lesson" if self.current_language == "en" else "فشل تحديث الدرس")

    def update_ui_text(self):
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - تعديل الدرس')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("تعديل الدرس")
                elif widget.text() == "Title (English)":
                    widget.setText("العنوان (بالإنجليزية)")
                elif widget.text() == "Title (Arabic)":
                    widget.setText("العنوان (بالعربية)")
                elif widget.text() == "Description (English)":
                    widget.setText("الوصف (بالإنجليزية)")
                elif widget.text() == "Description (Arabic)":
                    widget.setText("الوصف (بالعربية)")
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "Save Changes":
                    button.setText("حفظ التغييرات")
                elif button.text() == "Cancel":
                    button.setText("إلغاء")
        else:
            self.setWindowTitle('Educational Platform - Edit Lesson')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("Edit Lesson")
                elif widget.text() == "العنوان (بالإنجليزية)":
                    widget.setText("Title (English)")
                elif widget.text() == "العنوان (بالعربية)":
                    widget.setText("Title (Arabic)")
                elif widget.text() == "الوصف (بالإنجليزية)":
                    widget.setText("Description (English)")
                elif widget.text() == "الوصف (بالعربية)":
                    widget.setText("Description (Arabic)")
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "حفظ التغييرات":
                    button.setText("Save Changes")
                elif button.text() == "إلغاء":
                    button.setText("Cancel") 