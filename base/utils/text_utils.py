from PySide6.QtCore import Qt
from PySide6.QtWidgets import QWidget, QLayout

def sanitise_text(node_text=None):
            doc = node_text.document()
            current_text = doc.toPlainText()
            new_text = current_text.replace(" ", "_")
            if new_text != current_text:
                doc.blockSignals(True)
                doc.setPlainText(new_text)
                doc.blockSignals(False)


def disable_tab_focus(obj):
    if isinstance(obj, QWidget):
        obj.setFocusPolicy(Qt.NoFocus)
        for child in obj.findChildren(QWidget):
            child.setFocusPolicy(Qt.NoFocus)

    elif isinstance(obj, QLayout):
        for i in range(obj.count()):
            item = obj.itemAt(i)

            widget = item.widget()
            if widget:
                widget.setFocusPolicy(Qt.NoFocus)
                for child in widget.findChildren(QWidget):
                    child.setFocusPolicy(Qt.NoFocus)

            layout = item.layout()
            if layout:
                disable_tab_focus(layout)