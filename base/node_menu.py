from PySide6.QtWidgets import (QVBoxLayout, QPushButton, QDialog, QLabel)
from PySide6.QtGui import QCursor
from PySide6.QtCore import Qt

from importlib import reload
import os, string

from base import node
reload(node)

class NodePalette(QDialog):
    def __init__(self, parent=None, editor_window=None):
        super().__init__(parent)
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.Popup)
        self.editor_window = editor_window

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
        node_files = [".".join(f.split(".")[:-1]) for f in os.listdir(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..', 'nodes'))]
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
            btn.clicked.connect(lambda checked, t=node_type: self.add_node_to_scene(t))
            self.layout.addWidget(btn)

    def add_node_to_scene(self, node_type):
        global_pos = QCursor.pos()
        view = self.editor_window.view
        scene_pos = view.mapToScene(view.mapFromGlobal(global_pos))
        
        new_node = node.Node(scene_pos.x(), scene_pos.y(), label=node_type, window=self.editor_window)
        self.editor_window.scene.addItem(new_node)
        self.close()