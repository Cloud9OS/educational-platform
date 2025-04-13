import os
import shutil
from datetime import datetime
from typing import Optional

class FileManager:
    _instance = None
    _base_path: str = "media"
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(FileManager, cls).__new__(cls)
        return cls._instance
    
    def __init__(self):
        # Create necessary directories if they don't exist
        self._create_directories()
        
    def _create_directories(self):
        """Create necessary directories for media storage"""
        directories = [
            os.path.join(self._base_path, "images"),
            os.path.join(self._base_path, "videos"),
            os.path.join(self._base_path, "temp")
        ]
        
        for directory in directories:
            os.makedirs(directory, exist_ok=True)
            
    def save_image(self, source_path: str, lesson_id: int) -> Optional[str]:
        """Save an image file and return the new path"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lesson_{lesson_id}_{timestamp}.jpg"
            dest_path = os.path.join(self._base_path, "images", filename)
            
            # Copy file to destination
            shutil.copy2(source_path, dest_path)
            return dest_path
        except Exception as e:
            print(f"Error saving image: {e}")
            return None
            
    def save_video(self, source_path: str, lesson_id: int) -> Optional[str]:
        """Save a video file and return the new path"""
        try:
            # Generate unique filename
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"lesson_{lesson_id}_{timestamp}.mp4"
            dest_path = os.path.join(self._base_path, "videos", filename)
            
            # Copy file to destination
            shutil.copy2(source_path, dest_path)
            return dest_path
        except Exception as e:
            print(f"Error saving video: {e}")
            return None
            
    def delete_media(self, file_path: str) -> bool:
        """Delete a media file"""
        try:
            if os.path.exists(file_path):
                os.remove(file_path)
                return True
            return False
        except Exception as e:
            print(f"Error deleting file: {e}")
            return False
            
    def cleanup_temp_files(self):
        """Clean up temporary files"""
        temp_dir = os.path.join(self._base_path, "temp")
        try:
            for file in os.listdir(temp_dir):
                file_path = os.path.join(temp_dir, file)
                if os.path.isfile(file_path):
                    os.remove(file_path)
        except Exception as e:
            print(f"Error cleaning up temp files: {e}")
            
    def get_media_path(self, file_type: str, filename: str) -> Optional[str]:
        """Get the full path for a media file"""
        try:
            if file_type == "image":
                return os.path.join(self._base_path, "images", filename)
            elif file_type == "video":
                return os.path.join(self._base_path, "videos", filename)
            return None
        except Exception as e:
            print(f"Error getting media path: {e}")
            return None 