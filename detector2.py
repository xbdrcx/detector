import sys, qdarktheme, time, os
import PyQt6.QtWidgets as Widgets
import PyQt6.QtCore as Core
from PyQt6 import QtGui
from qtwidgets import AnimatedToggle, Toggle

app_title = "Detector"

class GUI(Widgets.QMainWindow):
    def __init__(self, screen_size):
        super().__init__()
        qdarktheme.setup_theme(custom_colors={"primary": "#FFFFFF"})
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
        self.setWindowIcon(QtGui.QIcon("./icons/favicon.ico"))
        # MAIN APP LAYOUT
        self.app_layout = Widgets.QVBoxLayout()
        # self.offset = None

        self.choose_harr_layout = Widgets.QHBoxLayout()

        self.harr_combo_label = Widgets.QLabel("Detect:")
        self.choose_harr_layout.addWidget(self.harr_combo_label)

        self.harr_combo = Widgets.QComboBox()
        self.harr_combo.addItems(['Frontal Face', 'Full Body', 'Smile', 'Cat Face'])
        self.choose_harr_layout.addWidget(self.harr_combo)

        self.app_layout.addLayout(self.choose_harr_layout)

        self.choose_source_layout = Widgets.QHBoxLayout()

        self.source_image_button = Widgets.QPushButton("Image")
        self.choose_source_layout.addWidget(self.source_image_button)

        self.source_image_button = Widgets.QPushButton("Video")
        self.choose_source_layout.addWidget(self.source_image_button)

        self.source_image_button = Widgets.QPushButton("Camera")
        self.choose_source_layout.addWidget(self.source_image_button)

        self.app_layout.addLayout(self.choose_source_layout)

        self.record_detection_layout = Widgets.QHBoxLayout()

        self.toggle_1 = Toggle()
        self.toggle_2 = AnimatedToggle(
            checked_color="#FFB000",
            pulse_checked_color="#44FFB000"
        )
        self.record_detection_layout.addWidget(self.toggle_1)
        self.record_detection_layout.addWidget(self.toggle_2)

        self.app_layout.addLayout(self.record_detection_layout)

        # RUN
        self.main_window = Widgets.QWidget()
        self.main_window.setLayout(self.app_layout)
        self.setCentralWidget(self.main_window)

        self.timer = Core.QTimer(self)
        self.timer.setInterval(100)
        self.timer.timeout.connect(self.update_ui)

    def set_position(self):
        self.timer.stop()
        pos = self.media_range_slider.value()
        self.mediaplayer.set_position(pos / self.mediaplayer.get_length())
        self.timer.start()

    def update_ui(self):
        """Updates the user interface"""

        # Set the slider's position to its corresponding media position
        # Note that the setValue function only takes values of type int,
        # so we must first convert the corresponding media position.
        media_pos = int(self.mediaplayer.get_position() * self.mediaplayer.get_length())
        self.media_range_slider.setValue(media_pos)

        # No need to call this function if nothing is played
        if not self.mediaplayer.is_playing():
            self.timer.stop()

            # # After the video finished, the play button stills shows "Pause",
            # # which is not the desired behavior of a media player.
            # # This fixes that "bug".
            # if not self.mediaplayer.is_paused:
            #     self.timer.stop()

if __name__ == "__main__":
    app = Widgets.QApplication(sys.argv)
    gui = GUI(screen_size=app.primaryScreen().size())
    gui.show()
    sys.exit(app.exec())