from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPixmap, QKeyEvent
from PySide6.QtCore import Qt
from importlib import reload
import os, sys

from base import port
from base.utils import text_utils
reload(port)
reload(text_utils)


class Node(QGraphicsRectItem):
    def __init__(self, x, y, width=150, height=45, label="Node", window=None):
        super().__init__(0, 0, width, height)
        self.setPos(x, y)
        self.setBrush(QColor("#e0e0e0"))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.width = width
        self.height = height
        self.editor_window = window
        self.label = label
        self.name = label

        self.connections = []
        self.create_divides()
        self.port_creation()
        self.node_name()
        self.add_icon(path=os.path.join(os.path.dirname(os.path.abspath(__file__)),"..","icons","rivet.svg"))

    def create_divides(self):
        margin = 5
        left_width = self.width * 0.2 - margin
        middle_width = self.width * 0.6 * margin
        right_width = self.width * 0.2 - margin

        self.disable_box = DisableButton(
            margin, margin, left_width, self.height - 2*margin, radius=6, parent=self,
            callback=self.disable_node
        )
        self.render_box = RenderButton(
            self.width - right_width - margin, margin, right_width, self.height - 2*margin, radius=6, parent=self,
            callback=self.render_node
        )

    def disable_node(self):
        print("Node disabled!")

    def render_node(self):
        if self.editor_window:
            self.editor_window.set_rendered_node(self)
        print("Node rendered!")
    
    def port_creation(self):
        port_factory = port.Port(parent=self, width=self.width, height=self.height)
        
        self.port_input = port_factory.create_input_port()
        self.port_output = port_factory.create_output_port()

        self.port_input.parent_node = self
        self.port_output.parent_node = self

        self.port_input.port_selected.connect(self.editor_window.handle_port_selected)
        self.port_output.port_selected.connect(self.editor_window.handle_port_selected)

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for connection in self.connections:
                connection.update_path()
        if change == QGraphicsItem.ItemSelectedChange and value:
            print(f"Node Selected: {self}")
        return super().itemChange(change, value)
    
    def node_name(self):
        font_name = "FiraCode Nerd Font Mono" # make this configurable
        font = QFont(font_name, pointSize=20)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
        self.node_text = QGraphicsTextItem(self.label, parent=self)
        self.node_text.setFont(font)
        self.node_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.node_text.setDefaultTextColor(QColor("#cacaca"))
        self.node_text.setPos(self.width +5, self.height /2 - 20)
        
        self.node_text.document().contentsChanged.connect(lambda: text_utils.sanitise_text(self.node_text))

    def add_icon(self, path=None):
        pixmap = QPixmap(path)
        self.icon = QGraphicsPixmapItem(pixmap, parent=self)
        self.icon.setPos(self.width / 2 - pixmap.height() / 2, self.height / 2 - pixmap.height() / 2)

        # Optional: scale icon to fit height
        max_height = self.rect().height() - 2
        if pixmap.height() > max_height:
            scale_factor = max_height / pixmap.height()
            self.icon.setScale(scale_factor)

    def set_rendered(self, rendered):
        self.is_rendered = rendered
        if rendered:
            self.render_box.setBrush(QColor("#008cff"))
            self.render_box.selected = True
        else:
            self.render_box.setBrush(QColor("#e0e0e0"))
            self.render_box.selected = False

    def __repr__(self):
        pos = self.pos()
        return f"<Node name=({self.name}), pos=({pos.x():.1f}, {pos.y():.1f}), unique_py_id=({hex(id(self))})>"

class RenderButton(QGraphicsRectItem):
    def __init__(self, x, y, width, height, radius=8, parent=None, callback=None):
        super().__init__(x, y, width, height, parent)
        self.radius = radius
        self.setPen(Qt.PenStyle.NoPen)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.callback = callback
        self.selected = False

    def paint(self, painter: QPainter, option, widget=None):
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)
        painter.drawPath(path)

    def mousePressEvent(self, event):
        self.callback()
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        if not self.selected:
            self.setBrush(QColor("#33a3ff"))  # Highlight on hover
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.selected:
            self.setBrush(QColor("#e0e0e0"))
        super().hoverLeaveEvent(event)

class DisableButton(QGraphicsRectItem):
    def __init__(self, x, y, width, height, radius=8, parent=None, callback=None):
        super().__init__(x, y, width, height, parent)
        self.radius = radius
        self.setPen(Qt.PenStyle.NoPen)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setAcceptHoverEvents(True)
        self.callback = callback
        self.selected = False
        self.parent = parent

    def paint(self, painter: QPainter, option, widget=None):
        painter.setBrush(self.brush())
        painter.setPen(self.pen())
        rect = self.rect()
        path = QPainterPath()
        path.addRoundedRect(rect, self.radius, self.radius)
        painter.drawPath(path)

    def mousePressEvent(self, event):
        if self.selected:
            self.setBrush(QColor("#e0e0e0"))
            self.parent.setBrush(QColor("#e0e0e0"))
            self.selected = False
        elif self.callback:
            self.callback()
            self.setBrush(QColor("#ffc34b"))
            self.parent.setBrush(QColor("#9b9b9b"))
            self.selected = True
        else:
            print("WARNING: No callback defined for render button.")
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        if not self.selected:
            self.setBrush(QColor("#ffd277"))
        super().hoverEnterEvent(event)

    def hoverLeaveEvent(self, event):
        if not self.selected:
            self.setBrush(QColor("#e0e0e0"))
        super().hoverLeaveEvent(event)
