from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsRectItem, QGraphicsEllipseItem,
    QGraphicsPathItem, QMainWindow
)
from PySide6.QtGui import QPainterPath, QPen, QColor, QPainter
from PySide6.QtCore import Qt, QPointF, QRectF
from importlib import reload


from base import node, port
module = [node, port]

for py in module:
    reload(py)

class NodeEditorView(QGraphicsView):
    def __init__(self, scene):
        super().__init__(scene)
        self.setRenderHint(QPainter.RenderHint.Antialiasing)
        self.setDragMode(QGraphicsView.DragMode.NoDrag)
        self._last_pan_point = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._last_pan_point = event.pos()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._last_pan_point:
            delta = self.mapToScene(event.pos()) - self.mapToScene(self._last_pan_point)
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
            self.translate(delta.x(), delta.y())
            self._last_pan_point = event.pos()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.MiddleButton:
            self._last_pan_point = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def drawBackground(self, painter: QPainter, rect: QRectF):
        super().drawBackground(painter, rect)
        grid_size = 50
        pen = QPen(QColor("#424242"), 0.5)
        painter.setPen(pen)

        left = int(rect.left()) - (int(rect.left()) % grid_size)
        top = int(rect.top()) - (int(rect.top()) % grid_size)

        for x in range(left, int(rect.right()), grid_size):
            painter.drawLine(x, rect.top(), x, rect.bottom())
        for y in range(top, int(rect.bottom()), grid_size):
            painter.drawLine(rect.left(), y, rect.right(), y)


class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Editor")
        self.resize(800, 600)
        self.scene = QGraphicsScene()
        self.view = NodeEditorView(self.scene)
        self.setCentralWidget(self.view)
        self.add_nodes_and_connections()

    def add_nodes_and_connections(self):
        node1 = node.Node(100, 100, label="Node 1")
        node2 = node.Node(100, 250, label="Node 2")
        self.scene.addItem(node1)
        self.scene.addItem(node2)

        connection = port.Connection(node1.port_output, node2.port_input)
        self.scene.addItem(connection)

        # track connection inside nodes
        node1.connections.append(connection)
        node2.connections.append(connection)
