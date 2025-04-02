from PyQt5.QtWidgets import (QWidget, QVBoxLayout, QGridLayout, QPushButton, 
                            QApplication, QSizePolicy)
from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QFont

class VirtualKeyboard(QWidget):
    keyPressed = pyqtSignal(str)
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setup_ui()
        self.setWindowTitle("Virtual Keyboard")
        
    def setup_ui(self):
        self.setStyleSheet("""
            QWidget {
                background-color: #e0e0e0;
            }
            QPushButton {
                background-color: white;
                border: 1px solid #808080;
                border-radius: 5px;
                min-width: 40px;
                min-height: 40px;
                font-family: Arial;
                font-size: 14px;
            }
            QPushButton[specialKey="true"] {
                background-color: #d0d0d0;
            }
            QPushButton:pressed {
                background-color: #a0a0a0;
            }
        """)
        
        main_layout = QVBoxLayout()
        main_layout.setSpacing(5)
        main_layout.setContentsMargins(10, 10, 10, 10)
        
        # Function keys row
        func_layout = QGridLayout()
        func_layout.setSpacing(5)
        
        func_keys = [
            'Esc', 'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 
            'F7', 'F8', 'F9', 'F10', 'F11', 'F12', 'Del', '⌦'
        ]
        
        for i, key in enumerate(func_keys):
            btn = self.create_button(key, special_key=True)
            func_layout.addWidget(btn, 0, i)
        
        # Number row
        num_layout = QGridLayout()
        num_layout.setSpacing(5)
        
        num_keys = [
            '`', '1', '2', '3', '4', '5', '6', '7', '8', '9', '0', '-', '=', 'Backspace'
        ]
        
        for i, key in enumerate(num_keys):
            btn = self.create_button(key)
            if key == 'Backspace':
                btn.setMinimumWidth(90)
            num_layout.addWidget(btn, 0, i)
        
        # QWERTY row
        qwerty_layout = QGridLayout()
        qwerty_layout.setSpacing(5)
        
        qwerty_keys = [
            'Tab', 'Q', 'W', 'E', 'R', 'T', 'Y', 'U', 'I', 'O', 'P', '[', ']', '\\'
        ]
        
        for i, key in enumerate(qwerty_keys):
            btn = self.create_button(key)
            if key == 'Tab':
                btn.setMinimumWidth(60)
            elif key == '\\':
                btn.setMinimumWidth(70)
            qwerty_layout.addWidget(btn, 0, i)
        
        # ASDF row
        asdf_layout = QGridLayout()
        asdf_layout.setSpacing(5)
        
        asdf_keys = [
            'Caps', 'A', 'S', 'D', 'F', 'G', 'H', 'J', 'K', 'L', ';', "'", 'Enter'
        ]
        
        for i, key in enumerate(asdf_keys):
            btn = self.create_button(key)
            if key == 'Caps':
                btn.setMinimumWidth(70)
            elif key == 'Enter':
                btn.setMinimumWidth(110)
            asdf_layout.addWidget(btn, 0, i)
        
        # ZXCV row
        zxcv_layout = QGridLayout()
        zxcv_layout.setSpacing(5)
        
        zxcv_keys = [
            'Shift', 'Z', 'X', 'C', 'V', 'B', 'N', 'M', ',', '.', '/', 'Shift'
        ]
        
        for i, key in enumerate(zxcv_keys):
            btn = self.create_button(key)
            if key == 'Shift' and i == 0:
                btn.setMinimumWidth(90)
            elif key == 'Shift' and i == len(zxcv_keys)-1:
                btn.setMinimumWidth(140)
            zxcv_layout.addWidget(btn, 0, i)
        
        # Space bar row
        space_layout = QGridLayout()
        space_layout.setSpacing(5)
        
        space_keys = ['Ctrl', 'Win', 'Alt', 'Space', 'Alt', 'Fn', 'Ctrl']
        
        for i, key in enumerate(space_keys):
            btn = self.create_button(key)
            if key == 'Space':
                btn.setMinimumWidth(340)
            else:
                btn.setMinimumWidth(60)
                btn.setMaximumHeight(30)
            space_layout.addWidget(btn, 0, i)
        
        # Add all rows to main layout
        main_layout.addLayout(func_layout)
        main_layout.addLayout(num_layout)
        main_layout.addLayout(qwerty_layout)
        main_layout.addLayout(asdf_layout)
        main_layout.addLayout(zxcv_layout)
        main_layout.addLayout(space_layout)
        
        self.setLayout(main_layout)
        self.setFixedSize(800, 300)
    
    def create_button(self, text, special_key=False):
        btn = QPushButton(text)
        btn.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.Preferred)
        
        if special_key:
            btn.setProperty("specialKey", True)
        
        btn.clicked.connect(lambda _, t=text: self.on_key_pressed(t))
        return btn
    
    def on_key_pressed(self, text):
        self.keyPressed.emit(text)
        
    def showEvent(self, event):
        # Center the keyboard on screen when shown
        screen_geometry = QApplication.desktop().screenGeometry()
        x = (screen_geometry.width() - self.width()) // 2
        y = (screen_geometry.height() - self.height()) // 2
        self.move(x, y)
        super().showEvent(event)


# Example usage
if __name__ == "__main__":
    import sys
    
    app = QApplication(sys.argv)
    
    def handle_key_press(key):
        print(f"Key pressed: {key}")
    
    keyboard = VirtualKeyboard()
    keyboard.keyPressed.connect(handle_key_press)
    keyboard.show()
    
    sys.exit(app.exec_())
