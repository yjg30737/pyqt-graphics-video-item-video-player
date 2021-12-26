from mutagen import mp4

from PyQt5.QtCore import QUrl, pyqtSignal
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QLabel, QPushButton, QHBoxLayout, QVBoxLayout

from pyqt_graphics_video_item_video_player.videoSlider import VideoSlider
from pyqt_resource_helper.pyqtResourceHelper import PyQtResourceHelper
from PyQt5.QtCore import Qt


class VideoControlWidget(QWidget):
    played = pyqtSignal(bool)
    seeked = pyqtSignal(int)
    containsCursor = pyqtSignal(bool)

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__initUi()

    def __initUi(self):
        self.__timer_lbl = QLabel()
        self.__cur_len_lbl = QLabel()

        self.__slider = VideoSlider()
        self.__slider.seeked.connect(self.seeked)
        self.__slider.updatePosition.connect(self.updatePosition)

        self.__timer_lbl.setText('00:00:00')
        self.__cur_len_lbl.setText('00:00:00')

        lay = QHBoxLayout()
        lay.addWidget(self.__timer_lbl)
        lay.addWidget(self.__slider)
        lay.addWidget(self.__cur_len_lbl)
        lay.setContentsMargins(0, 0, 0, 0)

        topWidget = QWidget()
        topWidget.setLayout(lay)

        self.__playBtn = QPushButton()
        self.__playBtn.setEnabled(False)

        self.__stopBtn = QPushButton()
        self.__stopBtn.setEnabled(False)

        btns = [self.__playBtn, self.__stopBtn]

        PyQtResourceHelper.setStyleSheet(btns, ['style/button.css'])
        PyQtResourceHelper.setIcon(btns, ['ico/play.png', 'ico/stop.png'])

        self.setStyleSheet('QLabel { color: white; }')

        self.__playBtn.clicked.connect(self.togglePlayback)
        self.__stopBtn.clicked.connect(self.stop)

        lay = QHBoxLayout()
        for btn in btns:
            lay.addWidget(btn)
        lay.setSpacing(0)
        lay.setContentsMargins(4, 0, 4, 0)

        btnWidget = QWidget()
        btnWidget.setLayout(lay)
        btnWidget.setStyleSheet('QWidget { '
                                'border: 1px solid #444; '
                                'padding: 5px; '
                                'border-radius: 5px; '
                                'background-color: #BBB;}'
                                )

        btnWidget.setMinimumWidth(btnWidget.sizeHint().width()*1.5)
        btnWidget.setMinimumHeight(btnWidget.sizeHint().height()*1.5)

        btnWidget.setMaximumWidth(btnWidget.sizeHint().width()*2.5)
        btnWidget.setMaximumHeight(btnWidget.sizeHint().height()*2.5)

        lay = QHBoxLayout()
        lay.setAlignment(Qt.AlignCenter)
        lay.addWidget(btnWidget)
        lay.setContentsMargins(0, 0, 0, 0)

        bottomWidget = QWidget()
        bottomWidget.setLayout(lay)

        lay = QVBoxLayout()
        lay.addWidget(topWidget)
        lay.addWidget(bottomWidget)
        lay.setSpacing(2)

        self.setLayout(lay)

    def __getMediaLengthHumanFriendly(self, filename):
        media = mp4.MP4(filename)
        media_length = media.info.length

        h = int(media_length / 3600)
        media_length -= (h * 3600)
        m = int(media_length / 60)
        media_length -= (m * 60)
        s = media_length
        song_length = '{:0>2d}:{:0>2d}:{:0>2d}'.format(int(h), int(m), int(s))

        return song_length

    def formatTime(self, millis):
        millis = int(millis)
        seconds = (millis / 1000) % 60
        seconds = round(seconds)
        minutes = (millis / (1000 * 60)) % 60
        minutes = int(minutes)
        hours = (millis / (1000 * 60 * 60)) % 24

        return "%02d:%02d:%02d" % (hours, minutes, seconds)

    def updatePosition(self, pos):
        self.__slider.setValue(pos)
        self.__timer_lbl.setText(self.formatTime(pos))

    def updateDuration(self, duration):
        self.__slider.setRange(0, duration)
        self.__slider.setEnabled(duration > 0)
        self.__slider.setPageStep(duration / 1000)

    def setPlayer(self, player: QMediaPlayer):
        self.__mediaPlayer = player
        self.__mediaPlayer.setNotifyInterval(1)
        self.__mediaPlayer.positionChanged.connect(self.updatePosition)
        self.__mediaPlayer.durationChanged.connect(self.updateDuration)

    def setMedia(self, filename):
        mediaContent = QMediaContent(QUrl.fromLocalFile(filename))  # it also can be used as playlist
        self.__mediaPlayer.setMedia(mediaContent)
        self.__playBtn.setEnabled(True)
        self.__cur_len_lbl.setText(self.__getMediaLengthHumanFriendly(filename))

    def play(self):
        PyQtResourceHelper.setIcon([self.__playBtn], ['ico/pause.png'])
        self.__mediaPlayer.play()
        self.played.emit(True)
        self.__stopBtn.setEnabled(True)

    def pause(self):
        PyQtResourceHelper.setIcon([self.__playBtn], ['ico/play.png'])
        self.__mediaPlayer.pause()

    def togglePlayback(self):
        if self.__mediaPlayer.mediaStatus() == QMediaPlayer.NoMedia:
            pass
        elif self.__mediaPlayer.state() == QMediaPlayer.PlayingState:
            self.pause()
        else:
            self.play()

    def stop(self):
        PyQtResourceHelper.setIcon([self.__playBtn], ['ico/play.png'])
        self.__mediaPlayer.stop()
        self.__stopBtn.setEnabled(False)
        self.played.emit(False)

    def enterEvent(self, e):
        self.containsCursor.emit(True)
        return super().enterEvent(e)

    def leaveEvent(self, e):
        self.containsCursor.emit(False)
        return super().leaveEvent(e)