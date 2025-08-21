class NullNode():
    def __init__(self, editor_window):
        self.editor_window = editor_window
        self.scene = editor_window.scene
        self.node_type = "common"
        self.node_id = "null_node"
        self.node_icon = "null_icon.png"