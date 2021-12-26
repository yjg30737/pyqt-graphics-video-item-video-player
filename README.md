# pyqt-graphics-video-item-video-player
Video(mp4 file only) player using QGraphicsVideoItem. Control widget at the bottom is shown/hidden followed by cursor's movement.

## Requirements
PyQt5 >= 5.8

## Setup
```pip3 install git+https://github.com/yjg30737/pyqt-graphics-video-item-video-player --upgrade```

## Included Packages
* <a href="https://github.com/yjg30737/pyqt-resource-helper.git">pyqt-resource-helper</a>

## Usage
This video player is mp4 only. 

You can set the video file by dropping it to the window. That is the only way.

## Example
### Code Sample
```python
from PyQt5.QtWidgets import QApplication
from pyqt_graphics_video_item_video_player.videoPlayer import VideoPlayer

if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    videoPlayer = VideoPlayer()
    videoPlayer.show()
    app.exec_()
```

### Result
Preview of interaction between cursor movement and control widget visibility

https://user-images.githubusercontent.com/55078043/147399452-891b9f8e-2a20-4724-8946-2e19526289c4.mp4

Preview of watching video with the pyqt-graphics-video-item-video-player and using control widget to navigate the video

https://user-images.githubusercontent.com/55078043/147399585-e251d5fd-6285-4dce-9922-75d0a230ceb3.mp4

## Note
QGraphicsVideoItem's quality is worse than QVideoWidget. Yeah.

You maybe wonder why did i make this in the first place.

Because for some reasons, I can't show the control widget (which has transparent background) over the QVideoWidget.

I'm still trying to figure out the way to solve this problem.

One more thing, There are some flaws in timer feature and button toggling. I will fix it.



