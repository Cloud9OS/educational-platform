from src.models.database import Database, Lesson
from datetime import datetime

def init_test_data():
    db = Database()
    
    # Add test users
    teacher = db.add_user("teacher", "Teacher123!", "teacher", "en")
    student = db.add_user("student", "Student123!", "student", "en")
    
    if teacher:
        # Add some test lessons
        lesson1 = Lesson(
            id=0,  # Will be set by database
            title="Introduction to Python",
            title_ar="مقدمة في بايثون",
            description="Learn the basics of Python programming language. This course covers variables, data types, control flow, and functions.",
            description_ar="تعلم أساسيات لغة البرمجة بايثون. تغطي هذه الدورة المتغيرات وأنواع البيانات والتحكم في التدفق والدوال.",
            image_path="resources/images/python.jpg",
            video_path="resources/videos/python_intro.mp4",
            created_by=teacher.id,
            created_at=datetime.now()
        )
        
        lesson2 = Lesson(
            id=0,  # Will be set by database
            title="Web Development Fundamentals",
            title_ar="أساسيات تطوير الويب",
            description="Introduction to HTML, CSS, and JavaScript. Learn how to create modern and responsive websites.",
            description_ar="مقدمة في HTML و CSS و JavaScript. تعلم كيفية إنشاء مواقع ويب حديثة ومتجاوبة.",
            image_path="resources/images/web_dev.jpg",
            video_path="resources/videos/web_dev_intro.mp4",
            created_by=teacher.id,
            created_at=datetime.now()
        )
        
        db.add_lesson(lesson1)
        db.add_lesson(lesson2)
        
if __name__ == "__main__":
    init_test_data() 