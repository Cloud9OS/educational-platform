from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QLineEdit, QPushButton, QComboBox, QMessageBox, QFrame)
from PyQt6.QtCore import Qt, QSize
from PyQt6.QtGui import QFont, QIcon, QPixmap
from src.models.database import Database, User
from src.utils.navigation import NavigationManager
from src.utils.security import Security

class LoginWindow(QMainWindow):
    def __init__(self, db: Database):
        super().__init__()
        self.db = db
        self.current_user = None
        self.nav_manager = NavigationManager()
        self.current_language = "ar"  # Set Arabic as default
        self.init_ui()
        # Set initial language
        self.update_language("العربية")
        
    def init_ui(self):
        self.setWindowTitle('Educational Platform - Login')
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
            pixmap = QPixmap("resources/images/login_illustration.png")
            if not pixmap.isNull():
                illustration_label.setPixmap(pixmap.scaled(400, 400, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation))
        except:
            # If image fails to load, show text
            illustration_label.setText("Educational Platform")
            illustration_label.setFont(QFont("Segoe UI", 24, QFont.Weight.Bold))
            illustration_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        illustration_layout.addWidget(illustration_label)
        content_layout.addWidget(illustration_frame)
        
        # Right side - Login form
        form_frame = QFrame()
        form_layout = QVBoxLayout(form_frame)
        form_layout.setSpacing(20)
        form_layout.setContentsMargins(40, 40, 40, 40)
        
        # Title
        title_label = QLabel("Sign In")
        title_label.setObjectName("titleLabel")
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(title_label)
        
        # Subtitle
        subtitle_label = QLabel("Welcome back! Please enter your details.")
        subtitle_label.setFont(QFont("Segoe UI", 14))
        form_layout.addWidget(subtitle_label)
        
        form_layout.addSpacing(20)
        
        # Username
        username_label = QLabel("Username")
        self.username_input = QLineEdit()
        self.username_input.setPlaceholderText("Enter your username")
        form_layout.addWidget(username_label)
        form_layout.addWidget(self.username_input)
        
        # Password
        password_label = QLabel("Password")
        self.password_input = QLineEdit()
        self.password_input.setPlaceholderText("Enter your password")
        self.password_input.setEchoMode(QLineEdit.EchoMode.Password)
        form_layout.addWidget(password_label)
        form_layout.addWidget(self.password_input)
        
        # Language selection
        lang_label = QLabel("Language")
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
        form_layout.addWidget(lang_label)
        form_layout.addWidget(self.lang_combo)
        
        form_layout.addSpacing(20)
        
        # Login button
        self.login_button = QPushButton("Sign In")
        self.login_button.clicked.connect(self.handle_login)
        self.login_button.setFixedWidth(200)
        button_container = QWidget()
        button_layout = QHBoxLayout(button_container)
        button_layout.setContentsMargins(0, 0, 0, 0)
        button_layout.addWidget(self.login_button, alignment=Qt.AlignmentFlag.AlignCenter)
        form_layout.addWidget(button_container)
        
        # Register link
        register_container = QWidget()
        register_layout = QHBoxLayout(register_container)
        register_layout.setContentsMargins(0, 0, 0, 0)
        
        no_account_label = QLabel("Don't have an account?")
        register_button = QPushButton("Sign Up")
        register_button.setObjectName("linkButton")
        register_button.clicked.connect(self.nav_manager.show_registration)
        
        register_layout.addWidget(no_account_label, alignment=Qt.AlignmentFlag.AlignRight)
        register_layout.addWidget(register_button, alignment=Qt.AlignmentFlag.AlignLeft)
        form_layout.addWidget(register_container)
        
        # Add form to content layout
        content_layout.addWidget(form_frame)
        
        # Set stretch factors
        content_layout.setStretch(0, 1)  # Illustration
        content_layout.setStretch(1, 1)  # Form
        
        main_layout.addLayout(content_layout)
        
    def update_language(self, lang: str):
        self.current_language = "ar" if lang == "العربية" else "en"
        
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - تسجيل الدخول')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("تسجيل الدخول")
                elif widget.text() == "Welcome back! Please enter your details.":
                    widget.setText("مرحباً بعودتك! الرجاء إدخال بياناتك.")
                elif widget.text() == "Username":
                    widget.setText("اسم المستخدم")
                elif widget.text() == "Password":
                    widget.setText("كلمة المرور")
                elif widget.text() == "Language":
                    widget.setText("اللغة")
                elif widget.text() == "Don't have an account?":
                    widget.setText("ليس لديك حساب؟")
                    
            # Update input placeholders
            self.username_input.setPlaceholderText("أدخل اسم المستخدم")
            self.password_input.setPlaceholderText("أدخل كلمة المرور")
            
            # Update buttons
            self.login_button.setText("تسجيل الدخول")
            for button in self.findChildren(QPushButton):
                if button.objectName() == "linkButton":
                    button.setText("إنشاء حساب")
        else:
            self.setWindowTitle('Educational Platform - Login')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText("Sign In")
                elif widget.text() == "مرحباً بعودتك! الرجاء إدخال بياناتك.":
                    widget.setText("Welcome back! Please enter your details.")
                elif widget.text() == "اسم المستخدم":
                    widget.setText("Username")
                elif widget.text() == "كلمة المرور":
                    widget.setText("Password")
                elif widget.text() == "اللغة":
                    widget.setText("Language")
                elif widget.text() == "ليس لديك حساب؟":
                    widget.setText("Don't have an account?")
                    
            # Update input placeholders
            self.username_input.setPlaceholderText("Enter your username")
            self.password_input.setPlaceholderText("Enter your password")
            
            # Update buttons
            self.login_button.setText("Sign In")
            for button in self.findChildren(QPushButton):
                if button.objectName() == "linkButton":
                    button.setText("Sign Up")
                
        # Update user's language preference if logged in
        if self.current_user:
            self.db.update_user_language(self.current_user.id, self.current_language)
        
    def handle_login(self):
        username = self.username_input.text()
        password = self.password_input.text()
        
        if not username or not password:
            self.show_error("يجب ملء جميع الحقول" if self.lang_combo.currentText() == "العربية" else "Please fill in all fields")
            return
            
        user = self.db.verify_user(username, password)
        if user:
            self.current_user = user
            self.nav_manager.show_dashboard(user)
        else:
            self.show_error("اسم المستخدم أو كلمة المرور غير صحيحة" if self.lang_combo.currentText() == "العربية" else "Invalid username or password")
            
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