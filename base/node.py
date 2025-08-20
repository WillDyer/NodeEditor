from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsEllipseItem, QGraphicsItem, QGraphicsView
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt
from importlib import reload

from base import port
reload(port)


class Node(QGraphicsRectItem):
    def __init__(self, x, y, width=150, height=45, label="Node"):
        super().__init__(0, 0, width, height)
        self.setPos(x, y)
        self.setBrush(QColor("#e0e0e0"))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.width = width
        self.height = height

        self.connections = []  # Track connections
        
        port_factory = port.Port(parent=self, width=self.width, height=self.height)
        self.port_input = port_factory.create_input_port()
        self.port_output = port_factory.create_output_port()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for connection in self.connections:
                connection.update_path()
        return super().itemChange(change, value)