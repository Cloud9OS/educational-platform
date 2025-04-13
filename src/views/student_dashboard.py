from PyQt6.QtWidgets import QMessageBox
from .dashboard import Dashboard
from src.models.database import User, Database

class StudentDashboard(Dashboard):
    def __init__(self, db: Database, user: User):
        super().__init__(db, user)
        self.init_student_ui()
        
    def init_student_ui(self):
        # Student dashboard is simpler, just inherits base functionality
        self.update_ui_text()
        
    def update_ui_text(self):
        super().update_ui_text()
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - لوحة الطالب')
        else:
            self.setWindowTitle('Educational Platform - Student Dashboard')
            
    def show_lesson_detail(self, lesson):
        # Override to add student-specific functionality if needed
        super().show_lesson_detail(lesson) 