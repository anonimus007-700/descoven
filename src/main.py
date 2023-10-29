import os
import sys
import math
import random
import threading

from PyQt5.QtWidgets import * 
from PyQt5.QtGui import * 
from PyQt5.QtCore import *
from PyQt5.QtMultimedia import QSoundEffect


class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__()
        self.acceptDrops()

        self.setWindowTitle("DESCOVEN")

        self.setGeometry(QDesktopWidget().availableGeometry())
        self.setMouseTracking(True)

        self.window_flags = Qt.FramelessWindowHint | Qt.WindowStaysOnTopHint

        self.setWindowFlags(self.window_flags)
        self.setAttribute(Qt.WA_TranslucentBackground)

        self.speed = 200
        self.folder_path = "res/images"
        self.is_left = False

        self.venom_black_stance = QMovie('res/venom/venom-blackstance.gif')
        self.venom_black_stance_left = QMovie('res/venom/venom-blackstance-left.gif')
        self.venom_black_walk = QMovie('res/venom/venom-blackwalk.gif')
        self.venom_black_walk_left = QMovie('res/venom/venom-blackwalk-left.gif')
        self.venom_hkrepeat = QMovie('res/venom/venom-hkrepeat.gif')
        
        self.cross = QPixmap('res/other/cross.png')

        self.venommm = QSoundEffect()
        self.venommm.setSource(QUrl.fromLocalFile("res/sound/venommm.wav"))
        self.your_world = QSoundEffect()
        self.your_world.setSource(QUrl.fromLocalFile("res/sound/your-world-is-not-so-ugly-after-all.wav"))

        self.UiComponents()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_player)
        self.timer.start(random.randint(2000, 5000))

        self.show_meme_timer = QTimer(self)
        self.show_meme_timer.timeout.connect(self.show_meme)
        self.show_meme_timer.start(random.randint(13000, 20000))

        self.show()
        # self.show_meme()

    def finish_walk(self):
        self.timer.start(random.randint(0, 6000))

        if self.is_left:
            self.venom_black_walk.stop()
            self.venom_black_stance_left.stop()
            self.player.setMovie(self.venom_black_stance_left)
            self.venom_black_stance_left.start()
        else:
            self.venom_black_walk_left.stop()
            self.venom_black_walk.stop()
            self.player.setMovie(self.venom_black_stance)
            self.venom_black_stance.start()
    
    def thread(func):
        def wrapper(*args, **kwargs):
            current_thread = threading.Thread(
                target=func, args=args, kwargs=kwargs)
            current_thread.start()
        return wrapper

    def UiComponents(self):
        self.meme_label = QLabel(self)
        self.player = QLabel(self)
        self.cross_but = QPushButton(self)
        
        self.cross_but.setStyleSheet("background-color: transparent; border: none;")
        
        self.opacity_effect_cross = QGraphicsOpacityEffect()
        self.cross_but.setGraphicsEffect(self.opacity_effect_cross)
        
        self.opacity_effect = QGraphicsOpacityEffect()
        self.meme_label.setGraphicsEffect(self.opacity_effect)
        
        self.venommm.setVolume(0.1)
        self.venommm.play()

        self.player.setMovie(self.venom_black_stance)
        self.player.setMinimumSize(QSize(250, 185))
        self.player.setMaximumSize(QSize(200, 200))

        self.venom_black_stance.start()

        self.showFullScreen()

    def move_player(self):
        self.timer.stop()

        new_x = random.randint(0, self.width())
        new_y = random.randint(0, self.height())
        
        distance = round(math.sqrt((new_x - self.player.x()) ** 2 + (new_y - self.player.y()) ** 2), 1)
        time = round(distance / self.speed, 0) * 1000

        self.animation = QPropertyAnimation(self.player, b"geometry")
        self.animation.setDuration(int(time))
        
        if self.player.x() >= new_x:
            self.venom_black_stance.stop()
            self.venom_black_stance_left.stop()
            self.player.setMovie(self.venom_black_walk_left)
            self.venom_black_walk_left.start()
            self.is_left = True
        else:
            self.venom_black_stance_left.stop()
            self.venom_black_stance.stop()
            self.player.setMovie(self.venom_black_walk)
            self.venom_black_walk.start()
            self.is_left = False

        start_rect = QRect(self.player.x(),
                           self.player.y(),
                           150, 120)
        end_rect = QRect(new_x,
                         new_y,
                         150, 120)

        self.animation.setStartValue(start_rect)
        self.animation.setEndValue(end_rect)
        
        self.animation.setEasingCurve(QEasingCurve.Linear)

        self.animation.start()

        self.animation.finished.connect(self.finish_walk)

    def show_meme(self):
        self.timer.stop()
        self.show_meme_timer.stop()
        self.venom_black_stance_left.stop()
        self.venom_black_stance.stop()
        self.venom_black_walk.stop()
        self.venom_black_walk_left.stop()

        try:
            self.animation.stop()
        except:
            pass

        self.player.setMovie(self.venom_hkrepeat)
        self.venom_hkrepeat.start()

        self.your_world.play()

        image_files = [file for file in os.listdir(self.folder_path)]

        random_image = random.choice(image_files)
        image_path = os.path.join(self.folder_path, random_image)

        meme = QPixmap(image_path)

        self.meme_label.setPixmap(meme)

        self.meme_label.setGeometry(random.randint(0, self.width()-meme.width()),
                                    random.randint(0, self.height()-meme.height()),
                                    meme.width(),
                                    meme.height())

        self.show_meme = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.show_meme.setStartValue(0)
        self.show_meme.setEndValue(1)
        self.show_meme.setDuration(3500)
        self.show_meme.start()
        self.meme_label.lower()
        
        self.layout().addWidget(self.meme_label)
        
        self.show_meme_stop = QTimer(self)
        self.show_meme_stop.timeout.connect(self.continue_show_meme)
        self.show_meme_stop.start(3700)
    
    def continue_show_meme(self):
        self.show_meme_stop.stop()
        self.venom_hkrepeat.stop()
        
        self.cross_but.setIcon(QIcon(self.cross))
        
        self.opacity_effect_cross.setOpacity(1)
        
        self.cross_but.resize(self.cross.width(),
                              self.cross.height())
        
        self.cross_but.move(self.meme_label.x(),
                            self.meme_label.y())
        
        self.cross_but.clicked.connect(self.cross_click)

        self.player.raise_()
        self.player.setMovie(self.venom_black_stance)
        self.venom_black_stance.start()
        
        self.timer.start(random.randint(2000, 5000))

    def cross_click(self):
        self.close_meme = QPropertyAnimation(self.opacity_effect, b'opacity')
        self.close_meme.setStartValue(1)
        self.close_meme.setEndValue(0)
        self.close_meme.setDuration(2000)

        self.close_meme_cross = QPropertyAnimation(self.opacity_effect_cross, b'opacity')
        self.close_meme_cross.setStartValue(1)
        self.close_meme_cross.setEndValue(0)
        self.close_meme_cross.setDuration(2000)
        
        self.group = QParallelAnimationGroup()
        self.group.addAnimation(self.close_meme)
        self.group.addAnimation(self.close_meme_cross)

        self.group.start()

        self.show_meme_timer.start(random.randint(10000, 20000))
        



App = QApplication(sys.argv)

window = Window()
sys.exit(App.exec())
