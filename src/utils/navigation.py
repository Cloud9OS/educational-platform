from typing import Optional
from PyQt6.QtWidgets import QMainWindow
from src.models.database import Database, User

class NavigationManager:
    _instance = None
    _current_window: Optional[QMainWindow] = None
    _db: Optional[Database] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(NavigationManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        if self._db is None:
            self._db = Database()
            
    @property
    def current_window(self) -> Optional[QMainWindow]:
        return self._current_window
        
    def show_login(self):
        if self._current_window:
            self._current_window.close()
        # Import here to avoid circular import
        from src.views.login_window import LoginWindow
        self._current_window = LoginWindow(self._db)
        self._current_window.show()
        
    def show_registration(self):
        if self._current_window:
            self._current_window.close()
        # Import here to avoid circular import
        from src.views.registration_window import RegistrationWindow
        self._current_window = RegistrationWindow(self._db)
        self._current_window.show()
        
    def show_dashboard(self, user: User):
        if self._current_window:
            self._current_window.close()
            
        if user.role == "admin":
            # Import here to avoid circular import
            from src.views.admin_dashboard import AdminDashboard
            self._current_window = AdminDashboard(user)
        elif user.role == "teacher":
            # Import here to avoid circular import
            from src.views.teacher_dashboard import TeacherDashboard
            self._current_window = TeacherDashboard(self._db, user)
        else:
            # Import here to avoid circular import
            from src.views.student_dashboard import StudentDashboard
            self._current_window = StudentDashboard(self._db, user)
            
        self._current_window.show()
        
    def show_teacher_dashboard(self, user: User):
        if self._current_window:
            self._current_window.close()
        # Import here to avoid circular import
        from src.views.teacher_dashboard import TeacherDashboard
        self._current_window = TeacherDashboard(self._db, user)
        self._current_window.show()
        
    def logout(self):
        self.show_login()
        
    def get_database(self) -> Database:
        return self._db 