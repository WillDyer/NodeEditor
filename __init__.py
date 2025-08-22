from PySide6.QtWidgets import QApplication
from PySide6.QtGui import QIcon
import sys, os
import importlib
import interface.ui as ui
importlib.reload(ui)

app = QApplication.instance() or QApplication(sys.argv)
app.setWindowIcon(QIcon(os.path.join(os.path.dirname(os.path.abspath(__file__)),"icons","autorig.svg")))
window = ui.Interface()
window.show()
app.exec()