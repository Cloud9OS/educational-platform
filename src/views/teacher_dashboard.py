from PyQt6.QtWidgets import (QPushButton, QFileDialog, QMessageBox, QFrame, 
                            QHBoxLayout, QVBoxLayout, QSizePolicy, QLabel)
from PyQt6.QtCore import Qt
from .dashboard import Dashboard
from .lesson_creation_window import LessonCreationWindow
from .lesson_edit_window import LessonEditWindow
from .lesson_card import LessonCard
from src.models.database import User, Database, Lesson

class TeacherDashboard(Dashboard):
    def __init__(self, db: Database, user: User):
        super().__init__(db, user)
        self.add_lesson_button = None
        self.init_teacher_ui()
        
    def init_teacher_ui(self):
        # Add lesson button
        self.add_lesson_button = QPushButton("Add Lesson")
        self.add_lesson_button.setObjectName("primaryButton")
        self.add_lesson_button.setStyleSheet("""
            QPushButton#primaryButton {
                background-color: #89b4fa;
                color: #1e1e2e;
                border: none;
                padding: 12px 24px;
                border-radius: 8px;
                font-size: 14px;
                font-weight: bold;
                min-width: 120px;
            }
            QPushButton#primaryButton:hover {
                background-color: #b4befe;
            }
            QPushButton#primaryButton:pressed {
                background-color: #74c7ec;
            }
        """)
        self.add_lesson_button.clicked.connect(self.show_lesson_creation)
        
        # Get the header layout from the base class
        header_frame = self.findChild(QFrame, "headerFrame")
        if header_frame:
            header_layout = header_frame.layout()
            if header_layout:
                # Insert the button before the language selector
                header_layout.insertWidget(header_layout.count() - 2, self.add_lesson_button)
        
        self.update_ui_text()
        
    def update_ui_text(self):
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - لوحة تحكم المعلم')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("لوحة تحكم المعلم")
                elif widget.text() == "الدروس المتاحة":
                    widget.setText("الدروس المتاحة")
                    
            # Update buttons if they exist
            if hasattr(self, 'add_lesson_button'):
                self.add_lesson_button.setText('إضافة درس')
            if hasattr(self, 'logout_button'):
                self.logout_button.setText('تسجيل الخروج')
        else:
            self.setWindowTitle('Educational Platform - Teacher Dashboard')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("Teacher Dashboard")
                elif widget.text() == "الدروس المتاحة":
                    widget.setText("Available Lessons")
                    
            # Update buttons if they exist
            if hasattr(self, 'add_lesson_button'):
                self.add_lesson_button.setText('Add Lesson')
            if hasattr(self, 'logout_button'):
                self.logout_button.setText('Logout')
            
    def show_lesson_creation(self):
        # Create and show the new lesson creation window
        self.lesson_window = LessonCreationWindow(self.db, self.user)
        self.lesson_window.show()
        # Hide the current window
        self.hide()

    def load_lessons(self):
        # Clear existing lessons
        for i in reversed(range(self.lessons_grid.count())): 
            self.lessons_grid.itemAt(i).widget().setParent(None)
            
        # Get lessons from database (only teacher's lessons)
        lessons = self.db.get_lessons(teacher_id=self.user.id)
        
        # Calculate grid dimensions based on window width
        grid_width = self.width() - 80  # Account for margins
        card_width = 300  # Minimum card width
        columns = max(1, grid_width // (card_width + self.lessons_grid.spacing()))
        
        # Add lessons to grid
        for i, lesson in enumerate(lessons):
            row = i // columns
            col = i % columns
            
            # Create card container
            card_container = QFrame()
            container_layout = QVBoxLayout(card_container)
            container_layout.setContentsMargins(0, 0, 0, 10)
            
            # Add lesson card
            card = LessonCard(lesson, self.current_language)
            card.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
            card.clicked.connect(lambda l=lesson: self.show_lesson_detail(l))
            container_layout.addWidget(card)
            
            # Add edit button
            edit_button = QPushButton("Edit Lesson" if self.current_language == "en" else "تعديل الدرس")
            edit_button.setStyleSheet("""
                QPushButton {
                    background-color: #89b4fa;
                    color: #1e1e2e;
                    border: none;
                    padding: 8px;
                    border-radius: 4px;
                    font-size: 12px;
                }
                QPushButton:hover {
                    background-color: #b4befe;
                }
            """)
            edit_button.clicked.connect(lambda checked, l=lesson: self.edit_lesson(l))
            container_layout.addWidget(edit_button)
            
            self.lessons_grid.addWidget(card_container, row, col)
            
    def edit_lesson(self, lesson: Lesson):
        """Open the lesson edit window."""
        self.edit_window = LessonEditWindow(self.db, self.user, lesson)
        self.edit_window.show()
        self.hide() 