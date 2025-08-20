from PySide6.QtWidgets import QApplication
import sys
import importlib
import base.base as base
importlib.reload(base)

app = QApplication.instance() or QApplication(sys.argv)
window = base.NodeEditorWindow()
window.show()
app.exec()