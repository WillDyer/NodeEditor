import importlib
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QLayout

last_node = None


def load_widget_for(node, property_widget):
    #remove_last_widget(property_widget)

    module_name = node
    class_name = f"{node.capitalize()}Properties"

    try:
        module = importlib.import_module(f"base.nodes.{module_name}")
        importlib.reload(module)
    except:
        print("Couldn't find module for ui passing")
        return

    try:
        widget_class = getattr(module, class_name, None)
        widget_instance = widget_class(property_widget)
        return widget_instance
    except:
        print(f"Class {class_name} not found in module {module_name}")
        return


def remove_last_widget(property_widget):
    if property_widget is None:
        return

    if isinstance(property_widget, QWidget):
        old_layout = property_widget.layout()
        if old_layout:
            while old_layout.count():
                item = old_layout.takeAt(0)
                widget = item.widget()
                if widget:
                    widget.setParent(None)
                    widget.deleteLater()
            old_layout.deleteLater()
            property_widget.setLayout(None)
        return

    if isinstance(property_widget, QLayout):
        while property_widget.count():
            item = property_widget.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()