import sys
import random
import psycopg2
from PyQt5.QtWidgets import QApplication, QWidget, QMessageBox, QLineEdit, QVBoxLayout, QPushButton
from PyQt5.QtCore import Qt, QBasicTimer, QRect, QTimer
from PyQt5.QtGui import QPainter, QColor, QFont

# Размеры игрового поля
CELL_SIZE = 20
WIDTH = 20  # количество ячеек по горизонтали
HEIGHT = 20  # количество ячеек по вертикали

# Database connection
def create_connection():
    return psycopg2.connect(
        dbname="postgres",
        user="postgres",
        password="123",
        host="localhost"
    )

class SnakeGame(QWidget):
    def __init__(self):
        super().__init__()
        self.conn = create_connection()
        self.cursor = self.conn.cursor()
        self.postgres_insert_query = """INSERT INTO "zmeika" (player, score) VALUES (%s, %s)"""
        self.initUI()
        self.key_timer = QTimer()
        self.key_timer.timeout.connect(self.reset_key_press)
        self.key_pressed = False

    def initUI(self):
        self.setWindowTitle('Змейка')
        self.setFixedSize(WIDTH * CELL_SIZE, HEIGHT * CELL_SIZE + 40)
    
        self.timer = QBasicTimer()
        self.speed = 100 
    
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
        self.layout.itemAt(1).widget().hide()
        self.timer.start(self.speed, self)
        self.setFocus()

    def generate_food(self):
        while True:
            position = (random.randint(0, WIDTH - 1), random.randint(0, HEIGHT - 1))
            if position not in self.snake:
                return position

    def timerEvent(self, event):
        if event.timerId() == self.timer.timerId():
            self.move_snake()
        else:
            super().timerEvent(event)

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

        if head_x < 0 or head_x >= WIDTH or head_y < 0 or head_y >= HEIGHT or (head_x, head_y) in self.snake:
            self.end_game()
            return

        new_head = (head_x, head_y)
        self.snake.insert(0, new_head)

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
            painter.setBrush(QColor('#0400ff') if index == 0 else QColor('#07f'))
            painter.drawRect(x * CELL_SIZE, y * CELL_SIZE + 40, CELL_SIZE, CELL_SIZE)

        # Рисуем счет
        painter.setPen(QColor('#ff6a00'))
        painter.setFont(QFont('Arial', 16))
        painter.drawText(10, 30, f'Счет: {self.score}')

    def keyPressEvent(self, event):
        key = event.key()
        if self.key_timer.isActive():
            return

        if key in (Qt.Key_Left, Qt.Key_Right, Qt.Key_Up, Qt.Key_Down):
            if (key == Qt.Key_Left and self.direction != Qt.Key_Right) or \
               (key == Qt.Key_Right and self.direction != Qt.Key_Left) or \
               (key == Qt.Key_Up and self.direction != Qt.Key_Down) or \
               (key == Qt.Key_Down and self.direction != Qt.Key_Up):
                self.direction = key

        self.key_timer.start(100)

    def reset_key_press(self):
        self.key_timer.stop()

    def end_game(self):
        self.timer.stop()
        self.game_over = True
        self.save_score()
        QMessageBox.information(self, 'Игра окончена', f'Ваш счет: {self.score}')
        self.close()

    def save_score(self):
        record_to_insert = (self.name, self.score)
        self.cursor.execute(self.postgres_insert_query, record_to_insert)
        self.conn.commit()
        print("Score saved successfully!")

    def closeEvent(self, event):
        self.cursor.close()
        self.conn.close()
        event.accept()

def main():
    app = QApplication(sys.argv)
    game = SnakeGame()
    game.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    main()
