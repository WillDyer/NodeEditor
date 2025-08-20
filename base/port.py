from PySide6.QtWidgets import QGraphicsObject, QGraphicsEllipseItem, QGraphicsPathItem, QGraphicsItem
from PySide6.QtGui import QColor, QPen, QPainterPath, QPainter
from PySide6.QtCore import Qt, Signal, QRectF


class Port:
    def __init__(self, parent, width, height):
        self.parent = parent
        self.width = width
        self.height = height

    def create_input_port(self):
        port_input = NoHighlightEllipse(self.width/2-10, 0-18, 16, 16, self.parent)
        port_input.setBrush(QColor("#3498db"))
        port_input.setPen(QPen(Qt.GlobalColor.black, 1))
        port_input.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable, True)
        return port_input

    def create_output_port(self):
        port_output = NoHighlightEllipse(self.width/2-10, self.height+2, 16, 16, self.parent)
        port_output.setBrush(QColor("#3498db"))
        port_output.setPen(QPen(Qt.GlobalColor.black, 1))
        port_output.setFlag(QGraphicsObject.GraphicsItemFlag.ItemIsSelectable, True)
        return port_output
    

class Connection(QGraphicsPathItem):
    def __init__(self, start_port: QGraphicsEllipseItem, end_port: QGraphicsEllipseItem):
        super().__init__()
        self.start_port = start_port
        self.end_port = end_port
        self.selected = False
        self.setPen(QPen(QColor("#2eaccc"), 2))
        self.default_pen = QPen(QColor("#2eaccc"), 2)
        self.hover_pen = QPen(QColor("#6dbacd"), 2)
        self.setZValue(-1)
        self.setFlag(QGraphicsItem.ItemIsSelectable, True)
        self.setFlag(QGraphicsItem.ItemIsFocusable, True)
        self.setAcceptHoverEvents(True)
        self.update_path()

    def update_path(self):
        start = self.start_port.mapToScene(self.start_port.boundingRect().center())
        end = self.end_port.mapToScene(self.end_port.boundingRect().center())
        path = QPainterPath(start)
        dy = max(abs(end.y() - start.y()) * 0.5, 90)
        path.cubicTo(start.x(), start.y() + dy, end.x(), end.y() - dy, end.x(), end.y())

        self.setPath(path)

    def paint(self, painter, option, widget=None):
        painter.setPen(self.pen())
        painter.drawPath(self.path())

    def mousePressEvent(self, event):
        if self.selected:
            self.setPen(self.default_pen)
            self.selected = False
        else:
            self.setPen(self.hover_pen)
            self.selected = True
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        if not self.selected:
            self.setPen(self.hover_pen)
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.selected:
            self.setPen(self.default_pen)
        super().hoverLeaveEvent(event)

class NoHighlightEllipse(QGraphicsObject):
    port_selected = Signal(object)
    def __init__(self, x, y, w, h, parent=None):
        super().__init__(parent)
        self.setAcceptHoverEvents(True)
        self.setPos(x, y)
        self._rect = QRectF(0, 0, w, h)
        self._brush = QColor("#3498db")
        self._pen = QPen(Qt.GlobalColor.black, 1)

    def boundingRect(self):
        return self._rect

    def paint(self, painter, option, widget=None):
        painter.setBrush(self._brush)
        painter.setPen(self._pen)
        painter.drawEllipse(self._rect)

    def setBrush(self, brush):
        self._brush = brush
        self.update()

    def brush(self):
        return self._brush

    def setPen(self, pen):
        self._pen = pen
        self.update()

    def pen(self):
        return self._pen

    def hoverEnterEvent(self, event):
        self.setBrush(QColor("#4ea4de"))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        self.setBrush(QColor("#3498db"))
        super().hoverLeaveEvent(event)

    def itemChange(self, change, value):
        if change == QGraphicsObject.ItemSelectedChange and value:
            print(value)
            self.port_selected.emit(self)
        return super().itemChange(change, value)