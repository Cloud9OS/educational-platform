from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QComboBox, QScrollArea, QGridLayout,
                            QFrame, QSizePolicy, QTableWidget, QTableWidgetItem, QDialog,
                            QLineEdit, QMessageBox, QTabWidget, QFormLayout)
from PyQt6.QtCore import Qt, pyqtSlot
from PyQt6.QtGui import QFont, QIcon
from src.models.database import Database, User, Lesson
from src.utils.navigation import NavigationManager
from src.utils.security import Security
from datetime import datetime

class AdminDashboard(QMainWindow):
    def __init__(self, user: User):
        super().__init__()
        self.user = user
        self.db = Database()
        self.nav = NavigationManager()
        self.current_language = user.language  # Get language from user
        self.setup_ui()
        self.load_data()
        # Set initial language
        self.update_ui_text()
        
    def setup_ui(self):
        self.setWindowTitle("Admin Dashboard")
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
            QLabel#sectionLabel {
                color: #94e2d5;
                font-size: 24px;
                font-weight: bold;
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
            QPushButton#dangerButton {
                background-color: #f38ba8;
            }
            QPushButton#dangerButton:hover {
                background-color: #eba0b3;
            }
            QTableWidget {
                background-color: #313244;
                border: none;
                border-radius: 12px;
                gridline-color: #45475a;
                color: #cdd6f4;
            }
            QTableWidget::item {
                padding: 8px;
            }
            QTableWidget::item:selected {
                background-color: #45475a;
            }
            QHeaderView::section {
                background-color: #181825;
                color: #89b4fa;
                padding: 8px;
                border: none;
                font-weight: bold;
            }
            QFrame {
                background-color: #313244;
                border-radius: 12px;
            }
            QComboBox {
                background-color: #313244;
                color: #cdd6f4;
                border: 2px solid #45475a;
                border-radius: 8px;
                padding: 8px;
            }
            QComboBox:hover {
                border-color: #89b4fa;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/dropdown.png);
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
        
        # Create central widget
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Header
        header_frame = QFrame()
        header_frame.setObjectName("headerFrame")
        header_layout = QHBoxLayout(header_frame)
        header_layout.setContentsMargins(20, 10, 20, 10)
        
        # Title
        title_label = QLabel("Admin Dashboard")
        title_label.setObjectName("titleLabel")
        header_layout.addWidget(title_label)
        
        # Right side controls
        controls_layout = QHBoxLayout()
        controls_layout.setSpacing(15)
        
        # Language selector
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "العربية"])
        self.lang_combo.setCurrentText("العربية" if self.user.language == "ar" else "English")
        self.lang_combo.currentTextChanged.connect(self.change_language)
        controls_layout.addWidget(self.lang_combo)
        
        # Logout button
        self.logout_button = QPushButton("Logout")
        self.logout_button.clicked.connect(self.nav.logout)
        controls_layout.addWidget(self.logout_button)
        
        header_layout.addLayout(controls_layout)
        main_layout.addWidget(header_frame)
        
        # Tab widget
        tabs = QTabWidget()
        
        # Users tab
        users_tab = QWidget()
        users_layout = QVBoxLayout(users_tab)
        
        # Users toolbar
        users_toolbar = QHBoxLayout()
        add_user_btn = QPushButton("Add User")
        add_user_btn.clicked.connect(self.add_user)
        users_toolbar.addWidget(add_user_btn)
        users_toolbar.addStretch()
        users_layout.addLayout(users_toolbar)
        
        # Users table
        self.users_table = QTableWidget()
        self.users_table.setColumnCount(5)
        self.users_table.setHorizontalHeaderLabels(["ID", "Username", "Role", "Language", "Actions"])
        self.users_table.horizontalHeader().setStretchLastSection(True)
        self.users_table.verticalHeader().setVisible(False)
        users_layout.addWidget(self.users_table)
        
        # Lessons tab
        lessons_tab = QWidget()
        lessons_layout = QVBoxLayout(lessons_tab)
        
        # Lessons table
        self.lessons_table = QTableWidget()
        self.lessons_table.setColumnCount(7)
        self.lessons_table.setHorizontalHeaderLabels(["ID", "Title", "Title (AR)", "Created By", "Created At", "Actions"])
        self.lessons_table.horizontalHeader().setStretchLastSection(True)
        self.lessons_table.verticalHeader().setVisible(False)
        lessons_layout.addWidget(self.lessons_table)
        
        # Add tabs
        tabs.addTab(users_tab, "Users")
        tabs.addTab(lessons_tab, "Lessons")
        main_layout.addWidget(tabs)
        
    def load_data(self):
        # Load users
        users = self.db.get_users()
        self.users_table.setRowCount(len(users))
        for i, user in enumerate(users):
            self.users_table.setItem(i, 0, QTableWidgetItem(str(user.id)))
            self.users_table.setItem(i, 1, QTableWidgetItem(user.username))
            self.users_table.setItem(i, 2, QTableWidgetItem(user.role))
            self.users_table.setItem(i, 3, QTableWidgetItem(user.language))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            edit_btn = QPushButton("Edit")
            edit_btn.clicked.connect(lambda checked, u=user: self.edit_user(u))
            
            delete_btn = QPushButton("Delete")
            delete_btn.setObjectName("dangerButton")
            delete_btn.clicked.connect(lambda checked, u=user: self.delete_user(u))
            
            actions_layout.addWidget(edit_btn)
            actions_layout.addWidget(delete_btn)
            self.users_table.setCellWidget(i, 4, actions_widget)

        # Load lessons
        lessons = self.db.get_lessons()
        self.lessons_table.setRowCount(len(lessons))
        for i, lesson in enumerate(lessons):
            self.lessons_table.setItem(i, 0, QTableWidgetItem(str(lesson.id)))
            self.lessons_table.setItem(i, 1, QTableWidgetItem(lesson.title))
            self.lessons_table.setItem(i, 2, QTableWidgetItem(lesson.title_ar))
            
            creator = self.db.get_user(lesson.created_by)
            creator_name = creator.username if creator else "Unknown"
            self.lessons_table.setItem(i, 3, QTableWidgetItem(creator_name))
            
            created_at = lesson.created_at.strftime("%Y-%m-%d %H:%M") if lesson.created_at else "Unknown"
            self.lessons_table.setItem(i, 4, QTableWidgetItem(created_at))
            
            actions_widget = QWidget()
            actions_layout = QHBoxLayout(actions_widget)
            actions_layout.setContentsMargins(0, 0, 0, 0)
            
            delete_btn = QPushButton("Delete")
            delete_btn.clicked.connect(lambda checked, l=lesson: self.delete_lesson(l))
            
            actions_layout.addWidget(delete_btn)
            self.lessons_table.setCellWidget(i, 5, actions_widget)

    def add_user(self):
        dialog = UserDialog(self)
        if dialog.exec():
            username = dialog.username.text()
            password = dialog.password.text()
            role = dialog.role.currentText()
            language = dialog.language.currentText()
            
            user = self.db.add_user(username, password, role, language)
            if user:
                self.load_data()
                QMessageBox.information(self, "Success", "User added successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Username '{username}' already exists. Please choose a different username.")

    def edit_user(self, user: User):
        dialog = UserDialog(self, user)
        if dialog.exec():
            username = dialog.username.text()
            role = dialog.role.currentText()
            language = dialog.language.currentText()
            
            if self.db.update_user(user.id, username, role, language):
                self.load_data()
                QMessageBox.information(self, "Success", "User updated successfully!")
            else:
                QMessageBox.warning(self, "Error", f"Username '{username}' is already taken by another user. Please choose a different username.")

    def delete_user(self, user: User):
        if user.role == 'admin':
            QMessageBox.warning(self, "Error", "Cannot delete admin user!")
            return
            
        reply = QMessageBox.question(self, "Confirm Delete",
                                   f"Are you sure you want to delete user {user.username}?\n"
                                   "This will also delete all lessons created by this user.",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_user(user.id):
                self.load_data()
                QMessageBox.information(self, "Success", "User deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete user.")

    def delete_lesson(self, lesson: Lesson):
        reply = QMessageBox.question(self, "Confirm Delete",
                                   f"Are you sure you want to delete lesson {lesson.title}?",
                                   QMessageBox.StandardButton.Yes | QMessageBox.StandardButton.No)
        
        if reply == QMessageBox.StandardButton.Yes:
            if self.db.delete_lesson(lesson.id):
                self.load_data()
                QMessageBox.information(self, "Success", "Lesson deleted successfully!")
            else:
                QMessageBox.warning(self, "Error", "Failed to delete lesson.")

    @pyqtSlot(str)
    def change_language(self, language: str):
        lang_code = 'ar' if language == 'العربية' else 'en'
        if self.db.update_user_language(self.user.id, lang_code):
            self.user.language = lang_code
            self.update_ui_text()

    def update_ui_text(self):
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - لوحة تحكم المشرف')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("لوحة تحكم المشرف")
                elif widget.text() == "Users":
                    widget.setText("المستخدمون")
                elif widget.text() == "Lessons":
                    widget.setText("الدروس")
                elif widget.text() == "Username":
                    widget.setText("اسم المستخدم")
                elif widget.text() == "Role":
                    widget.setText("الدور")
                elif widget.text() == "Actions":
                    widget.setText("الإجراءات")
                elif widget.text() == "Title":
                    widget.setText("العنوان")
                elif widget.text() == "Created By":
                    widget.setText("أنشئ بواسطة")
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "Add User":
                    button.setText("إضافة مستخدم")
                elif button.text() == "Edit":
                    button.setText("تعديل")
                elif button.text() == "Delete":
                    button.setText("حذف")
                elif button.text() == "Add Lesson":
                    button.setText("إضافة درس")
        else:
            self.setWindowTitle('Educational Platform - Admin Dashboard')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("Admin Dashboard")
                elif widget.text() == "المستخدمون":
                    widget.setText("Users")
                elif widget.text() == "الدروس":
                    widget.setText("Lessons")
                elif widget.text() == "اسم المستخدم":
                    widget.setText("Username")
                elif widget.text() == "الدور":
                    widget.setText("Role")
                elif widget.text() == "الإجراءات":
                    widget.setText("Actions")
                elif widget.text() == "العنوان":
                    widget.setText("Title")
                elif widget.text() == "أنشئ بواسطة":
                    widget.setText("Created By")
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "إضافة مستخدم":
                    button.setText("Add User")
                elif button.text() == "تعديل":
                    button.setText("Edit")
                elif button.text() == "حذف":
                    button.setText("Delete")
                elif button.text() == "إضافة درس":
                    button.setText("Add Lesson")


class UserDialog(QDialog):
    def __init__(self, parent=None, user: User = None):
        super().__init__(parent)
        self.user = user
        self.db = Database()
        self.setup_ui()

    def setup_ui(self):
        self.setWindowTitle("Add User" if not self.user else "Edit User")
        self.setMinimumWidth(400)
        layout = QFormLayout()
        self.setLayout(layout)

        # Username field
        self.username = QLineEdit()
        if self.user:
            self.username.setText(self.user.username)
        layout.addRow("Username:", self.username)

        # Password field (only for new users)
        if not self.user:
            self.password = QLineEdit()
            self.password.setEchoMode(QLineEdit.EchoMode.Password)
            layout.addRow("Password:", self.password)

        # Role selector
        self.role = QComboBox()
        self.role.addItems(['student', 'teacher'])
        if self.user:
            self.role.setCurrentText(self.user.role)
        layout.addRow("Role:", self.role)

        # Language selector
        self.language = QComboBox()
        self.language.addItems(['en', 'ar'])
        if self.user:
            self.language.setCurrentText(self.user.language)
        layout.addRow("Language:", self.language)

        # Buttons
        button_layout = QHBoxLayout()
        save_btn = QPushButton("Save")
        save_btn.clicked.connect(self.accept)
        cancel_btn = QPushButton("Cancel")
        cancel_btn.clicked.connect(self.reject)
        button_layout.addWidget(save_btn)
        button_layout.addWidget(cancel_btn)
        layout.addRow("", button_layout)

        self.setStyleSheet("""
            QDialog {
                background-color: #1E1E2E;
                color: #CDD6F4;
            }
            QLabel {
                color: #CDD6F4;
            }
            QLineEdit, QComboBox {
                background-color: #313244;
                color: #CDD6F4;
                border: 1px solid #45475A;
                border-radius: 4px;
                padding: 5px;
            }
            QLineEdit:focus, QComboBox:focus {
                border: 1px solid #89B4FA;
            }
            QPushButton {
                background-color: #89B4FA;
                color: #1E1E2E;
                border: none;
                border-radius: 4px;
                padding: 5px 15px;
            }
            QPushButton:hover {
                background-color: #B4BEFE;
            }
        """)

    def accept(self):
        username = self.username.text().strip()
        role = self.role.currentText()
        language = self.language.currentText()
        
        if not username:
            QMessageBox.warning(self, "Error", "Please enter a username")
            return
            
        if not self.user:  # Creating new user
            password = self.password.text()
            if not password:
                QMessageBox.warning(self, "Error", "Please enter a password")
                return
                
            # Check if username exists before trying to create
            existing_user = self.db.get_user_by_username(username)
            if existing_user:
                QMessageBox.warning(self, "Error", f"Username '{username}' already exists. Please choose a different username.")
                return
                
            user = self.db.add_user(username, password, role, language)
            if user:
                super().accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to create user. Please try again.")
        else:  # Updating existing user
            if username != self.user.username:  # Only check if username changed
                existing_user = self.db.get_user_by_username(username)
                if existing_user:
                    QMessageBox.warning(self, "Error", f"Username '{username}' is already taken by another user. Please choose a different username.")
                    return
                    
            if self.db.update_user(self.user.id, username, role, language):
                super().accept()
            else:
                QMessageBox.critical(self, "Error", "Failed to update user. Please try again.") 