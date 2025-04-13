from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel, QHBoxLayout
from PyQt6.QtCore import Qt, pyqtSignal
from PyQt6.QtGui import QPixmap, QFont, QColor, QPalette
from src.models.database import Lesson

class LessonCard(QFrame):
    clicked = pyqtSignal()
    
    def __init__(self, lesson: Lesson, language: str):
        super().__init__()
        self.lesson = lesson
        self.language = language
        self.init_ui()
        
    def init_ui(self):
        self.setFixedHeight(300)
        self.setMinimumWidth(300)
        self.setStyleSheet("""
            QFrame {
                background-color: #313244;
                border-radius: 10px;
            }
            QFrame:hover {
                background-color: #45475a;
            }
            QLabel {
                color: #cdd6f4;
            }
            QLabel#titleLabel {
                color: #89b4fa;
                font-weight: bold;
            }
        """)
        
        # Main layout
        layout = QVBoxLayout(self)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        # Image container
        image_container = QFrame()
        image_container.setFixedHeight(180)
        image_container.setStyleSheet("""
            QFrame {
                background-color: #1e1e2e;
                border-top-left-radius: 10px;
                border-top-right-radius: 10px;
                border-bottom-left-radius: 0px;
                border-bottom-right-radius: 0px;
            }
        """)
        
        # Image
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(self.lesson.image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(300, 180, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("No image")
            image_label.setStyleSheet("color: #6c7086; font-size: 14px;")
        
        image_layout.addWidget(image_label)
        layout.addWidget(image_container)
        
        # Content container
        content_container = QFrame()
        content_layout = QVBoxLayout(content_container)
        content_layout.setContentsMargins(15, 15, 15, 15)
        content_layout.setSpacing(10)
        
        # Title
        title_label = QLabel()
        title_label.setObjectName("titleLabel")
        title_label.setFont(QFont("Segoe UI", 14))
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Description
        desc_label = QLabel()
        desc_label.setFont(QFont("Segoe UI", 12))
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        
        # Set text based on language
        if self.language == "ar":
            title_label.setText(self.lesson.title_ar)
            desc_text = self.lesson.description_ar
        else:
            title_label.setText(self.lesson.title)
            desc_text = self.lesson.description
            
        # Truncate description
        if len(desc_text) > 100:
            desc_text = desc_text[:97] + "..."
        desc_label.setText(desc_text)
        
        content_layout.addWidget(title_label)
        content_layout.addWidget(desc_label)
        layout.addWidget(content_container)
        
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.clicked.emit()
            
    def enterEvent(self, event):
        self.setCursor(Qt.CursorShape.PointingHandCursor)
        super().enterEvent(event)
        
    def leaveEvent(self, event):
        self.setCursor(Qt.CursorShape.ArrowCursor)
        super().leaveEvent(event) 