import sys
from PyQt6.QtWidgets import QApplication
from src.utils.navigation import NavigationManager

def main():
    # Create the application
    app = QApplication(sys.argv)
    
    # Set application style
    app.setStyle('Fusion')
    
    # Initialize navigation manager and show login window
    nav_manager = NavigationManager()
    nav_manager.show_login()
    
    # Start the application event loop
    sys.exit(app.exec())

if __name__ == '__main__':
    main() 