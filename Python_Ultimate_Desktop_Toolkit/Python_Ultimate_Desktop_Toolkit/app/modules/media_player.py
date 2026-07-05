from PySide6.QtCore import QUrl, Qt
from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QListWidget, QSlider, QLineEdit, QLabel
from app.widgets.section import make_title

try:
    from PySide6.QtMultimedia import QMediaPlayer, QAudioOutput
    from PySide6.QtMultimediaWidgets import QVideoWidget
    MULTIMEDIA_OK = True
except Exception:
    MULTIMEDIA_OK = False


class MultimediaPage(QWidget):
    def __init__(self, logger=None):
        super().__init__()
        self.logger = logger
        layout = QVBoxLayout(self)
        layout.setContentsMargins(24, 24, 24, 24)
        layout.addWidget(make_title("Multimedia Player", "Play audio/video files, playlist and stream URL."))

        if not MULTIMEDIA_OK:
            layout.addWidget(QLabel("Qt Multimedia is not available in this PySide6 installation."))
            return

        self.player = QMediaPlayer()
        self.audio = QAudioOutput()
        self.player.setAudioOutput(self.audio)
        self.audio.setVolume(0.5)

        self.video = QVideoWidget()
        self.video.setMinimumHeight(330)
        self.player.setVideoOutput(self.video)
        layout.addWidget(self.video)

        self.playlist = QListWidget()
        self.playlist.itemDoubleClicked.connect(self.play_selected)
        layout.addWidget(self.playlist)

        controls = QHBoxLayout()
        for text, method in [("Add Files", self.add_files), ("Play", self.play), ("Pause", self.pause), ("Stop", self.stop)]:
            btn = QPushButton(text)
            btn.clicked.connect(method)
            controls.addWidget(btn)
        self.volume = QSlider(Qt.Horizontal)
        self.volume.setRange(0, 100)
        self.volume.setValue(50)
        self.volume.valueChanged.connect(lambda value: self.audio.setVolume(value / 100))
        controls.addWidget(QLabel("Volume"))
        controls.addWidget(self.volume)
        layout.addLayout(controls)

        streambar = QHBoxLayout()
        self.url_input = QLineEdit()
        self.url_input.setPlaceholderText("Radio/video stream URL")
        stream_btn = QPushButton("Play Stream")
        stream_btn.clicked.connect(self.play_stream)
        streambar.addWidget(self.url_input)
        streambar.addWidget(stream_btn)
        layout.addLayout(streambar)

    def log(self, msg):
        if self.logger:
            self.logger.log(msg)

    def add_files(self):
        paths, _ = QFileDialog.getOpenFileNames(self, "Add media files", "", "Media Files (*.mp3 *.wav *.mp4 *.avi *.mkv);;All Files (*)")
        for path in paths:
            self.playlist.addItem(path)
        if paths:
            self.log(f"Added {len(paths)} media files")

    def play_selected(self):
        item = self.playlist.currentItem()
        if item:
            self.player.setSource(QUrl.fromLocalFile(item.text()))
            self.player.play()

    def play(self):
        if self.player.source().isEmpty():
            self.play_selected()
        else:
            self.player.play()

    def pause(self):
        self.player.pause()

    def stop(self):
        self.player.stop()

    def play_stream(self):
        url = self.url_input.text().strip()
        if url:
            self.player.setSource(QUrl(url))
            self.player.play()
            self.log(f"Playing stream: {url}")
