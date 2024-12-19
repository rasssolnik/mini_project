import sys
import random
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, QRect, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont

# Размеры игрового поля
CELL_SIZE = 20
WIDTH = 20  # количество ячеек по горизонтали
HEIGHT = 20  # количество ячеек по вертикали

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()

        self.initUI()
        self.key_timer.timeout.connect(self.reset_key_press)  # Подключаем метод сброса нажатия клавиш
        self.key_pressed = False  # Флаг для отслеживания нажатия клавиш

    def initUI(self):
        self.setWindowTitle('Змейка')
        self.setFixedSize(WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 40)

        self.timer = QBasicTimer()
        self.speed = 100  #cкорость игры

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Введите ваше имя")
        self.start_button = QPushButton("Начать игру", self)
        self.start_button.clicked.connect(self.start_game)

        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)
        #проверка
#
    

