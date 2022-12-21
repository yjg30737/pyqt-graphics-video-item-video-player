from PyQt5.QtWidgets import QApplication
from pyqt_graphics_video_item_video_player.videoPlayer import VideoPlayer

if __name__ == "__main__":
    import sys, os

    app = QApplication(sys.argv)
    videoPlayer = VideoPlayer()
    videoPlayer.show()
    videoPlayer.setMedia(os.path.join(os.getcwd(), '71ic2e6e0c613.mp4'))
    app.exec_()