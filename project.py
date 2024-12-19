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
        self.key_timer = QTimer()  # Таймер для управления задержкой нажатия клавиш
        self.key_pressed = False  # Флаг для отслеживания нажатия клавиш

    def initUI(self):
        self.setWindowTitle('Змейка')
        self.setFixedSize(WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 40)

        self.timer = QBasicTimer()
        self.speed = 100  #cкорость игры

        self.snake = [(WIDTH // 2, HEIGHT // 2)]
        self.direction = Qt.Key_Right
        self.food = self.generate_food()
        self.score = 0
        self.game_over = False

        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignCenter)

        self.name_input = QLineEdit(self)
        self.name_input.setPlaceholderText("Введите ваше имя")
        self.start_button = QPushButton("Начать игру", self)
        self.start_button.clicked.connect(self.start_game)

        self.layout.addWidget(self.name_input)
        self.layout.addWidget(self.start_button)
        self.setLayout(self.layout)

    def start_game(self):
        self.name = self.name_input.text()
        if not self.name:
            QMessageBox.warning(self, 'Ошибка', 'Пожалуйста, введите имя!')
            return
        self.layout.itemAt(0).widget().hide()
        self.layout.itemAt(1).widget().hide()  # Скрываем кнопку и поле ввода имени (начало игры, чтобы не мешало)
        self.timer.start(self.speed, self)
        self.setFocus()  # Устанавливаем фокус на игровое окно (ради того чтобы после нажатия кнопки начала игры кнопки перемещения нажимались адекватно)
    
    def generate_food(self):
        while True: #спавн яблок и проверка на то что змеи нет на клетке
            position = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if position not in self.snake:
                return position

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
        else:
            super().timerEvent(event) #движение змеи

    def move_snake(self):
        head_x, head_y = self.snake[0]

        if self.direction == Qt.Key_Left:
            head_x -= 1
        elif self.direction == Qt.Key_Right:
            head_x += 1
        elif self.direction == Qt.Key_Up:
            head_y -= 1
        elif self.direction == Qt.Key_Down:
            head_y += 1

        # Проверка столкновений с границами
        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT:
            self.end_game()
            return

        new_head = (head_x, head_y)

        # Проверка столкновений с телом змеи
        if new_head in self.snake:
            self.end_game()
            return

        self.snake.insert(0, new_head)

        # Проверка поедания еды
        if new_head == self.food:
            self.score += 10
            self.food = self.generate_food()
        else:
            self.snake.pop()

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)

        # Рисуем игровое поле
        for x in range(WIDTH):
            for y in range(HEIGHT):
                rect = QRect(x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)
                painter.setPen(QColor('#00ff1a'))
                painter.setBrush(QColor('#038510'))
                painter.drawRect(rect)

        # Рисуем еду
        food_x, food_y = self.food
        painter.setBrush(QColor(255, 0, 0))
        painter.drawEllipse(food_x * CELL_SIZE, food_y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)

        # Рисуем змею
        for index, (x, y) in enumerate(self.snake):
            if index == 0:
                painter.setBrush(QColor('#0400ff'))  # Голова
            else:
                painter.setBrush(QColor('#07f'))
            painter.drawRect(x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)

        # Рисуем счет
        painter.setPen(QColor('#ff6a00'))
        painter.setFont(QFont('Arial', 16))
        painter.drawText(10, 30, f'Счет: {self.score}')

        def keyPressEvent(self, event):
            key = event.key()
            # Запрет на противоположное направление
            if self.key_timer.isActive():  # Проверяем, активен ли таймер
                return  # Если активен, игнорируем нажатие

            if key == Qt.Key_Left and self.direction != Qt.Key_Right:
                self.direction = Qt.Key_Left
            elif key == Qt.Key_Right and self.direction != Qt.Key_Left:
                self.direction = Qt.Key_Right
            elif key == Qt.Key_Up and self.direction != Qt.Key_Down:
                self.direction = Qt.Key_Up
            elif key == Qt.Key_Down and self.direction != Qt.Key_Up:
                self.direction = Qt.Key_Down

            self.key_timer.start(100)  # Запускаем таймер на 100 мс
            self.key_pressed = True  # Устанавливаем флаг нажатия клавиши

        def reset_key_press(self):
            self.key_timer.stop()  # Останавливаем таймер, когда время истекло
            self.key_pressed = False  # Сбрасываем флаг нажатия клавиши


