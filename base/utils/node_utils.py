import importlib
from PySide6.QtCore import QTimer
from PySide6.QtWidgets import QWidget, QLayout, QComboBox, QLineEdit, QCheckBox, QSpinBox, QDoubleSpinBox, QAbstractSpinBox, QPushButton, QSlider


last_node = None
property = {}


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
            QWidget().setLayout(old_layout)

    if isinstance(property_widget, QLayout):
        while property_widget.count():
            item = property_widget.takeAt(0)
            widget = item.widget()
            if widget:
                widget.setParent(None)
                widget.deleteLater()


def save_widget_values(widget):
    for child in widget.findChildren(QWidget):
        name = child.objectName()
        if not name:
            continue

        if isinstance(child, QComboBox):
            property[name] = child.currentIndex()
        elif isinstance(child, QLineEdit):
            property[name] = child.text()
        elif isinstance(child, QCheckBox):
            property[name] = child.isChecked()
        elif isinstance(child, (QSpinBox, QDoubleSpinBox, QAbstractSpinBox)):
            property[name] = child.value()
        else:
            pass

    return property


def restore_widget_property(layout, properties: dict):
    actionable_types = (QCheckBox, QLineEdit, QComboBox, QSpinBox, QDoubleSpinBox, QSlider, QCheckBox, QPushButton)

    def iterate_layout(layout):
        for i in range(layout.count()):
            item = layout.itemAt(i)

            if item.widget():
                widget = item.widget()
                yield widget

                if widget.layout():
                    yield from iterate_layout(widget.layout())
            elif item.layout():
                yield from iterate_layout(item.layout())

    for child in iterate_layout(layout):
        if not isinstance(child, actionable_types):
            continue
        name = child.objectName()
        if name not in properties:
            continue

        # print(f"restoring {name}: {properties[name]}")

        if isinstance(child, QComboBox):
            child.setCurrentIndex(properties[name])
        elif isinstance(child, QLineEdit):
            child.setText(properties[name])
        elif isinstance(child, QCheckBox):
            child.setChecked(properties[name])
        elif isinstance(child, (QSpinBox, QDoubleSpinBox)):
            child.setValue(properties[name])
        else:
            pass