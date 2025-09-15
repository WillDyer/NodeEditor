from PySide6.QtWidgets import QSpinBox


class text_field():
    def __init__(self, text: str, ptr: str, default=None, parent=None):
        if default is None:
            default = ""
        widget, field, label = self.create_field(text, default, ptr)
        self.set_style(field, label)
        parent.addWidget(widget)

    def create_field(self, text, default, ptr):
        from PySide6.QtWidgets import QLineEdit, QHBoxLayout, QLabel, QWidget
        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        label = QLabel(f"{text}: ")
        label.setFixedWidth(100)
        
        field = QLineEdit(default)
        field.setObjectName(ptr)
        widget.setToolTip(f"<b>Parameter: </b>{ptr}")
        
        layout.addWidget(label)
        layout.addWidget(field)
        return widget, field, label

    def set_style(self, field, label):
        field.setStyleSheet("""
            QLineEdit {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding-left: 5px;
                padding-top: 5px;
                padding-bottom: 5px;
                color: #ffffff;
                background-color: #1e1e1e;
                border: 1px solid #3e3e3e;
                border-radius: 4px;}
            QLineEdit:hover {
                border: 1px solid #5e5e5e;}
            QLineEdit:focus {
                border: 1px solid #007acc;
                background-color: #252526;}
        """)

        label.setStyleSheet("""
            QLabel {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;}
        """)

class button():
    def __init__(self, text: str, ptr: str, parent=None):
        widget, label, button = self.create_button(text, ptr)
        self.set_style(button, label)
        parent.addWidget(widget)

    def create_button(self, text, ptr):
        from PySide6.QtWidgets import QPushButton, QHBoxLayout, QLabel, QWidget, QSizePolicy
        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"{text}: ")
        label.setFixedWidth(100)

        button = QPushButton(text)
        button.setObjectName(ptr)
        button.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)
        widget.setToolTip(f"<b>Parameter: </b> {ptr}")
        
        layout.addWidget(label)
        layout.addWidget(button)
        return widget, label, button
    
    def set_style(self, button, label):
        button.setStyleSheet("""
            QPushButton {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;
                background-color: #333333;
                border: none;
                border-radius: 4px;}
            QPushButton:hover {
                background-color: #444444;}
            QPushButton:pressed {
                background-color: #0072b8;}
        """)

        label.setStyleSheet("""
            QLabel {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;}
        """)

class checkbox():
    def __init__(self, text: str, ptr: str, parent=None, enable=False):
        widget, label, checkbox = self.create_checkbox(text, ptr, enable)
        parent.addWidget(widget)
        self.set_style(checkbox, label)

    def create_checkbox(self, text, ptr, enable):
        from PySide6.QtWidgets import QCheckBox, QWidget, QHBoxLayout, QLabel, QSizePolicy
        from PySide6.QtCore import Qt
        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"{text}: ")
        label.setFixedWidth(100)
        
        checkbox = QCheckBox()
        checkbox.setObjectName(ptr)
        checkbox.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        widget.setToolTip(f"<b>Parameter: </b> {ptr}")
        if enable:
            checkbox.setChecked(True)
        
        layout.addWidget(label)
        layout.addWidget(checkbox)
        layout.addStretch()
        return widget, label, checkbox
    
    def set_style(self, checkbox, label):
        checkbox.setStyleSheet("""
            QCheckBox {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;}
        """)

        label.setStyleSheet("""
            QLabel {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;}
        """)

