import sys, qdarktheme, time, os
import PyQt6.QtWidgets as Widgets
import PyQt6.QtCore as Core
from PyQt6 import QtGui
from pyqt_switch import PyQtSwitch

app = Widgets.QApplication(sys.argv)

app_title = "Detector"
media_source = 0
record_on = False
prints_on = False

class GUI(Widgets.QMainWindow):
    def __init__(self, screen_size):
        super().__init__()
        # Screen and App Sizes
        self.screen_width = screen_size.width()
        self.screen_height = screen_size.height()
        self.app_width = 600
        self.app_height = 500
        self.app_x = int((self.screen_width - self.app_width) / 2)
        self.app_y = int((self.screen_height - self.app_height) / 2)
        # INIT WINDOW
        self.setFixedSize(self.app_width, self.app_height)
        self.setWindowTitle(app_title)
        self.setWindowIcon(QtGui.QIcon("./favicon.ico"))
        # MAIN APP LAYOUT
        self.app_layout = Widgets.QVBoxLayout()

        self.choose_harr_layout = Widgets.QHBoxLayout()

        self.harr_combo_label = Widgets.QLabel("Detect:")
        self.choose_harr_layout.addWidget(self.harr_combo_label)

        self.harr_combo = Widgets.QComboBox()
        self.harr_combo.addItems(['Frontal Face', 'Full Body', 'Smile', 'Cat Face'])
        self.choose_harr_layout.addWidget(self.harr_combo)

        self.app_layout.addLayout(self.choose_harr_layout)

        self.choose_source_layout = Widgets.QHBoxLayout()

        self.source_image_button = Widgets.QPushButton("Image")
        self.source_image_button.setStyleSheet('QPushButton { background-color: grey }')
        self.source_image_button.clicked.connect(lambda: self.toggleSource(0))
        self.choose_source_layout.addWidget(self.source_image_button)

        self.source_video_button = Widgets.QPushButton("Video")
        self.source_video_button.setStyleSheet('QPushButton { background-color: darkgrey }')
        self.source_video_button.clicked.connect(lambda: self.toggleSource(1))
        self.choose_source_layout.addWidget(self.source_video_button)

        self.source_camera_button = Widgets.QPushButton("Camera")
        self.source_camera_button.setStyleSheet('QPushButton { background-color: darkgrey }')
        self.source_camera_button.clicked.connect(lambda: self.toggleSource(2))
        self.choose_source_layout.addWidget(self.source_camera_button)

        self.app_layout.addLayout(self.choose_source_layout)

        self.record_detection_layout = Widgets.QHBoxLayout()

        self.record_switch = Widgets.QPushButton("Record detection", self)
        self.record_switch.setStyleSheet('QPushButton { background-color: red;}')
        self.record_switch.clicked.connect(self.toggleRecord)
        self.record_detection_layout.addWidget(self.record_switch)

        self.print_switch = Widgets.QPushButton("Print detections", self)
        self.print_switch.setStyleSheet('QPushButton { background-color: red;}')
        self.print_switch.clicked.connect(self.togglePrints)
        self.record_detection_layout.addWidget(self.print_switch)

        self.app_layout.addLayout(self.record_detection_layout)

        self.start_button = Widgets.QPushButton("Start", self)
        self.app_layout.addWidget(self.start_button)

        # RUN
        self.main_window = Widgets.QWidget()
        self.main_window.setLayout(self.app_layout)
        self.setCentralWidget(self.main_window)
        self.show()

    def toggleSource(self, source):
        global media_source
        media_source = source
        self.source_image_button.setStyleSheet('QPushButton { background-color: darkgrey }')
        self.source_video_button.setStyleSheet('QPushButton { background-color: darkgrey }')
        self.source_camera_button.setStyleSheet('QPushButton { background-color: darkgrey }')
        if source == 0:
            self.source_image_button.setStyleSheet('QPushButton { background-color: grey }')
        elif source == 1:
            self.source_video_button.setStyleSheet('QPushButton { background-color: grey }')
        else:
            self.source_camera_button.setStyleSheet('QPushButton { background-color: grey }')

    def toggleRecord(self):
        global prints_on
        if prints_on:
            prints_on = False
            self.record_switch.setStyleSheet('QPushButton { background-color: green;}')
        else:
            prints_on = True
            self.record_switch.setStyleSheet('QPushButton { background-color: red;}')

    def togglePrints(self):
        global record_on
        if record_on:
            record_on = False
            self.print_switch.setStyleSheet('QPushButton { background-color: green;}')
        else:
            record_on = True
            self.print_switch.setStyleSheet('QPushButton { background-color: red;}')

if __name__ == "__main__":
    gui = GUI(screen_size=app.primaryScreen().size())
    sys.exit(app.exec())