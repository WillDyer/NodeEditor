from PySide6.QtCore import Qt
from PySide6.QtGui import QPalette, QColor
from PySide6.QtWidgets import (
    QHBoxLayout,
    QLabel,
    QWidget,
    QSizePolicy,
    QSpacerItem,
    QComboBox
)


class LowerBarWidget(QWidget):
    def __init__(self, parent_widget):
        super().__init__()
        self.parent_widget = parent_widget

        self.setAutoFillBackground(True)
        palette = self.palette()
        palette.setColor(QPalette.Window, QColor("#1B1B1B"))
        self.setPalette(palette)

        self.setFixedHeight(25)
        self.lower_bar_layout = QHBoxLayout()
        self.lower_bar_layout.setContentsMargins(5, 1, 2, 2)
        self.lower_bar_layout.setSpacing(2)
        self.setLayout(self.lower_bar_layout)

        self.process_definition()
        self.update_status()

    def process_definition(self):
        tmp_label = QLabel("Current Process Running: Im a placeholder :)")
        tmp_label.setStyleSheet("""
            QLabel {
                font-family: "FiraCode Nerd Font Mono";
                font-size: 8pt;
            }
        """)

        self.lower_bar_layout.addWidget(tmp_label, alignment=Qt.AlignmentFlag.AlignVCenter)
        self.lower_bar_layout.addStretch()

    def update_status(self):
        combo = QComboBox()
        combo.addItem("Auto Update")
        combo.addItem("Pause")
        
        combo.setFocusPolicy(Qt.FocusPolicy.NoFocus)

        combo.setStyleSheet("""
            QComboBox {
                font-family: "FiraCode Nerd Font Mono";
                font-size: 10pt;
                background-color: #1B1B1B;
                
            }
        """)

        self.lower_bar_layout.addWidget(combo, alignment=Qt.AlignmentFlag.AlignVCenter)
        