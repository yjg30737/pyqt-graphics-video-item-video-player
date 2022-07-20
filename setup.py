from setuptools import setup, find_packages

setup(
    name='pyqt-graphics-video-item-video-player',
    version='0.0.1',
    author='Jung Gyu Yoon',
    author_email='yjg30737@gmail.com',
    license='MIT',
    packages=find_packages(),
    description='PyQt video player widget',
    package_data={'pyqt_graphics_video_item_video_player.style': ['button.css', 'slider.css'],
                  'pyqt_graphics_video_item_video_player.ico': ['pause.png', 'play.png', 'stop.png']},
    url='https://github.com/yjg30737/pyqt-graphics-video-item-video-player.git',
    install_requires=[
        'mutagen',
        'PyQt5>=5.8',
        'pyqt-resource-helper>=0.0.1'
    ]
)