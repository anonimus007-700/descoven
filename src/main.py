import sys
import random
import threading
import math

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
        self.is_left = False

        self.venom_black_stance = QMovie('res/venom-blackstance.gif')
        self.venom_black_stance_left = QMovie('res/venom-blackstance-left.gif')
        self.venom_black_walk = QMovie('res/venom-blackwalk.gif')
        self.venom_black_walk_left = QMovie('res/venom-blackwalk-left.gif')
        
        self.venommm = QSoundEffect()
        self.venommm.setSource(QUrl.fromLocalFile("res/music/venommm.wav"))

        self.UiComponents()

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_player)
        self.timer.start(random.randint(2000, 5000))

        self.show()

    def all_timer(self):
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.move_player)
        self.timer.start(random.randint(1200, 4000))
        
        self.sania_random_choice = random.choice([self.sania_ult_1, self.sania_ult_2])
        self.stas_random_choice = random.choice([self.stas_ult_1, self.stas_ult_2, self.stas_ult_3])
        self.misha_random_choice = random.choice([self.misha_ult_1, self.misha_ult_2])

        self.ult_timer = QTimer(self)
        if self.player_chose == 'sania':
            self.ult_timer.timeout.connect(self.sania_random_choice)
        elif self.player_chose == 'stas':
            self.ult_timer.timeout.connect(self.stas_random_choice)
        elif self.player_chose == 'misha':
            self.ult_timer.timeout.connect(self.misha_random_choice)
        elif self.player_chose == 'kolia':
            self.ult_timer.timeout.connect(self.kolia_ult_1)

        self.ult_timer.start(random.randint(8000, 25000))

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
        self.player = QLabel(self)
        
        self.venommm.setVolume(0.1)
        self.venommm.play()

        self.player.setMovie(self.venom_black_stance)
        self.player.setMinimumSize(QSize(150, 120))
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
            self.venom_black_walk_left.stop()
            self.player.setMovie(self.venom_black_walk_left)
            self.venom_black_walk_left.start()
            self.is_left = True
        else:
            self.venom_black_walk_left.stop()
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


App = QApplication(sys.argv)

window = Window()
sys.exit(App.exec())

