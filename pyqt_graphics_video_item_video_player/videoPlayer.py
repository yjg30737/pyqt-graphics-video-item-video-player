from PyQt5.QtCore import QUrl, QTimer
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtWidgets import QWidget, QGridLayout

from pyqt_graphics_video_item_video_player.videoControlWidget import VideoControlWidget
from pyqt_graphics_video_item_video_player.videoGraphicsView import VideoGraphicsView


class VideoPlayer(QWidget):

    def __init__(self):
        super().__init__()
        self.__initUi()

    def __initUi(self):
        self.__mediaPlayer = QMediaPlayer()
        self.__view = VideoGraphicsView()
        self.__view.setMouseTracking(True)
        self.__view.setMedia.connect(self.setMedia)
        self.__view.mouseMoveEvent = self.mouseMoveEvent

        self.__mediaPlayer.setVideoOutput(self.__view.getItem())
        
        self.__hideShowInterval = 2000

        self.__videoControlWidget = VideoControlWidget()
        self.__videoControlWidget.setPlayer(self.__mediaPlayer)
        self.__videoControlWidget.played.connect(self.__initPlay)
        self.__videoControlWidget.seeked.connect(self.__seekPosition)
        self.__videoControlWidget.containsCursor.connect(self.__setRemainControlWidgetVisible)

        self.__videoControlWidget.setVisible(False)
        self.__videoControlWidget.setMaximumHeight(75)

        lay = QGridLayout()
        lay.addWidget(self.__view, 0, 0, 2, 1)
        lay.addWidget(self.__videoControlWidget, 1, 0, 1, 1)
        lay.setContentsMargins(0, 0, 0, 0)

        self.setLayout(lay)

        self.setMouseTracking(True)

        self.__timerInit()

    def setMedia(self, filename):
        mediaContent = QMediaContent(QUrl.fromLocalFile(filename))
        self.__mediaPlayer.setMedia(mediaContent)
        self.__videoControlWidget.setMedia(filename)

    def __timerInit(self):
        self.__timer = QTimer()
        self.__timer.setInterval(self.__hideShowInterval)
        self.__timer.timeout.connect(self.__bottomWidgetToggled)

    def __bottomWidgetToggled(self):
        self.__timer.stop()
        self.__videoControlWidget.setVisible(False)

    def __timerStart(self):
        self.__videoControlWidget.setVisible(True)
        self.__timer.start()

    def __seekPosition(self, pos):
        self.__mediaPlayer.setPosition(pos)

    def enterEvent(self, e):
        self.__timerStart()
        return super().enterEvent(e)

    def mouseMoveEvent(self, e):
        if self.__timer.isActive():
            self.__timer.setInterval(self.__hideShowInterval)
        else:
            self.__timerStart()
        return super().mouseMoveEvent(e)

    def leaveEvent(self, e):
        self.__videoControlWidget.setVisible(False)
        return super().leaveEvent(e)

    def __initPlay(self):
        self.__view.initPlay()

    def __setRemainControlWidgetVisible(self, f):
        if f:
            self.__timer.timeout.disconnect()
        else:
            self.__timer.timeout.connect(self.__bottomWidgetToggled)