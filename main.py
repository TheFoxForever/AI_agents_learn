import sys
from PyQt6.QtWidgets import QApplication, QSystemTrayIcon
from PyQt6.QtGui import QIcon
from gui.main_window import MainWindow
from ai_agent import AIAgent


def main() -> None:
    app = QApplication(sys.argv)
    ai_agent: AIAgent = AIAgent()
    window: MainWindow = MainWindow(ai_agent)
    print(window)  # Print the window object
    print(window.size())  # Print window size
    print(window.pos())  # Print window position

    # Set up system tray icon
    tray_icon: QSystemTrayIcon = QSystemTrayIcon(QIcon("icon.png"), app)
    tray_icon.setToolTip("AI Personal Assistant")
    tray_icon.show()

    window.show()
    print(window.isHidden())  # Check if window is hidden
    print(window.layout())  # Check window layout
    print("Before exec")
    sys.exit(app.exec())
    print("After exec")


if __name__ == "__main__":
    main()
