from importlib import reload

from PySide6.QtWidgets import QVBoxLayout

from base import node
from base.utils import text_utils
from interface import ui_elements
reload(node)
reload(ui_elements)
reload(text_utils)


class Attr():
    def __init__(self, editor_window, temp_widget):
        self.editor_window = editor_window
        self.scene = editor_window.scene
        self.node_type = "common"
        self.node_id = "attr"
        self.node_icon = "rivet.png"

        self.attr_node = node.Node(0,0, label=self.node_id, icon=self.node_icon, window=editor_window, property_widget=temp_widget)
        
    def return_widget(self):
        return self.attr_node

class AttrProperties():
    def __init__(self, property_widget):
        self.property_widget = property_widget
        self.create_node_ui()

    def create_node_ui(self):
        self.temp_property = QVBoxLayout(self.property_widget)

        ui_elements.label(text="Properties", ptr="properties_label", parent=self.temp_property)
        ui_elements.text_field(text="text field",ptr="text_field", parent=self.temp_property)
        ui_elements.button(text="button", ptr="button", parent=self.temp_property)
        ui_elements.checkbox(text="checkbox", ptr="checkbox", enable=True, parent=self.temp_property)
        ui_elements.dropdown(text="dropdown", ptr="dropdown", items=["item1", "item2"], parent=self.temp_property)
        ui_elements.slider(text="slider", ptr="slider", min_value=0, max_value=10, step=1, parent=self.temp_property)
        self.temp_property.addStretch()
        text_utils.disable_tab_focus(self.temp_property)
