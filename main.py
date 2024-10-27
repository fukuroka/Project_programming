from symbol import pass_stmt

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget
from PyQt5.QtCore import Qt, QRect

import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("РосСтройТорг расчет")
        self.setFixedSize(700, 500)

        #тут будет регистрация/вход




        self.main_window() # не забудь перейти на главное окно


    def main_window(self):
        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        title = QLabel("РосСтройТорг расчет", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 22))
        title.setGeometry(QRect(0, 20, 700, 50))  # позиция и размер

        projects = QLabel("Проект комнаты 1\nПроект комнаты 2\nПроект комнаты 3\nПроект комнаты 4", self)
        projects.setFont(QFont("Arial", 14))
        projects.setAlignment(Qt.AlignCenter)
        projects.setGeometry(QRect(0, 150, 700, 100))

        create_project_button = QPushButton("Создать проект", self)
        create_project_button.setFixedSize(200, 50)
        create_project_button.setGeometry(QRect(250, 350, 200, 50))

        central_widget.setLayout(QtWidgets.QVBoxLayout())

    def input_room(self):
        pass

    def type_of_floor(self):
        pass

    def materials_floor(self):
        pass

    def type_of_wall(self):
        pass

    def materials_wall(self):
        pass

    def order(self):
        pass

def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    application()