from PySide6.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QSplitter)
from PySide6.QtCore import Qt

from importlib import reload

from base import base
from interface import ui_elements
reload(base)
reload(ui_elements)


class Interface(QWidget):
    def __init__(self, *args, **kwargs):
        super(Interface, self).__init__(*args, **kwargs)
        self.setWindowFlags(Qt.Window)
        self.setWindowTitle("Node Editor")
        self.initUI()

    def initUI(self):
        self.horizontalLayout = QHBoxLayout(self)
        self.horizontalLayout.setContentsMargins(0, 0, 0, 0)
        self.splitter = QSplitter(Qt.Horizontal)

        self.temp_property_widget()
        self.node_editor()

        self.splitter.addWidget(self.node_editor_widget)
        self.splitter.addWidget(self.temp_widget)

        self.horizontalLayout.addWidget(self.splitter)

        self.splitter.setSizes([600, 300])
        self.splitter.setHandleWidth(3)
        self.splitter.setStyleSheet("""
            QSplitter::handle {
                background-color: #2e2e2e;
            }
        """)

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