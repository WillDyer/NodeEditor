from PySide6.QtCore import QSize, Qt, QTimer
from PySide6.QtGui import QPalette, QColor, QPixmap, QPainter, QIcon
from PySide6.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QLabel,
    QMainWindow,
    QStyle,
    QToolButton,
    QVBoxLayout,
    QWidget,
    QMenuBar,
    QSizePolicy,
    QSpacerItem
)
import os


class TitleBarWidget(QWidget):
    def __init__(self, parent_window):
        super().__init__()
        self.parent_window = parent_window
        self.initial_pos = None
        self.is_maximized = False
        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#1B1B1B"))
        self.setPalette(palette)

        self.setFixedHeight(35)
        self.title_bar_layout = QHBoxLayout()
        self.title_bar_layout.setContentsMargins(1, 1, 1, 1)
        self.title_bar_layout.setSpacing(2)
        self.setLayout(self.title_bar_layout)

        self.menu_items()
        self.title_widget()
        self.window_controls()


    def title_widget(self):
        self.title_layout = QHBoxLayout()

        self.logo_holder = QLabel()
        self.logo = QPixmap(os.path.join(os.path.dirname(os.path.abspath(__file__)), "icons", "autorig.png"))
        self.logo_scaled = self.logo.scaled(
            20, 20,
            Qt.AspectRatioMode.KeepAspectRatio,
            Qt.TransformationMode.SmoothTransformation
        )
        self.logo_holder.setPixmap(self.logo_scaled)
        self.logo_holder.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.title = QLabel("NodeEditor")
        self.title.setStyleSheet("font-weight: bold;")
        self.title.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)

        self.title_layout.addWidget(self.logo_holder)
        self.title_layout.addWidget(self.title)
        self.title_bar_layout.addStretch()
        self.title_bar_layout.addLayout(self.title_layout)

        return self.title_layout

    def menu_items(self):
        menu_bar = QMenuBar(self)
        menu_bar.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        menu_bar.setStyleSheet("""
            QMenuBar {
                font-family: "FiraCode Nerd Font Mono";
                font-size: 10pt;
                margin: 5px;
                padding: 0px;
                border: none;
            }
            QMenuBar::item {
                margin: 0px;
                padding: 0px 5px;  /* just enough to separate items */
            }
        """)

        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction("Open")
        file_menu.addAction("Save")
        file_menu.addAction("Exit")

        pref_menu = menu_bar.addMenu("&Pref")
        pref_menu.addAction("Font")
        pref_menu.addAction("Themes")

        # Add menu bar as a normal widget
        self.title_bar_layout.addWidget(menu_bar)

    def window_controls(self):
        # Minimize
        self.min_button = QToolButton()
        self.min_button.setIcon(white_icon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMinButton)))
        # below crashing app
        self.min_button.clicked.connect(lambda: self.parent_window.showMinimized())

        # Maximize / Restore toggle
        self.max_button = QToolButton()
        self.max_button.setIcon(white_icon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarMaxButton)))
        self.max_button.clicked.connect(self.toggle_max_restore)

        # Close
        self.close_button = QToolButton()
        self.close_button.setIcon(white_icon(self.style().standardIcon(QStyle.StandardPixmap.SP_TitleBarCloseButton)))
        self.close_button.clicked.connect(lambda: self.parent_window.close())

        button_style = """
                    QToolButton {
                        background-color: transparent;
                        border: none;
                        border-radius: 4px;
                        color: #ffffff;
                    }

                    QToolButton:hover {
                        background-color: #505050;
                    }

                    QToolButton:pressed {
                        background-color: #1c1c1c;
                    }
                    """

        self.title_bar_layout.addStretch()
        for btn in [self.min_button, self.max_button, self.close_button]:
            btn.setFocusPolicy(Qt.FocusPolicy.NoFocus)
            btn.setFixedSize(QSize(28, 28))
            btn.setSizePolicy(QSizePolicy.Policy.Fixed, QSizePolicy.Policy.Fixed)
            btn.setStyleSheet(button_style)
            self.title_bar_layout.addWidget(btn)
        

    def toggle_max_restore(self):
        window = self.parent_window
        screen_geom = window.screen().availableGeometry()

        if getattr(self, 'is_maximized', False):
            window.showNormal()
            normal_width, normal_height = 1000, 600
            window.resize(normal_width, normal_height)

            x = screen_geom.x() + (screen_geom.width() - normal_width) // 2
            y = screen_geom.y() + (screen_geom.height() - normal_height) // 2
            window.move(x, y)
            self.is_maximized = False
        else:
            screen_geom = window.screen().availableGeometry()
            window.setGeometry(screen_geom)
            self.is_maximized = True

    def mousePressEvent(self, event):
        if event.button() == Qt.LeftButton:
            self.initial_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.initial_pos is not None and not self.parent_window.isMaximized():
            delta = event.position().toPoint() - self.initial_pos
            self.parent_window.move(
                self.parent_window.x() + delta.x(),
                self.parent_window.y() + delta.y()
            )
        super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        self.initial_pos = None
        super().mouseReleaseEvent(event)

def white_icon(style_icon, size=28):
    # Get standard pixmap from style
    pixmap = style_icon.pixmap(size, size)
    
    # Create a transparent pixmap
    white_pixmap = QPixmap(pixmap.size())
    white_pixmap.fill(QColor(0, 0, 0, 0))  # fully transparent
    
    # Paint the pixmap white
    painter = QPainter(white_pixmap)
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_Source)
    painter.drawPixmap(0, 0, pixmap)
    
    painter.setCompositionMode(QPainter.CompositionMode.CompositionMode_SourceIn)
    painter.fillRect(white_pixmap.rect(), QColor(255, 255, 255))  # white overlay
    painter.end()
    
    return QIcon(white_pixmap)