from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QDialog, QLabel)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt

import importlib
import os, string
from functools import partial

from base import node
importlib.reload(node)

nodes_dir = os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'base', 'nodes')
node_files = [
    os.path.splitext(f)[0]
    for f in os.listdir(nodes_dir)
    if f.endswith(".py") and not f.startswith("__")
]
node_files = [f for f in node_files if f]
modules = {}
for module_name in node_files:
    full_module_name = f"base.nodes.{module_name}"
    modules[module_name] = importlib.import_module(full_module_name)
    importlib.reload(modules[module_name])


class NodePalette(QDialog):
    def __init__(self, parent=None, editor_window=None, temp_widget=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.editor_window = editor_window
        self.temp_widget = temp_widget

        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5, 0, 0, 5)
        self.setLayout(self.layout)

        self.node_label = QLabel("Tab Menu")
        self.node_label.setStyleSheet("""
            QLabel {
                font-family: "FiraCode Nerd Font Mono";
                font-weight: bold;
                font-size: 15px;
                padding: 5px;
            }
        """)
        self.layout.addWidget(self.node_label)

        self.find_nodes()

    def find_nodes(self):
        node_files = [".".join(f.split(".")[:-1]) for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'base', 'nodes'))]
        try: node_files.remove("")
        except ValueError: pass
        node_files = [f for f in node_files if f not in ["__init__"]]
        node_files = sorted(node_files)

        for node_type in node_files:
            node_name = string.capwords(node_type)
            btn = QPushButton(node_name)
            btn.setFlat(True)
            btn.setStyleSheet("""
                QPushButton {
                    background-color: transparent;
                    border: none;
                    text-align: left;
                    padding: 5px;
                }
                QPushButton:hover {
                    background-color: rgba(50, 50, 50, 1);
                }
                QPushButton:pressed {
                    background-color: rgba(30, 30, 30, 1);
                }
            """)
            # btn.clicked.connect(lambda checked, t=node_type: self.add_node_to_scene(t))
            cls = getattr(modules[node_type], node_type.capitalize())
            btn.clicked.connect(partial(self.add_node_to_scene, cls))
            self.layout.addWidget(btn)

    def add_node_to_scene(self, node_class):
        global_pos = QCursor.pos()
        view = self.editor_window.view
        scene_pos = view.mapToScene(view.mapFromGlobal(global_pos))
        
        #new_node = node.Node(scene_pos.x(), scene_pos.y(), label=node_type, window=self.editor_window)
        print(self.temp_widget)
        new_node_class = node_class(self.editor_window, self.temp_widget)
    
        self.editor_window.scene.addItem(new_node_class.return_widget())
        self.close()