class dropdown():
    def __init__(self, text: str, ptr: str, items: list, parent=None):
        dropdown, label = self.make_dropdown(text, ptr, items)
        parent.addWidget(dropdown)
        self.set_style(dropdown, label)

    def make_dropdown(self, text, ptr, items):
        from PySide6.QtWidgets import QComboBox, QWidget, QHBoxLayout, QLabel, QSizePolicy
        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setToolTip(f"<b>Parameter: </b> {ptr}")
        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)
        
        dropdown = QComboBox()
        dropdown.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        dropdown.addItems(items)
        dropdown.setObjectName(ptr)

        label = QLabel(f"{text}: ")
        label.setFixedWidth(100)

        layout.addWidget(label)
        layout.addWidget(dropdown)
        return widget, label
    
    def set_style(self, dropdown, label):
        label.setStyleSheet("""
            QLabel {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;}
        """)

        dropdown.setStyleSheet("""
            QComboBox {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                color: #ffffff;
                padding: 5px;
                background-color: #1e1e1e;
                border: 1px solid #3e3e3e;
                border-radius: 4px;}
            QComboBox:hover {
                border: 1px solid #5e5e5e;}
            QComboBox:focus {
                border: 1px solid #007acc;
                background-color: #252526;}
            QComboBox::drop-down {
                subcontrol-origin: padding;
                subcontrol-position: top right;
                width: 20px;
                border-left: 1px solid #555;
            }
            QComboBox::down-arrow {
                image: url(D:/Desktop/NodeEditor/interface/icons/dropdown.svg);
                width: 20px;
                height: 20px;
            }
        """)

class slider():
    def __init__(self, text: str, ptr: str, min_value: int, max_value: int, step: int, parent=None):
        widget, slider, label, spin = self.create_slider(text, ptr, min_value, max_value, step)
        parent.addWidget(widget)
        self.set_style(slider, label)

    def create_slider(self, text, ptr, min_value, max_value, step):
        from PySide6.QtWidgets import QSlider, QHBoxLayout, QLabel, QWidget
        from PySide6.QtCore import Qt
        widget = QWidget()
        widget.setContentsMargins(0, 0, 0, 0)
        widget.setToolTip(f"<b>Parameter: </b> {ptr}")

        layout = QHBoxLayout(widget)
        layout.setContentsMargins(0, 0, 0, 0)

        label = QLabel(f"{text}: ")
        label.setFixedWidth(100)

        spin = SpinBoxNoArrows(min_value, max_value, step)
        spin.setObjectName(f"{ptr}_spin")
        spin.setValue(0)

        slider = QSlider(Qt.Horizontal, widget)
        slider.setObjectName(f"{ptr}_slider")
        slider.setMinimum(min_value)
        slider.setMaximum(max_value)
        slider.setValue(min_value)
        slider.setTickPosition(QSlider.TicksBelow)
        slider.setTickInterval(step)
        slider.setSingleStep(step)

        layout.addWidget(label)
        layout.addWidget(spin)
        layout.addWidget(slider)

        slider.valueChanged.connect(spin.setValue)
        spin.valueChanged.connect(slider.setValue)

        return widget, slider, label, spin
    
    def set_style(self, slider, label):
        label.setStyleSheet("""
            QLabel {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                padding: 8px;
                color: #ffffff;}
        """)

class label():
    def __init__(self, text: str, ptr: str, parent=None):
        label = self.create_label(text, ptr)
        self.set_style(label)
        parent.addWidget(label)

    def create_label(self, text, ptr):
        from PySide6.QtWidgets import QLabel
        label = QLabel(text)
        label.setFixedWidth(100)
        label.setObjectName(ptr)
        label.setToolTip(f"<b>Parameter: </b> {ptr}")
        return label
    
    def set_style(self, label):
        label.setStyleSheet("""
            QLabel {
                font-family: FiraCode Nerd Font Mono;
                font-size: 10px;
                font-weight: bold;
                padding: 8px;
                color: #ffffff;}
        """)

class SpinBoxNoArrows(QSpinBox):
    def __init__(self, min_value=0, max_value=100, step=1, parent=None):
        from PySide6.QtWidgets import QAbstractSpinBox
        super().__init__(parent)
        self.setRange(min_value, max_value)
        self.setSingleStep(step)

        # Hide arrow buttons
        self.setButtonSymbols(QAbstractSpinBox.NoButtons)