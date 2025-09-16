from PySide6.QtWidgets import QGraphicsRectItem, QGraphicsItem, QGraphicsTextItem, QGraphicsPixmapItem, QWidget
from PySide6.QtGui import QColor, QFont, QPainter, QPainterPath, QPixmap
from PySide6.QtCore import Qt, QTimer
from importlib import reload
import os

from base import port
from base.utils import text_utils, node_utils
reload(port)
reload(text_utils)
reload(node_utils)


class Node(QGraphicsRectItem):
    def __init__(self, x, y, width=150, height=45, label="Node", icon=None, window=None, property_widget=None):
        super().__init__(0, 0, width, height)
        self.setPos(x, y)
        self.setBrush(QColor("#e0e0e0"))
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsMovable)
        self.setFlag(QGraphicsItem.GraphicsItemFlag.ItemIsSelectable)
        self.setFlag(QGraphicsItem.ItemSendsGeometryChanges)
        self.width = width
        self.height = height
        self.editor_window = window
        self.property_widget = property_widget
        self.label = label
        self.name = label

        self.connections = []
        self.last_selected_node = []
        self.properties = {}
        self.create_divides()
        self.port_creation()
        self.node_name()
        self.add_icon(path=icon)

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

        if change == QGraphicsItem.ItemSelectedHasChanged:
            scene = self.scene()
            if not scene:
                return super().itemChange(change, value)

            previous_node = getattr(scene, "last_selected_node", None)

            if value:  # Node selected
                if getattr(scene, "selected_node", None) and getattr(scene, "selected_node", None) != self:
                    scene.previous_node = getattr(scene, "selected_node", None)

                # Now set this as the active node
                scene.selected_node = self
                print(f"\nNew Selection: {getattr(scene, 'selected_node', None)},\nPrevious: {getattr(scene, 'previous_node', None)}\n")

            else:  # Node deselected
                if getattr(scene, "selected_node", None) == self:
                    scene.previous_node = scene.selected_node
                    scene.selected_node = None
                    print(f"\nDeselected: {getattr(scene, 'selected_node', None)},\nPrevious: {getattr(scene, 'previous_node', None)}\n")


            previous_node = getattr(scene, "previous_node", None)
            selected_node = getattr(scene, "selected_node", None)

            # Save and remove UI for previous node if it exists
            if previous_node:
                print(f"Saving and removing UI for previous node: {previous_node}")
                previous_node.save_properties_and_remove_ui()

            # Load and restore UI for selected node if it exists
            if selected_node:
                print(f"Loading and restoring UI for selected node: {selected_node}")
                selected_node.load_ui_and_restore_properties()

        return super().itemChange(change, value)
    
    def save_properties_and_remove_ui(self):
        if self.property_widget:
            self.properties = node_utils.save_widget_values(self.property_widget)
            node_utils.remove_last_widget(self.property_widget)

    def load_ui_and_restore_properties(self):
        if not self.property_widget:
            return

        node_utils.remove_last_widget(self.property_widget)

        property_class = node_utils.load_widget_for(self.label, self.property_widget)
        if property_class:
            layout = property_class.return_layout()
            if layout:
                self.property_widget.setLayout(layout)

                if hasattr(self, "properties") and self.properties is not None:
                    node_utils.restore_widget_property(self.property_widget.layout(), self.properties)
    
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
        if path is None:
            path = "rivet.png"
        file_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "interface", "icons")
        path = os.path.join(file_path, path)

        pixmap = QPixmap(path)
        max_height = self.height - 8
        if pixmap.height() > max_height:
            pixmap = pixmap.scaledToHeight(max_height, Qt.TransformationMode.SmoothTransformation)

        self.icon = QGraphicsPixmapItem(pixmap, parent=self)
        rect = self.icon.boundingRect()
        self.icon.setPos(self.width / 2 - rect.width() / 2, self.height / 2 - rect.height() / 2)

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
