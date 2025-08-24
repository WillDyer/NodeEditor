from importlib import reload

from base import node
reload(node)


class Null():
    def __init__(self, editor_window, temp_widget):
        self.editor_window = editor_window
        self.scene = editor_window.scene
        self.node_type = "common"
        self.node_id = "null"
        self.node_icon = "autorig.png"

        self.null_node = node.Node(0,0, label=self.node_id, icon=self.node_icon, window=editor_window, property_widget=temp_widget)
        
    def return_widget(self):
        return self.null_node
    
class NullProperties():
    def __init__(self, property_widget):
        print("No Widget for a null node, empty ui")