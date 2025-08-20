from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPixmap
from PySide6.QtCore import Qt
from importlib import reload
import os, sys

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

        self.disable_box = DisbaleButton(
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
        print("Node rendered!")

        
    def port_creation(self):
        port_factory = port.Port(parent=self, width=self.width, height=self.height)
        self.port_input = port_factory.create_input_port()
        self.port_output = port_factory.create_output_port()

    def itemChange(self, change, value):
        if change == QGraphicsItem.ItemPositionHasChanged:
            for connection in self.connections:
                connection.update_path()
        return super().itemChange(change, value)
    
    def node_name(self):
        font_name = "FiraCode Nerd Font Mono" # make this configurable
        font = QFont(font_name, pointSize=20)
        font.setLetterSpacing(QFont.SpacingType.AbsoluteSpacing, 1)
        self.node_text = QGraphicsTextItem("node", parent=self)
        self.node_text.setFont(font)
        self.node_text.setTextInteractionFlags(Qt.TextInteractionFlag.TextEditorInteraction)
        self.node_text.setDefaultTextColor(QColor("#cacaca"))
        self.node_text.setPos(self.width +5, self.height /2 - 20)

    def add_icon(self, path=None):
        pixmap = QPixmap(path)
        self.icon = QGraphicsPixmapItem(pixmap, parent=self)
        self.icon.setPos(self.width / 2 - pixmap.height() / 2, self.height / 2 - pixmap.height() / 2)

        # Optional: scale icon to fit height
        max_height = self.rect().height() - 2
        if pixmap.height() > max_height:
            scale_factor = max_height / pixmap.height()
            self.icon.setScale(scale_factor)

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
        if self.selected:
            self.setBrush(QColor("#e0e0e0"))
            self.selected = False
        elif self.callback:
            self.callback()
            self.setBrush(QColor("#008cff"))
            self.selected = True
        else:
            print("WARNING: No callback defined for render button.")
        super().mousePressEvent(event)

    def hoverEnterEvent(self, event):
        self.setBrush(QColor("#33a3ff"))  # Highlight on hover
        super().hoverEnterEvent(event)


class DisbaleButton(QGraphicsRectItem):
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
        self.setBrush(QColor("#ffdd98"))  # Highlight on hover
        super().hoverEnterEvent(event)
