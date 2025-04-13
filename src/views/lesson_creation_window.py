from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QTextEdit, QFrame,
                            QFileDialog, QScrollArea, QMessageBox)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from src.models.database import Database, User, Lesson
from src.utils.navigation import NavigationManager
import os

class LessonCreationWindow(QMainWindow):
    def __init__(self, db: Database, user: User):
        super().__init__()
        self.db = db
        self.user = user
        self.nav_manager = NavigationManager()
        self.current_language = user.language  # Get language from user
        self.selected_video_path = None
        self.selected_image_path = None
        self.init_ui()
        # Set initial language
        self.update_ui_text()
        
    def init_ui(self):
        self.setWindowTitle('Educational Platform - Create Lesson')
        self.setMinimumSize(1200, 800)
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
            QLabel#subtitleLabel {
                color: #94e2d5;
                font-size: 16px;
            }
            QLineEdit, QTextEdit {
                padding: 12px;
                border: 2px solid #313244;
                border-radius: 8px;
                background-color: #313244;
                color: #cdd6f4;
                font-size: 14px;
                selection-background-color: #45475a;
            }
            QLineEdit:focus, QTextEdit:focus {
                border: 2px solid #89b4fa;
                background-color: #1e1e2e;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
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
            QPushButton#secondaryButton {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
            }
            QPushButton#secondaryButton:hover {
                background-color: #45475a;
                border-color: #89b4fa;
            }
            QFrame {
                background-color: #313244;
                border-radius: 12px;
            }
            QFrame#previewFrame {
                background-color: #181825;
                border: 2px solid #313244;
            }
            QLabel#fileLabel {
                color: #a6e3a1;
                font-size: 13px;
            }
            QLabel#errorLabel {
                color: #f38ba8;
                font-size: 14px;
                margin: 8px;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QScrollBar:vertical {
                border: none;
                background-color: #313244;
                width: 10px;
                margin: 0;
            }
            QScrollBar::handle:vertical {
                background-color: #45475a;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #89b4fa;
            }
        """)
        
        # Create central widget with scroll area
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_widget = QWidget()
        header_layout = QVBoxLayout(header_widget)
        header_layout.setContentsMargins(20, 20, 20, 20)
        
        title_label = QLabel("Create New Lesson")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        
        subtitle_label = QLabel("Share your knowledge and inspire students with engaging content")
        subtitle_label.setObjectName("subtitleLabel")
        header_layout.addWidget(subtitle_label)
        
        main_layout.addWidget(header_widget)
        
        # Content area
        content_widget = QWidget()
        content_layout = QHBoxLayout(content_widget)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 0, 20, 20)
        
        # Left side - Preview
        preview_frame = QFrame()
        preview_frame.setObjectName("previewFrame")
        preview_layout = QVBoxLayout(preview_frame)
        preview_layout.setSpacing(20)
        preview_layout.setContentsMargins(30, 30, 30, 30)
        
        preview_title = QLabel("Preview")
        preview_title.setObjectName("titleLabel")
        preview_layout.addWidget(preview_title)
        
        # Preview container
        preview_container = QFrame()
        preview_container.setStyleSheet("""
            QFrame {
                background-color: #11111b;
                border: 2px dashed #45475a;
            }
        """)
        preview_container_layout = QVBoxLayout(preview_container)
        
        self.preview_image = QLabel()
        self.preview_image.setFixedSize(480, 270)
        self.preview_image.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.preview_image.setStyleSheet("""
            QLabel {
                background-color: transparent;
                border-radius: 8px;
            }
        """)
        preview_container_layout.addWidget(self.preview_image, alignment=Qt.AlignmentFlag.AlignCenter)
        
        preview_layout.addWidget(preview_container)
        
        # Video info
        self.video_info = QLabel("No video selected")
        self.video_info.setObjectName("fileLabel")
        self.video_info.setAlignment(Qt.AlignmentFlag.AlignCenter)
        preview_layout.addWidget(self.video_info)
        
        # Upload buttons
        upload_layout = QHBoxLayout()
        upload_layout.setSpacing(10)
        
        self.video_button = QPushButton("Upload Video")
        self.video_button.setObjectName("secondaryButton")
        self.video_button.setIcon(QIcon("resources/icons/upload_video.png"))
        self.video_button.clicked.connect(self.select_video)
        upload_layout.addWidget(self.video_button)
        
        self.image_button = QPushButton("Upload Thumbnail")
        self.image_button.setObjectName("secondaryButton")
        self.image_button.setIcon(QIcon("resources/icons/upload_image.png"))
        self.image_button.clicked.connect(self.select_image)
        upload_layout.addWidget(self.image_button)
        
        preview_layout.addLayout(upload_layout)
        preview_layout.addStretch()
        
        content_layout.addWidget(preview_frame)
        
        # Right side - Form
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(30, 30, 30, 30)
        
        # Lesson details section
        details_label = QLabel("Lesson Details")
        details_label.setObjectName("titleLabel")
        form_layout.addWidget(details_label)
        
        # Title input
        title_label = QLabel("Title")
        self.title_input = QLineEdit()
        self.title_input.setPlaceholderText("Enter an engaging title for your lesson")
        form_layout.addWidget(title_label)
        form_layout.addWidget(self.title_input)
        
        # Description input
        description_label = QLabel("Description")
        self.description_input = QTextEdit()
        self.description_input.setPlaceholderText("Provide a detailed description of what students will learn")
        self.description_input.setMinimumHeight(200)
        form_layout.addWidget(description_label)
        form_layout.addWidget(self.description_input)
        
        form_layout.addStretch()
        
        # Create button
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        
        self.create_button = QPushButton("Create Lesson")
        self.create_button.setFixedWidth(200)
        self.create_button.clicked.connect(self.handle_create)
        button_layout.addWidget(self.create_button, alignment=Qt.AlignmentFlag.AlignCenter)
        
        form_layout.addWidget(button_container)
        
        content_layout.addWidget(form_frame)
        
        # Set stretch factors
        content_layout.setStretch(0, 1)  # Preview
        content_layout.setStretch(1, 1)  # Form
        
        main_layout.addWidget(content_widget)
        
    def select_video(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Video",
            "",
            "Video Files (*.mp4 *.avi *.mov *.wmv)"
        )
        if file_path:
            self.selected_video_path = file_path
            filename = os.path.basename(file_path)
            self.video_info.setText(f"Selected: {filename}")
            self.video_button.setText("Change Video")
            
    def select_image(self):
        file_path, _ = QFileDialog.getOpenFileName(
            self,
            "Select Thumbnail",
            "",
            "Image Files (*.png *.jpg *.jpeg)"
        )
        if file_path:
            self.selected_image_path = file_path
            pixmap = QPixmap(file_path)
            if not pixmap.isNull():
                scaled_pixmap = pixmap.scaled(
                    self.preview_image.size(),
                    Qt.AspectRatioMode.KeepAspectRatio,
                    Qt.TransformationMode.SmoothTransformation
                )
                self.preview_image.setPixmap(scaled_pixmap)
            self.image_button.setText("Change Thumbnail")
            
    def handle_create(self):
        title = self.title_input.text().strip()
        description = self.description_input.toPlainText().strip()
        
        # Validate input
        if not title:
            self.show_error("Please enter a lesson title")
            return
            
        if not description:
            self.show_error("Please enter a lesson description")
            return
            
        if not self.selected_video_path:
            self.show_error("Please select a video file")
            return
            
        # Create lesson
        lesson = Lesson(
            id=0,  # Will be set by database
            title=title,
            title_ar=title,  # For now, use same title for both languages
            description=description,
            description_ar=description,  # For now, use same description for both languages
            image_path=self.selected_image_path or "",
            video_path=self.selected_video_path,
            created_by=self.user.id,
            created_at=None  # Will be set by database
        )
        
        if self.db.add_lesson(lesson):
            self.close()  # Close the lesson creation window
            self.nav_manager.show_teacher_dashboard(self.user)
        else:
            self.show_error("Failed to create lesson")
            
    def show_error(self, message: str):
        """Show an error message in the form."""
        QMessageBox.warning(self, "Error", message)

    def update_ui_text(self):
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - إنشاء درس')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("إنشاء درس جديد")
                elif widget.text() == "Share your knowledge and inspire students with engaging content":
                    widget.setText("شارك معرفتك وألهم الطلاب بمحتوى جذاب")
                elif widget.text() == "Preview":
                    widget.setText("معاينة")
                elif widget.text() == "Title (English)":
                    widget.setText("العنوان (بالإنجليزية)")
                elif widget.text() == "Title (Arabic)":
                    widget.setText("العنوان (بالعربية)")
                elif widget.text() == "Description (English)":
                    widget.setText("الوصف (بالإنجليزية)")
                elif widget.text() == "Description (Arabic)":
                    widget.setText("الوصف (بالعربية)")
                elif widget.text() == "Upload Image":
                    widget.setText("رفع صورة")
                elif widget.text() == "Upload Video":
                    widget.setText("رفع فيديو")
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "Create Lesson":
                    button.setText("إنشاء الدرس")
                elif button.text() == "Cancel":
                    button.setText("إلغاء")
        else:
            self.setWindowTitle('Educational Platform - Create Lesson')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("Create New Lesson")
                elif widget.text() == "شارك معرفتك وألهم الطلاب بمحتوى جذاب":
                    widget.setText("Share your knowledge and inspire students with engaging content")
                elif widget.text() == "معاينة":
                    widget.setText("Preview")
                elif widget.text() == "العنوان (بالإنجليزية)":
                    widget.setText("Title (English)")
                elif widget.text() == "العنوان (بالعربية)":
                    widget.setText("Title (Arabic)")
                elif widget.text() == "الوصف (بالإنجليزية)":
                    widget.setText("Description (English)")
                elif widget.text() == "الوصف (بالعربية)":
                    widget.setText("Description (Arabic)")
                elif widget.text() == "رفع صورة":
                    widget.setText("Upload Image")
                elif widget.text() == "رفع فيديو":
                    widget.setText("Upload Video")
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "إنشاء الدرس":
                    button.setText("Create Lesson")
                elif button.text() == "إلغاء":
                    button.setText("Cancel")