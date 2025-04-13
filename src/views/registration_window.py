from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QFrame, QMessageBox, QComboBox)
from PyQt6.QtCore import Qt
from PyQt6.QtGui import QFont, QIcon, QPixmap
from src.models.database import Database, User
from src.utils.navigation import NavigationManager
from src.utils.security import Security

class RegistrationWindow(QMainWindow):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.nav_manager = NavigationManager()
        self.current_language = "ar"  # Set Arabic as default
        self.init_ui()
        # Set initial language
        self.update_language("العربية")
        
    def init_ui(self):
        self.setWindowTitle('Educational Platform - Registration')
        self.setMinimumSize(1000, 600)
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
            QLineEdit {
                padding: 12px;
                border: 2px solid #313244;
                border-radius: 6px;
                background-color: #313244;
                color: #cdd6f4;
                font-size: 14px;
                selection-background-color: #45475a;
            }
            QLineEdit:focus {
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
            QPushButton#linkButton {
                background-color: transparent;
                color: #89b4fa;
                padding: 5px;
                text-decoration: underline;
            }
            QPushButton#linkButton:hover {
                color: #b4befe;
            }
            QComboBox {
                padding: 12px;
                border: 2px solid #313244;
                border-radius: 6px;
                background-color: #313244;
                color: #cdd6f4;
                font-size: 14px;
                min-width: 150px;
            }
            QComboBox:hover {
                border-color: #89b4fa;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/dropdown.png);
                width: 12px;
                height: 12px;
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
        main_layout.setSpacing(0)
        main_layout.setContentsMargins(0, 0, 0, 0)
        
        # Create two-column layout
        content_layout = QHBoxLayout()
        content_layout.setSpacing(0)
        content_layout.setContentsMargins(0, 0, 0, 0)
        
        # Left side - Illustration
        illustration_frame = QFrame()
        illustration_layout = QVBoxLayout(illustration_frame)
        illustration_layout.setContentsMargins(40, 40, 40, 40)
        
        # Add illustration image
        illustration_label = QLabel()
        illustration_label.setFixedSize(400, 400)
        illustration_label.setStyleSheet("background-color: transparent;")
        try:
            pixmap = QPixmap("resources/images/register_illustration.png")
            if not pixmap.isNull():
                illustration_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
            # If image fails to load, show text
            illustration_label.setText("Educational Platform")
            illustration_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
            illustration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        illustration_layout.addWidget(illustration_label)
        content_layout.addWidget(illustration_frame)
        
        # Right side - Registration form
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        self.title_label = QLabel("Create Student Account")
        self.title_label.setObjectName("titleLabel")
        self.title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(self.title_label)
        
        # Subtitle
        self.subtitle_label = QLabel("Join us and start learning today!")
        self.subtitle_label.setFont(QFont("Segoe UI", 14))
        form_layout.addWidget(self.subtitle_label)
        
        form_layout.addSpacing(20)
        
        # Username
        self.username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Choose a username")
        form_layout.addWidget(self.username_label)
        form_layout.addWidget(self.username_input)
        
        # Password
        self.password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Create a password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.password_label)
        form_layout.addWidget(self.password_input)
        
        # Confirm Password
        self.confirm_password_label = QLabel("Confirm Password")
        self.confirm_password_input = QLineEdit()
        self.confirm_password_input.setPlaceholderText("Confirm your password")
        self.confirm_password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(self.confirm_password_label)
        form_layout.addWidget(self.confirm_password_input)
        
        # Language selection
        self.lang_label = QLabel("Language")
        self.lang_combo = QComboBox()
        self.lang_combo.addItems(["English", "العربية"])
        self.lang_combo.setCurrentText("العربية")  # Set Arabic as default
        self.lang_combo.currentTextChanged.connect(self.update_language)
        self.lang_combo.setStyleSheet("""
            QComboBox {
                background-color: #2d2d2d;
                color: #ffffff;
                border: 1px solid #3d3d3d;
                border-radius: 4px;
                padding: 5px;
                min-width: 100px;
            }
            QComboBox:hover {
                border-color: #4d4d4d;
            }
            QComboBox:focus {
                border-color: #0078d4;
            }
            QComboBox::drop-down {
                border: none;
            }
            QComboBox::down-arrow {
                image: url(resources/icons/dropdown.png);
                width: 12px;
                height: 12px;
            }
        """)
        form_layout.addWidget(self.lang_label)
        form_layout.addWidget(self.lang_combo)
        
        form_layout.addSpacing(20)
        
        # Register button
        self.register_button = QPushButton("Create Account")
        self.register_button.clicked.connect(self.handle_register)
        self.register_button.setFixedWidth(200)
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.register_button, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(button_container)
        
        # Login link
        login_container = QWidget()
        login_layout = QHBoxLayout(login_container)
        login_layout.setContentsMargins(0, 0, 0, 0)
        
        self.have_account_label = QLabel("Already have an account?")
        self.login_button = QPushButton("Sign In")
        self.login_button.setObjectName("linkButton")
        self.login_button.clicked.connect(self.nav_manager.show_login)
        
        login_layout.addWidget(self.have_account_label, alignment=Qt.AlignmentFlag.AlignRight)
        login_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(login_container)
        
        # Add form to content layout
        content_layout.addWidget(form_frame)
        
        # Set stretch factors
        content_layout.setStretch(0, 1)  # Illustration
        content_layout.setStretch(1, 1)  # Form
        
        main_layout.addLayout(content_layout)
        
    def update_language(self, lang: str):
        self.current_language = "ar" if lang == "العربية" else "en"
        
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - التسجيل')
            self.title_label.setText("إنشاء حساب طالب")
            self.subtitle_label.setText("انضم إلينا وابدأ التعلم اليوم!")
            self.username_label.setText("اسم المستخدم")
            self.username_input.setPlaceholderText("اختر اسم مستخدم")
            self.password_label.setText("كلمة المرور")
            self.password_input.setPlaceholderText("أنشئ كلمة مرور")
            self.confirm_password_label.setText("تأكيد كلمة المرور")
            self.confirm_password_input.setPlaceholderText("أكد كلمة المرور")
            self.lang_label.setText("اللغة")
            self.register_button.setText("إنشاء حساب")
            self.have_account_label.setText("لديك حساب بالفعل؟")
            self.login_button.setText("تسجيل الدخول")
        else:
            self.setWindowTitle('Educational Platform - Registration')
            self.title_label.setText("Create Student Account")
            self.subtitle_label.setText("Join us and start learning today!")
            self.username_label.setText("Username")
            self.username_input.setPlaceholderText("Choose a username")
            self.password_label.setText("Password")
            self.password_input.setPlaceholderText("Create a password")
            self.confirm_password_label.setText("Confirm Password")
            self.confirm_password_input.setPlaceholderText("Confirm your password")
            self.lang_label.setText("Language")
            self.register_button.setText("Create Account")
            self.have_account_label.setText("Already have an account?")
            self.login_button.setText("Sign In")
            
    def handle_register(self):
        username = self.username_input.text().strip()
        password = self.password_input.text().strip()
        confirm_password = self.confirm_password_input.text().strip()
        
        # Validate inputs
        if not username or not password or not confirm_password:
            self.show_error("Please fill in all fields" if self.current_language == "en" else "يجب ملء جميع الحقول")
            return
            
        if password != confirm_password:
            self.show_error("Passwords do not match" if self.current_language == "en" else "كلمات المرور غير متطابقة")
            return
            
        # Check if username exists
        if self.db.get_user_by_username(username):
            self.show_error("Username already exists" if self.current_language == "en" else "اسم المستخدم موجود بالفعل")
            return
            
        # Create user with selected language
        user = self.db.add_user(username, password, "student", self.current_language)
        if user:
            self.nav_manager.show_login()
        else:
            self.show_error("Failed to create account" if self.current_language == "en" else "فشل إنشاء الحساب")
            
    def show_error(self, message: str):
        error_label = QLabel(message)
        error_label.setStyleSheet("color: #f38ba8; font-size: 14px;")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        # Find and remove any existing error label
        for widget in self.findChildren(QLabel):
            if widget.styleSheet().startswith("color: #f38ba8"):
                widget.deleteLater()
                
        # Add the new error label to the form layout
        form_frame = self.findChild(QFrame)
        if form_frame:
            form_frame.layout().insertWidget(form_frame.layout().count() - 2, error_label) 