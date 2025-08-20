from PySide6.QtWidgets import (
    QGraphicsView, QGraphicsScene, QGraphicsItem,
    QGraphicsRectItem, QGraphicsEllipseItem,
    QGraphicsPathItem, QMainWindow
)
from PySide6.QtGui import QPainterPath, QPen, QColor, QPainter
from PySide6.QtCore import Qt, QPointF
from importlib import reload


from base import node
module = [node]

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

        connection = Connection(node1.port_output, node2.port_input)
        self.scene.addItem(connection)

        # track connection inside nodes
        node1.connections.append(connection)
        node2.connections.append(connection)
