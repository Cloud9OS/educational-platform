from PyQt6.QtWidgets import (QMainWindow, QWidget, QVBoxLayout, QHBoxLayout,
                            QLabel, QPushButton, QScrollArea, QFrame, QSizePolicy,
                            QSlider)
from PyQt6.QtCore import Qt, QUrl, QTimer
from PyQt6.QtGui import QFont, QPixmap, QIcon
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from src.models.database import Lesson

class LessonDetailWindow(QMainWindow):
    def __init__(self, lesson: Lesson, language: str):
        super().__init__()
        self.lesson = lesson
        self.current_language = language  # Get language from user
        self.init_ui()
        # Set initial language
        self.update_ui_text()
        
    def init_ui(self):
        self.setWindowTitle('Lesson Details')
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
                font-size: 24px;
                font-weight: bold;
                color: #89b4fa;
            }
            QLabel#descriptionLabel {
                font-size: 16px;
                line-height: 1.6;
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
            QPushButton:disabled {
                background-color: #45475a;
                color: #6c7086;
            }
            QScrollArea {
                border: none;
                background-color: transparent;
            }
            QFrame {
                background-color: #313244;
                border-radius: 10px;
            }
            QSlider::groove:horizontal {
                border: none;
                height: 6px;
                background: #45475a;
                border-radius: 3px;
            }
            QSlider::handle:horizontal {
                background: #89b4fa;
                width: 16px;
                height: 16px;
                margin: -5px 0;
                border-radius: 8px;
            }
            QSlider::handle:horizontal:hover {
                background: #b4befe;
            }
        """)
        
        # Create central widget and main layout
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)
        main_layout.setSpacing(20)
        main_layout.setContentsMargins(20, 20, 20, 20)
        
        # Content container
        content_frame = QFrame()
        content_layout = QVBoxLayout(content_frame)
        content_layout.setSpacing(20)
        content_layout.setContentsMargins(20, 20, 20, 20)
        
        # Title section
        title_label = QLabel()
        title_label.setObjectName("titleLabel")
        title_label.setWordWrap(True)
        title_label.setAlignment(Qt.AlignmentFlag.AlignLeft)
        content_layout.addWidget(title_label)
        
        # Media section
        media_layout = QHBoxLayout()
        media_layout.setSpacing(20)
        
        # Video section (left side)
        video_container = QFrame()
        video_container.setMinimumWidth(800)
        video_layout = QVBoxLayout(video_container)
        video_layout.setContentsMargins(0, 0, 0, 0)
        
        # Video player
        self.video_widget = QVideoWidget()
        self.video_widget.setMinimumHeight(450)
        self.media_player = QMediaPlayer()
        self.audio_output = QAudioOutput()
        self.media_player.setAudioOutput(self.audio_output)
        self.media_player.setVideoOutput(self.video_widget)
        video_layout.addWidget(self.video_widget)
        
        # Video controls
        controls_frame = QFrame()
        controls_layout = QVBoxLayout(controls_frame)
        controls_layout.setContentsMargins(10, 10, 10, 10)
        
        # Progress slider
        self.progress_slider = QSlider(Qt.Orientation.Horizontal)
        self.progress_slider.setEnabled(False)
        controls_layout.addWidget(self.progress_slider)
        
        # Buttons
        buttons_layout = QHBoxLayout()
        
        self.play_button = QPushButton("Play")
        try:
            self.play_button.setIcon(QIcon("resources/icons/play.png"))
            self.play_button.setText("")  # Clear text if icon loaded
        except:
            pass  # Keep text if icon failed to load
        self.play_button.setFixedSize(40, 40)
        self.play_button.clicked.connect(self.toggle_playback)
        buttons_layout.addWidget(self.play_button)
        
        self.stop_button = QPushButton("Stop")
        try:
            self.stop_button.setIcon(QIcon("resources/icons/stop.png"))
            self.stop_button.setText("")  # Clear text if icon loaded
        except:
            pass  # Keep text if icon failed to load
        self.stop_button.setFixedSize(40, 40)
        self.stop_button.clicked.connect(self.media_player.stop)
        buttons_layout.addWidget(self.stop_button)
        
        buttons_layout.addStretch()
        controls_layout.addLayout(buttons_layout)
        video_layout.addWidget(controls_frame)
        
        media_layout.addWidget(video_container, stretch=2)
        
        # Image section (right side)
        image_container = QFrame()
        image_layout = QVBoxLayout(image_container)
        image_layout.setContentsMargins(0, 0, 0, 0)
        
        image_label = QLabel()
        image_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        pixmap = QPixmap(self.lesson.image_path)
        if not pixmap.isNull():
            scaled_pixmap = pixmap.scaled(350, 350, Qt.AspectRatioMode.KeepAspectRatio, Qt.TransformationMode.SmoothTransformation)
            image_label.setPixmap(scaled_pixmap)
        else:
            image_label.setText("No image available")
            image_label.setStyleSheet("color: #6c7086; font-size: 16px;")
        
        image_layout.addWidget(image_label)
        media_layout.addWidget(image_container, stretch=1)
        
        content_layout.addLayout(media_layout)
        
        # Description
        desc_label = QLabel()
        desc_label.setObjectName("descriptionLabel")
        desc_label.setWordWrap(True)
        desc_label.setAlignment(Qt.AlignmentFlag.AlignJustify)
        content_layout.addWidget(desc_label)
        
        main_layout.addWidget(content_frame)
        
        # Set up video player
        if self.lesson.video_path:
            try:
                self.media_player.setSource(QUrl.fromLocalFile(self.lesson.video_path))
                self.media_player.durationChanged.connect(self.update_duration)
                self.media_player.positionChanged.connect(self.update_position)
                self.progress_slider.sliderMoved.connect(self.set_position)
            except Exception:
                self.handle_video_error()
        else:
            self.handle_video_error()
        
    def update_ui_text(self):
        if self.current_language == "ar":
            self.setWindowTitle('منصة التعليم - تفاصيل الدرس')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText(self.lesson.title_ar)
                elif widget.objectName() == "descriptionLabel":
                    widget.setText(self.lesson.description_ar)
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "Back":
                    button.setText("رجوع")
        else:
            self.setWindowTitle('Educational Platform - Lesson Details')
            # Update all text elements
            for widget in self.findChildren(QLabel):
                if widget.objectName() == "titleLabel":
                    widget.setText(self.lesson.title)
                elif widget.objectName() == "descriptionLabel":
                    widget.setText(self.lesson.description)
                    
            # Update buttons
            for button in self.findChildren(QPushButton):
                if button.text() == "رجوع":
                    button.setText("Back")
            
    def toggle_playback(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.play_button.setIcon(QIcon("resources/icons/play.png"))
        else:
            self.media_player.play()
            self.play_button.setIcon(QIcon("resources/icons/pause.png"))
            
    def update_duration(self, duration):
        self.progress_slider.setEnabled(True)
        self.progress_slider.setRange(0, duration)
        
    def update_position(self, position):
        self.progress_slider.setValue(position)
        
    def set_position(self, position):
        self.media_player.setPosition(position)
            
    def handle_video_error(self):
        self.video_widget.setStyleSheet("background-color: #313244;")
        error_label = QLabel("Video not available")
        error_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        error_label.setStyleSheet("color: #f38ba8; font-size: 16px;")
        self.video_widget.layout().addWidget(error_label)
        self.play_button.setEnabled(False)
        self.stop_button.setEnabled(False)
        self.progress_slider.setEnabled(False)
        
    def closeEvent(self, event):
        self.media_player.stop()
        event.accept()
        
    def resizeEvent(self, event):
        super().resizeEvent(event)
        # Update video widget size to maintain aspect ratio
        if self.video_widget.height() < self.video_widget.width() / 16 * 9:
            self.video_widget.setMinimumHeight(self.video_widget.width() / 16 * 9) 