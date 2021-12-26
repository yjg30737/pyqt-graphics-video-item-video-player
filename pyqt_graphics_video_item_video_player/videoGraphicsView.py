import os.path

from PyQt5.QtCore import pyqtSignal, QSizeF, Qt
from PyQt5.QtMultimediaWidgets import QGraphicsVideoItem
from PyQt5.QtWidgets import QGraphicsScene, QGraphicsView


class VideoGraphicsView(QGraphicsView):
    setMedia = pyqtSignal(str)

    def __init__(self,  *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.__filename = ''
        self.__item = ''
        self.__ext = ['.mp4']
        self.setAcceptDrops(True)
        self.__initUi()

    def __initUi(self):
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        self.setStyleSheet('QGraphicsView { background: #000; }')
        scene = QGraphicsScene()
        self.setScene(scene)

        self.__item = QGraphicsVideoItem()
        self.__item.setAcceptDrops(True)
        self.scene().addItem(self.__item)

        w_f = float(self.contentsRect().size().width())
        h_f = float(self.contentsRect().size().height())
        self.__item.setSize(QSizeF(w_f, h_f))

    def setFileName(self, filename):
        self.__filename = filename

    def getItem(self):
        return self.__item

    def initPlay(self):
        if self.__item:
            self.fitInView(self.__item, Qt.KeepAspectRatio)

    def dragEnterEvent(self, e):
        super().dragEnterEvent(e)
        if e.mimeData().hasUrls():
            filename = e.mimeData().urls()[0].toLocalFile()
            ext = os.path.splitext(filename)[-1]
            print(ext)
            if ext in self.__ext:
                e.accept()
                return
        e.ignore()

    def dragMoveEvent(self, e):
        super().dragMoveEvent(e)

    def dropEvent(self, e):
        super().dropEvent(e)
        filename = e.mimeData().urls()[0].toLocalFile()
        self.setMedia.emit(filename)

    def resizeEvent(self, e):
        self.initPlay()
        return super().resizeEvent(e)