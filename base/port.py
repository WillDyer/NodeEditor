from PySide6.QtWidgets import QGraphicsEllipseItem, QGraphicsPathItem
from PySide6.QtGui import QColor, QPen, QPainterPath
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
    

class Connection(QGraphicsPathItem):
    def __init__(self, start_port: QGraphicsEllipseItem, end_port: QGraphicsEllipseItem):
        super().__init__()
        self.start_port = start_port
        self.end_port = end_port
        self.setPen(QPen(QColor("#2eaccc"), 2))
        self.setZValue(-1)
        self.update_path()

    def update_path(self):
        start = self.start_port.mapToScene(self.start_port.boundingRect().center())
        end = self.end_port.mapToScene(self.end_port.boundingRect().center())
        path = QPainterPath(start)
        #mid_y = (start.y() + end.y()) / 2
        dy = max(abs(end.y() - start.y()) * 0.5, 90)
        #path.cubicTo(start.x(), mid_y, end.x(), mid_y, end.x(), end.y())
        path.cubicTo(start.x(), start.y() + dy, end.x(), end.y() - dy, end.x(), end.y())

        self.setPath(path)