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
        if event.button() == Qt.MouseButton.LeftButton and event.modifiers() & Qt.KeyboardModifier.AltModifier:
            self._last_pan_point = event.pos()
            event.accept()
        else:
            super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self._last_pan_point:
            old_scene_pos = self.mapToScene(self._last_pan_point)
            new_scene_pos = self.mapToScene(event.pos())
            delta = new_scene_pos - old_scene_pos
            self.setTransformationAnchor(QGraphicsView.ViewportAnchor.NoAnchor)
            self.translate(delta.x(), delta.y())
            self._last_pan_point = event.pos()
            event.accept()
        else:
            super().mouseMoveEvent(event)

    def mouseReleaseEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton and event.modifiers() & Qt.KeyboardModifier.AltModifier:
            self._last_pan_point = None
            event.accept()
        else:
            super().mouseReleaseEvent(event)

    def wheelEvent(self, event):
        zoom_in_factor = 1.15
        zoom_out_factor = 1 / zoom_in_factor
        max_scale = 1.5
        min_scale = 0.1

        old_pos = self.mapToScene(event.position().toPoint())

        if event.angleDelta().y() > 0:
            zoom_factor = zoom_in_factor
        else:
            zoom_factor = zoom_out_factor

        new_scale = self.transform().m11() * zoom_factor
        if new_scale < min_scale or new_scale > max_scale:
            return  # stop zooming

        self.scale(zoom_factor, zoom_factor)

        new_pos = self.mapToScene(event.position().toPoint())
        delta = new_pos - old_pos
        self.translate(delta.x(), delta.y())

    def keyPressEvent(self, event):
        if event.key() == Qt.Key_Delete:
            for item in self.scene().selectedItems():
                if isinstance(item, port.Connection):
                    self.scene().removeItem(item)
                    del item
            event.accept()
        else:
            super().keyPressEvent(event)

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


class NodeEditorScene(QGraphicsScene):
    def __init__(self, window, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.window = window

    def mousePressEvent(self, event):
        item = self.itemAt(event.scenePos(), self.views()[0].transform())

        if item is None:
            self.window.selected_ports.clear()
        if self.window.temp_connection is not None:
            self.removeItem(self.window.temp_connection)
            self.window.temp_connection = None
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.window.temp_connection is not None:
            self.window.temp_connection.set_end_pos(event.scenePos())
        super().mouseMoveEvent(event)

class NodeEditorWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Node Editor")
        self.resize(800, 600)
        self.scene = NodeEditorScene(self)
        self.scene.setSceneRect(self.scene.itemsBoundingRect().adjusted(-1000, -1000, 1000, 1000))
        self.view = NodeEditorView(self.scene)
        self.setCentralWidget(self.view)
        self.rendered_node = None
        self.selected_ports = []
        self.temp_connection = None

        self.add_nodes_and_connections()

    def add_nodes_and_connections(self):
        #################################
        # this is a temporary setup     #
        # to demonstrate the node editor#
        #################################
        node1 = node.Node(100, 100, label="Node_1", window=self)
        node2 = node.Node(100, 250, label="Node_2", window=self)
        self.scene.addItem(node1)
        self.scene.addItem(node2)

        """connection = port.Connection(node1.port_output, node2.port_input)
        self.scene.addItem(connection)

        # track connection inside nodes
        node1.connections.append(connection)
        node2.connections.append(connection)"""

        self.set_rendered_node(node2) # default a node to rendered

    def handle_port_selected(self, selected_port):
        if selected_port not in self.selected_ports:
            self.selected_ports.append(selected_port)
            if len(self.selected_ports) == 1:
                self.temp_connection = port.Connection(self.selected_ports[0])
                self.scene.addItem(self.temp_connection)
            if len(self.selected_ports) == 2:
                connection = port.Connection(self.selected_ports[0], self.selected_ports[1])
                self.scene.addItem(connection)

                node1 = self.selected_ports[0].parent_node
                node2 = self.selected_ports[1].parent_node

                node1.connections.append(connection)
                node2.connections.append(connection)

                if self.temp_connection is not None:
                    self.scene.removeItem(self.temp_connection)
                    del self.temp_connection
                    self.temp_connection = None
                self.selected_ports.clear()

    def set_rendered_node(self, node):
        if self.rendered_node and self.rendered_node is not node:
            self.rendered_node.set_rendered(False)
            print(f"Node {self.rendered_node} is no longer rendered.")
        self.rendered_node = node
        node.set_rendered(True)