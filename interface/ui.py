from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QSplitter, QMainWindow)
from PySide6.QtCore import Qt, QEvent

from importlib import reload

from base import base
from interface import ui_elements, title_bar
reload(base)
reload(ui_elements)
reload(title_bar)


class Interface(QMainWindow):
    def __init__(self, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        self.setWindowTitle("Node Editor")
        self.setWindowFlags(Qt.Window | Qt.FramelessWindowHint)
        self.initUI()

    def initUI(self):
        central_widget = QWidget()
        main_layout = QVBoxLayout(central_widget)
        main_layout.setContentsMargins(0, 0, 0, 0)
        main_layout.setSpacing(0)

        self.title_bar = title_bar.TitleBarWidget(self)
        main_layout.addWidget(self.title_bar)

        self.splitter = QSplitter(Qt.Horizontal)

        self.temp_property_widget()
        self.node_editor()

        self.splitter.addWidget(self.node_editor_widget)
        self.splitter.addWidget(self.temp_widget)
        main_layout.addWidget(self.splitter)

        self.splitter.setSizes([600, 300])
        self.splitter.setHandleWidth(3)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2e2e2e;
            }
        """)
        self.setCentralWidget(central_widget)

    def title_bar_widget(self):
        self.title_bar = title_bar.TitleBarWidget(self)
        self.titlebar_layout.addWidget(self.title_bar)

    def node_editor(self):
        self.node_editor_widget = QWidget()
        self.node_editor_widget.setMinimumWidth(250)
        self.node_editor_layout = QVBoxLayout(self.node_editor_widget)
        self.node_editor_layout.setContentsMargins(0, 0, 0, 0)
        self.node_editor = base.NodeEditorWindow(self.temp_widget)
        self.node_editor_layout.addWidget(self.node_editor)

    def temp_property_widget(self):
        self.temp_widget = QWidget()
        self.temp_widget.setObjectName("property_widget")
        self.temp_widget.setMinimumWidth(250)
        return self.temp_widget
        """self.temp_property = QVBoxLayout(self.temp_widget)

        ui_elements.label(text="Properties", ptr="properties_label", parent=self.temp_property)
        ui_elements.text_field(text="text field",ptr="text_field", parent=self.temp_property)
        ui_elements.button(text="button", ptr="button", parent=self.temp_property)
        ui_elements.checkbox(text="checkbox", ptr="checkbox", enable=True, parent=self.temp_property)
        ui_elements.dropdown(text="dropdown", ptr="dropdown", items=["item1", "item2"], parent=self.temp_property)
        ui_elements.slider(text="slider", ptr="slider", min_value=0, max_value=10, step=1, parent=self.temp_property)
        self.temp_property.addStretch()"""

    def changeEvent(self, event):
            if event.type() == QEvent.Type.WindowStateChange:
                self.title_bar.window_state_changed(self.windowState())
            super().changeEvent(event)
            event.accept()