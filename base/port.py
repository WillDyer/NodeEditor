from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsRectItem, QGraphicsItem
from PySide6.QtGui import QColor, QPen
from PySide6.QtCore import Qt


class Port:
    def __init__(self, parent, width, height):
        self.parent = parent
        self.width = width
        self.height = height

    def create_input_port(self):
        port_input = QGraphicsEllipseItem(self.width/2-10, 0-18, 16, 16, self.parent)
        port_input.setBrush(QColor("#3498db"))
        port_input.setPen(QPen(Qt.GlobalColor.black, 1))
        return port_input

    def create_output_port(self):
        port_output = QGraphicsEllipseItem(self.width/2-10, self.height+2, 16, 16, self.parent)
        port_output.setBrush(QColor("#3498db"))
        port_output.setPen(QPen(Qt.GlobalColor.black, 1))
        return port_output