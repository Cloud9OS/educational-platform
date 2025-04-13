from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QComboBox, QScrollArea, QGridLayout,
                            QFrame, QSizePolicy)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from src.models.database import Database, User, Lesson
from .lesson_card import LessonCard
from .lesson_detail import LessonDetailWindow
from src.utils.navigation import NavigationManager

class Dashboard(QMainWindow):
    def __init__(self, db: Database, user: User):
        super().__init__()
        self.db = db
        self.user = user
        self.current_language = user.language
        self.nav_manager = NavigationManager()
        self.init_ui()
        # Set initial language
        self.update_ui_text()
        
    def init_ui(self):
        self.setWindowTitle('Educational Platform - Dashboard')
        self.setMinimumSize(1000, 600)
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1e1e2e;
            }
            QLabel {
                color: #cdd6f4;
                font-size: 14px;
            }
            QPushButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                padding: 10px 20px;
                border-radius: 6px;
                font-size: 14px;
                font-weight: bold;
            }
            QPushButton:hover {
                background-color: #b4befe;
            }
            QPushButton:pressed {
                background-color: #74c7ec;
            }
            QComboBox {
                padding: 8px 15px;
                border: 2px solid #89b4fa;
                border-radius: 6px;
                background-color: #313244;
                color: #cdd6f4;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #b4befe;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/dropdown.png);
                width: 12px;
                height: 12px;
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
                background-color: #89b4fa;
                border-radius: 5px;
                min-height: 20px;
            }
            QScrollBar::handle:vertical:hover {
                background-color: #b4befe;
            }
            QFrame#headerFrame {
                background-color: #313244;
                border-radius: 10px;
                padding: 10px;
            }
            QFrame#contentFrame {
                background-color: #313244;
                border-radius: 10px;
                padding: 20px;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header section
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Welcome message
        self.welcome_label = QLabel()
        self.update_welcome_message()
        self.welcome_label.setFont(QFont("Segoe UI", 18, QFont.Weight.Bold))
        header_layout.addWidget(self.welcome_label)
        
        # Right side controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # Language selector
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "العربية"])
        self.lang_combo.setCurrentText("العربية" if self.current_language == "ar" else "English")
        self.lang_combo.currentTextChanged.connect(self.update_language)
        controls_layout.addWidget(self.lang_combo)
        
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.setFixedWidth(120)
        self.logout_button.clicked.connect(self.handle_logout)
        controls_layout.addWidget(self.logout_button)
        
        header_layout.addLayout(controls_layout)
        main_layout.addWidget(header_frame)
        
        # Content area
        content_frame = QFrame()
        content_frame.setObjectName("contentFrame")
        content_layout = QVBoxLayout(content_frame)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Lessons section title
        lessons_title = QLabel("Available Lessons")
        lessons_title.setFont(QFont("Segoe UI", 16, QFont.Weight.Bold))
        lessons_title.setContentsMargins(20, 0, 0, 20)
        content_layout.addWidget(lessons_title)
        
        # Lessons grid
        self.lessons_scroll = QScrollArea()
        self.lessons_scroll.setWidgetResizable(True)
        self.lessons_scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        self.lessons_widget = QWidget()
        self.lessons_grid = QGridLayout(self.lessons_widget)
        self.lessons_grid.setSpacing(20)
        self.lessons_grid.setContentsMargins(20, 0, 20, 20)
        self.lessons_scroll.setWidget(self.lessons_widget)
        content_layout.addWidget(self.lessons_scroll)
        
        main_layout.addWidget(content_frame)
        
        # Load lessons
        self.load_lessons()
        
    def update_welcome_message(self):
        if self.current_language == "ar":
            self.welcome_label.setText(f"مرحباً {self.user.username}")
        else:
            self.welcome_label.setText(f"Welcome, {self.user.username}")
            
    def update_language(self, lang: str):
        self.current_language = "ar" if lang == "العربية" else "en"
        self.update_welcome_message()
        self.update_ui_text()
        self.load_lessons()
        
    def update_ui_text(self):
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - لوحة التحكم')
            self.logout_button.setText('تسجيل الخروج')
            # Find and update the lessons title label
            for widget in self.findChildren(QLabel):
                if widget.text() == "Available Lessons":
                    widget.setText("الدروس المتاحة")
        else:
            self.setWindowTitle('Educational Platform - Dashboard')
            self.logout_button.setText('Logout')
            # Find and update the lessons title label
            for widget in self.findChildren(QLabel):
                if widget.text() == "الدروس المتاحة":
                    widget.setText("Available Lessons")
            
    def load_lessons(self):
        # Clear existing lessons
        for i in reversed(range(self.lessons_grid.count())): 
            self.lessons_grid.itemAt(i).widget().setParent(None)
            
        # Get lessons from database
        lessons = self.db.get_lessons()
        
        # Calculate grid dimensions based on window width
        grid_width = self.lessons_scroll.viewport().width()
        card_width = 300  # Minimum card width
        columns = max(1, grid_width // (card_width + self.lessons_grid.spacing()))
        
        # Add lessons to grid
        for i, lesson in enumerate(lessons):
            row = i // columns
            col = i % columns
            
            card = LessonCard(lesson, self.current_language)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            card.clicked.connect(lambda l=lesson: self.show_lesson_detail(l))
            self.lessons_grid.addWidget(card, row, col)
            
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Reload lessons grid when window is resized
        self.load_lessons()
        
    def show_lesson_detail(self, lesson: Lesson):
        # Store the detail window as an instance variable to prevent garbage collection
        self.detail_window = LessonDetailWindow(lesson, self.current_language)
        self.detail_window.show()
        
    def handle_logout(self):
        self.nav_manager.logout() 