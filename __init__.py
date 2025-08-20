from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import sys, os
import importlib
import base.base as base
importlib.reload(base)

app = QApplication.instance() or QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons","autorig.svg")))
window = base.NodeEditorWindow()
window.show()
app.exec()