import math
import sqlite3
import datetime

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QDialog, QLineEdit, \
    QHBoxLayout, QRadioButton
from PyQt5.QtCore import Qt, QRect
from PyQt5.QtGui import QDesktopServices
from PyQt5.QtCore import QUrl

import sys


class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("РосСтройТорг расчет")
        self.setFixedSize(700, 500)

        self.current_material_index = 0
        self.current_order_id = None  # ID текущего заказа
        self.project_name = ''
        self.current_user_id = 0
        self.previous_material_type_id = None

        self.login()

    def login(self):
        self.clear_window()

        self.login_widget = QWidget(self)
        self.setCentralWidget(self.login_widget)
        self.setFixedSize(700, 500)

        self.title_label = QLabel("Вход", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22))
        self.title_label.setGeometry(QRect(0, 0, 700, 50))  # позиция и размер

        self.login_label = QLabel("Логин", self)
        self.login_label.setFont(QFont("Arial", 12))
        self.login_label.setGeometry(QRect(210, 210, 200, 23))
        self.login_input = QLineEdit(self)
        self.login_input.setGeometry(QRect(260, 210, 200, 23))

        self.password_label = QLabel("Пароль", self)
        self.password_label.setFont(QFont("Arial", 12))
        self.password_input = QLineEdit(self)
        self.password_input.setEchoMode(QLineEdit.Password)
        self.password_label.setGeometry(QRect(200, 250, 200, 23))
        self.password_input.setGeometry(QRect(260, 250, 200, 23))

        self.register_button = QPushButton("Регистрация", self)
        self.register_button.setGeometry(QRect(360, 350, 100, 40))
        self.register_button.clicked.connect(lambda: self.create_account())
        self.login_button = QPushButton("Войти", self)
        self.login_button.setGeometry(QRect(250, 350, 100, 40))
        self.login_button.clicked.connect(lambda: self.login_function())

        main_layout = QVBoxLayout(self.login_widget)
        main_layout.addWidget(self.title_label)

        self.error_label = QLabel("", self)
        main_layout.addWidget(self.error_label)

    def login_function(self):
        user = self.login_input.text()
        password = self.password_input.text()

        if not user or not password:
            self.error_label.setText('Пожалуйста заполните все поля')
            return

        try:
            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT id_client,password FROM client WHERE email=?", (user,))
                result_pass = cur.fetchone()

            if result_pass and result_pass[1] == password:
                self.current_user_id = result_pass[0]  # Получаем ID пользователя
                self.main_window()
            else:
                self.error_label.setText('Введен неверный логин или пароль')
        except sqlite3.Error as e:
            self.error_label.setText(f"Ошибка базы данных: {e}")

    def create_account(self):
        self.clear_window()

        self.central_widget = QWidget(self)
        self.setCentralWidget(self.central_widget)

        self.setWindowTitle("Регистрация")
        self.setFixedSize(700, 500)

        self.title_label = QLabel("Регистрация", self)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22))
        self.title_label.setGeometry(QRect(250, 30, 200, 50))

        self.name_label = QLabel("Имя", self)
        self.name_label.setGeometry(QRect(220, 110, 100, 23))
        self.name_input = QLineEdit(self)
        self.name_input.setGeometry(QRect(250, 110, 200, 23))

        self.surname_label = QLabel("Фамилия", self)
        self.surname_label.setGeometry(QRect(195, 150, 100, 23))
        self.surname_input = QLineEdit(self)
        self.surname_input.setGeometry(QRect(250, 150, 200, 23))

        self.patronymic_label = QLabel("Отчество", self)
        self.patronymic_label.setGeometry(QRect(190, 190, 100, 23))
        self.patronymic_input = QLineEdit(self)
        self.patronymic_input.setGeometry(QRect(250, 190, 200, 23))

        self.phone_label = QLabel("Телефон", self)
        self.phone_label.setGeometry(QRect(195, 230, 100, 23))
        self.phone_input = QLineEdit(self)
        self.phone_input.setGeometry(QRect(250, 230, 200, 23))

        self.email_label = QLabel("Email", self)
        self.email_label.setGeometry(QRect(215, 270, 100, 23))
        self.email_input = QLineEdit(self)
        self.email_input.setGeometry(QRect(250, 270, 200, 23))

        self.password_label = QLabel("Пароль", self)
        self.password_label.setGeometry(QRect(205, 310, 100, 23))
        self.password_input = QLineEdit(self)
        self.password_input.setGeometry(QRect(250, 310, 200, 23))
        self.password_input.setEchoMode(QLineEdit.Password)

        self.confirm_password_label = QLabel("Повторите пароль", self)
        self.confirm_password_label.setGeometry(QRect(148, 350, 170, 23))  # Изменено QRect
        self.confirm_password_input = QLineEdit(self)
        self.confirm_password_input.setGeometry(QRect(250, 350, 200, 23))
        self.confirm_password_input.setEchoMode(QLineEdit.Password)

        self.register_button = QPushButton("Зарегистрироваться", self)
        self.register_button.setGeometry(QRect(250, 420, 200, 30))
        self.register_button.clicked.connect(lambda: self.create_acc_function())

        self.error_label = QLabel("", self)
        self.error_label.setAlignment(Qt.AlignCenter)
        self.error_label.setGeometry(QRect(250, 520, 200, 23))

        self.title_label.show()
        self.name_label.show()
        self.name_input.show()
        self.surname_label.show()
        self.surname_input.show()
        self.patronymic_label.show()
        self.patronymic_input.show()
        self.phone_label.show()
        self.phone_input.show()
        self.email_label.show()
        self.email_input.show()
        self.password_label.show()
        self.password_input.show()
        self.confirm_password_label.show()
        self.confirm_password_input.show()
        self.register_button.show()
        self.error_label.show()

    def create_acc_function(self):
        email = self.email_input.text()
        password = self.password_input.text()
        password2 = self.confirm_password_input.text()
        name = self.name_input.text()
        fam = self.surname_input.text()
        fathname = self.patronymic_input.text()
        number = self.phone_input.text()

        if len(email) == 0 or len(password) == 0 or len(password2) == 0 or len(name) == 0 or len(fam) == 0 or len(
                fathname) == 0 or len(number) == 0:
            self.error_label.setText('Пожалуйста заполните все поля')
        elif password == password2:
            try:
                with sqlite3.connect('database.db') as conn:
                    cur = conn.cursor()
                    user_info = (name, fam, fathname, email, number, password)
                    cur.execute(
                        'INSERT INTO client (name, surname, patronymic, email, phone_number, password) VALUES (?, ?, ?, ?, ?, ?)',
                        user_info)
                    conn.commit()
                    self.current_user_id = cur.lastrowid

                self.main_window()
            except sqlite3.Error as e:
                self.error_label.setText(f'Ошибка базы данных: {e}')
        else:
            self.error_label.setText('Пароли не совпадают')

    def main_window(self):
        self.clear_window()

        self.main_window_widget = QWidget(self)
        self.setCentralWidget(self.main_window_widget)

        title = QLabel("РосСтройТорг расчет", self.main_window_widget)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 22))
        title.setGeometry(QRect(0, 20, 700, 50))  # позиция и размер

        projects_layout = QVBoxLayout()  # Создаем вертикальный layout для кнопок проектов
        projects = self.load_projects_from_db()  # Загружаем проекты из базы данных
        if projects:
            for project in projects:
                project_button = QPushButton(project[0], self.main_window_widget)
                project_button.clicked.connect(lambda checked, p=project[0]: self.open_order_for_project(p))
                projects_layout.addWidget(project_button)
        else:
            projects_layout.addWidget(QLabel("У вас пока нет проектов", self.main_window_widget))

        projects_widget = QWidget(self.main_window_widget)  # Создаем виджет для layout'а
        projects_widget.setLayout(projects_layout)
        projects_widget.setGeometry(QRect(250, 150, 200, 200))  # Устанавливаем позицию и размер

        create_project_button = QPushButton("Создать проект", self.main_window_widget)
        create_project_button.clicked.connect(self.create_project)
        create_project_button.setFixedSize(200, 50)
        create_project_button.setGeometry(QRect(250, 350, 200, 50))

        self.main_window_widget.show()

    def load_projects_from_db(self):
        with sqlite3.connect("database.db") as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT title FROM room_project WHERE id_client=?", (self.current_user_id,))
            projects = cursor.fetchall()

        return projects

    def open_order_for_project(self, project_name):
        self.project_name = project_name  # Сохраняем название проекта
        self.order()  # Открываем окно заказа для выбранного проекта

    def create_project(self):
        dialog = QDialog(self)
        dialog.setWindowTitle("Создание проекта")

        label = QLabel("Название проекта:", dialog)
        input_field = QLineEdit(dialog)
        button_create = QPushButton("Создать", dialog)

        layout = QVBoxLayout(dialog)
        layout.addWidget(label)
        layout.addWidget(input_field)

        button_layout = QHBoxLayout()
        button_layout.addStretch(1)
        button_layout.addWidget(button_create)
        layout.addLayout(button_layout)

        button_create.clicked.connect(lambda: self.save_project_name(input_field.text(), dialog))

        dialog.exec_()

    def save_project_name(self, project_name, dialog):
        if project_name:
            try:
                with sqlite3.connect("database.db") as conn:
                    cursor = conn.cursor()
                    cursor.execute(
                        "INSERT INTO room_project (id_client, length, width, height, title) VALUES (?, ?, ?, ?, ?)",
                        (self.current_user_id, 0, 0, 0, project_name)
                    )
                    conn.commit()
                    self.project_name = project_name
                    print(f"Название проекта '{project_name}' сохранено в базе данных.")
                    self.input_room()

            except Exception as e:
                print(f"Ошибка при сохранении проекта: {e}")
        else:
            print("Название проекта не может быть пустым.")

    def input_room(self):

        self.clear_window()
        self.input_widget = QWidget(self)
        self.setCentralWidget(self.input_widget)

        self.setFixedSize(700, 500)

        self.title_label = QLabel("Введите параметры помещения", self.input_widget)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22))
        self.title_label.move(130, 20)

        self.title_label = QLabel("*вводите десятичные числа через точку(пример: 10.5; 3.0)", self.input_widget)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 11))
        self.title_label.move(160, 70)

        self.length_label = QLabel("Длина (м)", self.input_widget)
        self.length_label.setGeometry(QRect(195, 160, 100, 23))
        self.length_input = QLineEdit(self.input_widget)
        self.length_input.setGeometry(QRect(250, 160, 200, 23))

        self.width_label = QLabel("Ширина (м)", self.input_widget)
        self.width_label.setGeometry(QRect(187, 210, 100, 23))
        self.width_input = QLineEdit(self.input_widget)
        self.width_input.setGeometry(QRect(250, 210, 200, 23))

        self.height_label = QLabel("Высота (м)", self.input_widget)
        self.height_label.setGeometry(QRect(190, 260, 100, 23))
        self.height_input = QLineEdit(self.input_widget)
        self.height_input.setGeometry(QRect(250, 260, 200, 23))

        back_button = QPushButton("Назад", self.input_widget)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 420)
        back_button.clicked.connect(self.main_window)

        next_button = QPushButton("Далее", self.input_widget)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 420)
        next_button.clicked.connect(self.save_parameters_room)

        self.input_widget.show()

    def save_parameters_room(self):
        try:
            length = float(self.length_input.text())
            width = float(self.width_input.text())
            height = float(self.height_input.text())

            if length <= 0 or width <= 0 or height <= 0:
                self.error_label.setText('Пожалуйста, введите положительные числа')
                return
            '''if isinstance(length,int) or isinstance(width,int) or isinstance(height,int):
                self.error_label.setText('Пожалуйста, введите числа через точку, в т.ч. и целые!')
                return'''

            with sqlite3.connect('database.db') as conn:
                cur = conn.cursor()
                cur.execute("SELECT id_project FROM room_project WHERE title = ?", (self.project_name,))
                id_project = cur.fetchone()[0]
                room_info = (length, width, height, id_project)
                cur.execute(
                    'UPDATE room_project SET length=?, width=?, height=? WHERE id_project=?',
                    room_info
                )
                conn.commit()

            self.type_of_floor()

        except ValueError:
            self.error_label.setText('Пожалуйста, введите корректные числовые значения')
        except sqlite3.Error as e:
            self.error_label.setText(f'Ошибка базы данных: {e}')

    def type_of_floor(self):
        self.clear_window()

        self.floor_type_window = QWidget(self)
        self.setCentralWidget(self.floor_type_window)
        self.floor_type_window.setFixedSize(700, 500)

        font = QFont("Arial", 16)

        self.title_label = QLabel("Выберите вид материала для пола", self.floor_type_window)
        self.title_label.setGeometry(0, 20, 700, 50)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22))

        self.radio_button1 = QRadioButton("Ламинат", self.floor_type_window)
        self.radio_button1.setFont(font)
        self.radio_button1.setChecked(True)
        self.radio_button1.move(50, 170)

        self.radio_button2 = QRadioButton("Паркет", self.floor_type_window)
        self.radio_button2.setFont(font)
        self.radio_button2.move(50, 220)

        self.radio_button3 = QRadioButton("Плитка для пола", self.floor_type_window)
        self.radio_button3.setFont(font)
        self.radio_button3.move(50, 270)

        back_button = QPushButton("Назад", self.floor_type_window)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 420)

        next_button = QPushButton("Далее", self.floor_type_window)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 420)
        next_button.clicked.connect(self.on_next_button_clicked)

        self.floor_type_window.show()

    def on_next_button_clicked(self):
        if self.radio_button1.isChecked():
            type_material_name = "Ламинат"
        elif self.radio_button2.isChecked():
            type_material_name = "Паркет"
        elif self.radio_button3.isChecked():
            type_material_name = "Плитка для пола"
        else:
            type_material_name = ""

        type_material_id = self.get_type_material_id_by_name(type_material_name)

        if type_material_id:
            self.materials_floor(type_material_id, 'floor')
        else:
            print(f"Ошибка: тип материала '{type_material_name}' не найден в базе данных.")

    def get_type_material_id_by_name(self, type_material_name):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id_type FROM types_material WHERE name_type = ?", (type_material_name,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    # очищение окна
    def clear_window(self):
        for widget in self.children():
            if isinstance(widget, QWidget) and widget != self.centralWidget():
                widget.deleteLater()

    def materials_floor(self, type_material_id, source):

        '''type_material_name = self.get_type_material_name(type_material_id)

        title = QLabel(f"{type_material_name} в наличии", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))
        title.setGeometry(QRect(0, 20, 700, 40))

        self.block1_layout = QVBoxLayout()
        self.block1_label = QLabel(self)
        self.block1_label.setAlignment(Qt.AlignCenter)
        self.block1_photo = QLabel(self)
        self.block1_photo.setAlignment(Qt.AlignCenter)
        self.block1_button_add = QPushButton("Добавить",self)
        self.block1_button_add.clicked.connect(lambda: self.add_material_to_order(0))
        self.block1_button_add.setStyleSheet("min-height: 30px;")
        self.block1_layout.addWidget(self.block1_label)
        self.block1_layout.addWidget(self.block1_photo)
        self.block1_layout.addStretch(1)
        self.block1_layout.addWidget(self.block1_button_add)
        self.block1_widget = QWidget(self)
        self.block1_widget.setLayout(self.block1_layout)
        self.block1_widget.move(60, 70)
        self.block1_widget.setFixedSize(250, 300)
        self.block1_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")


        self.block2_layout = QVBoxLayout()
        self.block2_label = QLabel(self)
        self.block2_label.setAlignment(Qt.AlignCenter)
        self.block2_photo = QLabel(self)
        self.block2_button_add = QPushButton("Добавить",self)
        self.block2_button_add.clicked.connect(lambda: self.add_material_to_order(1))
        self.block2_button_add.setStyleSheet("min-height: 30px;")
        self.block2_photo.setAlignment(Qt.AlignCenter)
        self.block2_layout.addWidget(self.block2_label)
        self.block2_layout.addWidget(self.block2_photo)
        self.block2_layout.addStretch(1)
        self.block2_layout.addWidget(self.block2_button_add)
        self.block2_widget = QWidget(self)
        self.block2_widget.setLayout(self.block2_layout)
        self.block2_widget.move(400, 70)
        self.block2_widget.setFixedSize(250, 300)
        self.block2_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")

        prev_button_arrow = QPushButton("<-", self)
        prev_button_arrow.setFixedSize(45, 20)
        prev_button_arrow.move(50, 415)
        prev_button_arrow.clicked.connect(self.show_previous_material)

        next_button_arrow = QPushButton("->", self)
        next_button_arrow.setFixedSize(45, 20)
        next_button_arrow.move(100, 415)
        next_button_arrow.clicked.connect(self.show_next_material)

        back_button = QPushButton("Назад", self)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 400)

        next_button = QPushButton("Далее", self)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 400)

        self.current_material_index = 0
        self.materials = self.load_materials_from_db(type_material_id)
        self.update_material_blocks()  # Обновляем оба блока'''

        self.clear_window()

        type_material_name = self.get_type_material_name(type_material_id)
        self.previous_material_type_id = type_material_id

        self.materials_window = QWidget(self)
        self.materials_window.setWindowTitle("Материалы")
        self.setCentralWidget(self.materials_window)
        self.materials_window.setFixedSize(700, 500)

        title = QLabel(f"{type_material_name} в наличии", self.materials_window)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))
        title.setGeometry(QRect(0, 20, 700, 40))

        self.block1_widget = QWidget(self.materials_window)
        self.block1_widget.setGeometry(QRect(50, 70, 600, 150))
        self.block1_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.block1_layout = QHBoxLayout(self.block1_widget)

        self.block1_photo = QLabel(self.block1_widget)
        self.block1_photo.setFixedSize(230, 130)
        self.block1_photo.setStyleSheet("border: 1px solid black;")
        pixmap1 = QPixmap()
        pixmap1 = pixmap1.scaled(self.block1_photo.size(), Qt.KeepAspectRatio)
        self.block1_photo.setPixmap(pixmap1)
        self.block1_photo.setAlignment(Qt.AlignCenter)

        self.block1_label = QLabel(self.block1_widget)
        self.block1_label.setAlignment(Qt.AlignLeft)
        self.block1_label.setFixedWidth(230)
        self.block1_label.setWordWrap(True)

        self.block1_button_add = QPushButton("Добавить", self.block1_widget)
        self.block1_button_add.clicked.connect(lambda: self.add_material_to_order(0))
        self.block1_button_add.setFixedSize(80, 30)

        self.block1_layout.addWidget(self.block1_photo)
        self.block1_layout.addSpacing(20)
        self.block1_layout.addWidget(self.block1_label)
        self.block1_layout.addStretch(1)
        self.block1_layout.addWidget(self.block1_button_add)

        self.block2_widget = QWidget(self.materials_window)
        self.block2_widget.setGeometry(QRect(50, 250, 600, 150))
        self.block2_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.block2_layout = QHBoxLayout(self.block2_widget)

        self.block2_photo = QLabel(self.block2_widget)
        self.block2_photo.setFixedSize(230, 130)
        self.block2_photo.setStyleSheet("border: 1px solid black;")
        pixmap2 = QPixmap()
        pixmap2 = pixmap2.scaled(self.block2_photo.size(), Qt.KeepAspectRatio)
        self.block2_photo.setPixmap(pixmap2)
        self.block2_photo.setAlignment(Qt.AlignCenter)

        self.block2_label = QLabel(self.block2_widget)
        self.block2_label.setAlignment(Qt.AlignLeft)
        self.block2_label.setFixedWidth(230)
        self.block2_label.setWordWrap(True)

        self.block2_button_add = QPushButton("Добавить", self.block2_widget)
        self.block2_button_add.clicked.connect(lambda: self.add_material_to_order(1))
        self.block2_button_add.setFixedSize(80, 30)

        self.block2_layout.addWidget(self.block2_photo)
        self.block2_layout.addSpacing(20)
        self.block2_layout.addWidget(self.block2_label)
        self.block2_layout.addStretch(1)
        self.block2_layout.addWidget(self.block2_button_add)

        prev_button_arrow = QPushButton("<-", self.materials_window)
        prev_button_arrow.setFixedSize(45, 20)
        prev_button_arrow.move(50, 430)
        prev_button_arrow.clicked.connect(self.show_previous_material)

        next_button_arrow = QPushButton("->", self.materials_window)
        next_button_arrow.setFixedSize(45, 20)
        next_button_arrow.move(100, 430)
        next_button_arrow.clicked.connect(self.show_next_material)

        back_button = QPushButton("Назад", self.materials_window)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 420)
        if source == 'floor':
            back_button.clicked.connect(self.type_of_floor)  # Возвращаемся к type_of_floor
        elif source == 'wall':
            back_button.clicked.connect(self.type_of_wall)  # Возвращаемся к type_of_wall

        next_button = QPushButton("Далее", self.materials_window)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 420)
        if source == 'floor':
            next_button.clicked.connect(self.type_of_wall)  # Ведем к type_of_wall
        elif source == 'wall':
            next_button.clicked.connect(self.order)  # Ведем к order

        self.current_material_index = 0
        self.materials = self.load_materials_from_db(type_material_id)
        self.update_material_blocks()  # Обновляем оба блока
        self.materials_window.show()

    def add_material_to_order(self, block_index):
        # material_index = self.current_material_index + block_index
        start_index = self.current_material_index
        material_index = start_index + block_index

        if 0 <= material_index < len(self.materials):
            material = self.materials[material_index]
            material_name = material[0]
            material_id = self.get_material_id(material_name)
            try:
                material_id = self.get_material_id(material_name)
                if material_id:
                    # Создаем новый заказ, если его еще нет
                    if not self.current_order_id:
                        self.create_new_order()

                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()

                    #  Добавляем материал
                    cursor.execute(
                        "INSERT INTO order_item (id_order, id_material, quantity) VALUES (?, ?, ?)",
                        (self.current_order_id, material_id, 1)
                    )
                    conn.commit()
                    conn.close()

                    print(f"Материал '{material_name}' добавлен в заказ.")

                    self.update_order_quantities_and_cost()  # <-- Вызывать после добавления материала
                    self.update_order_items()
                else:
                    print(f"Ошибка: материал '{material_name}' не найден в базе данных.")
            except Exception as e:
                print(f"Ошибка при добавлении материала в заказ: {e}")
        else:
            print(
                f"Материал не найден. block_index: {block_index}, current_material_index: {self.current_material_index}, material_index: {material_index}, len(self.materials): {len(self.materials)}")

    '''def add_material_to_order(self, block_index):
        material_index = self.current_material_index + block_index
        if 0 <= material_index < len(self.materials):
            material_name = self.materials[material_index][0]  # Берем название материала

            try:
                material_id = self.get_material_id(material_name)
                if material_id:
                    # Создаем новый заказ, если его еще нет
                    if not self.current_order_id:
                        self.create_new_order()

                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()

                    cursor.execute(
                        "INSERT INTO order_item (id_order, id_material, quantity) VALUES (?, ?, ?)",
                        (self.current_order_id, material_id, 1)
                    )
                    conn.commit()
                    conn.close()

                    print(
                        f"Материал '{material_name}' (id: {material_id}) добавлен в заказ (id_order: {self.current_order_id}).")
                    self.update_order_items()
                else:
                    print(f"Ошибка: материал '{material_name}' не найден в базе данных.")
            except Exception as e:
                print(f"Ошибка при добавлении материала в заказ: {e}")
        else:
            print("Материал не найден.")'''

    def create_new_order(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Получаем id_project из текущего проекта
        cursor.execute("SELECT id_project FROM room_project WHERE title = ?", (self.project_name,))
        id_project = cursor.fetchone()[0]

        # Создаем новый заказ
        cursor.execute(
            "INSERT INTO `order` (id_project, status, amount, order_date) VALUES (?, 'Новый', 0, ?)",
            (id_project, datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
        )
        conn.commit()
        self.current_order_id = cursor.lastrowid  # Получаем ID последней записи

        conn.close()

        print(f"Создан новый заказ (id_order: {self.current_order_id}).")

    def get_material_id(self, material_name):

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT id_material FROM material WHERE name=?", (material_name,))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def get_type_material_name(self, type_material_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        query = "SELECT name_type FROM types_material WHERE id_type = ?"
        cursor.execute(query, (type_material_id,))
        result = cursor.fetchone()
        conn.close()

        if result:
            return result[0]
        else:
            return "Неизвестный тип"

    def load_materials_from_db(self, type_material_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        query = f"""
                    SELECT 
                        m.name, m.producer, m.length, m.width, m.price, m.count_pack, m.photo  -- Выбираем length и width
                    FROM 
                        material AS m
                    JOIN 
                        types_material AS t ON m.id_type = t.id_type
                    WHERE 
                        t.id_type = ?
                """
        cursor.execute(query, (type_material_id,))
        materials = cursor.fetchall()
        conn.close()
        return materials

    # обновляет записи в обоих блоках
    '''def update_material_blocks(self):
        for i, (label, photo_label) in enumerate(
                [(self.block1_label, self.block1_photo), (self.block2_label, self.block2_photo)]
        ):
            material_index = self.current_material_index + i
            if len(self.materials) > material_index:
                self.show_material_in_block(label, photo_label, material_index)
            else:
                self.clear_block(label, photo_label)'''

    def update_material_blocks(self, show_order_info=False):  # <---  Добавлен аргумент show_order_info
        for i, (label, photo_label) in enumerate(
                [(self.block1_label, self.block1_photo), (self.block2_label, self.block2_photo)]
        ):
            material_index = self.current_material_index + i
            if material_index < len(self.materials):
                material = self.materials[material_index]
                if show_order_info:
                    self.show_material_info_for_order(label, photo_label, material)  # <--- Передаем show_order_info
                else:
                    self.show_material_info_for_selection(label, photo_label, material)
            else:
                self.clear_block(label, photo_label)

    def show_material_in_block(self, label, photo_label, material_index):
        material = self.materials[material_index]
        name, producer, length, width, price, count, photo_path = material

        text = f"""
                      Название: {name}
                      Производитель: {producer}
                      Размеры: {length}x{width} см
                      Цена: {price} руб.
                      Количество в упаковке: {count}
                  """
        label.setText(text)

        pixmap = QPixmap(photo_path)
        pixmap = pixmap.scaled(230, 280, Qt.KeepAspectRatio)
        photo_label.setPixmap(pixmap)

    def clear_block(self, label, photo_label):
        label.setText("Материалы не найдены")
        photo_label.clear()

    def show_next_material(self):
        if len(self.materials) > self.current_material_index + 2:
            self.current_material_index += 2
            self.update_material_blocks()

    def show_previous_material(self):
        if self.current_material_index > 0:
            self.current_material_index -= 2
            self.update_material_blocks()

    def type_of_wall(self):

        self.clear_window()
        self.wall_type_window = QWidget(self)
        self.setCentralWidget(self.wall_type_window)
        self.wall_type_window.setFixedSize(700, 500)

        font = QFont("Arial", 16)

        self.title_label = QLabel("Выберите вид материала для стен", self.wall_type_window)
        self.title_label.setGeometry(0, 20, 700, 50)
        self.title_label.setAlignment(Qt.AlignCenter)
        self.title_label.setFont(QFont("Arial", 22))

        self.radio_button1 = QRadioButton("Обои", self.wall_type_window)
        self.radio_button1.setFont(font)
        self.radio_button1.setChecked(True)
        self.radio_button1.move(50, 170)

        self.radio_button2 = QRadioButton("Мозаика", self.wall_type_window)
        self.radio_button2.setFont(font)
        self.radio_button2.move(50, 220)

        self.radio_button3 = QRadioButton("Плитка для стен", self.wall_type_window)
        self.radio_button3.setFont(font)
        self.radio_button3.move(50, 270)

        back_button = QPushButton("Назад", self.wall_type_window)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 420)

        next_button = QPushButton("Далее", self.wall_type_window)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 420)
        next_button.clicked.connect(self.on_next_button_clicked_wall)  # Подключаем обработчик

        self.wall_type_window.show()

    def on_next_button_clicked_wall(self):
        if self.radio_button1.isChecked():
            type_material_name = "Обои"
        elif self.radio_button2.isChecked():
            type_material_name = "Мозаика"
        elif self.radio_button3.isChecked():
            type_material_name = "Плитка для стен"
        else:
            type_material_name = ""  # Или какое-то значение по умолчанию

        type_material_id = self.get_type_material_id_by_name(type_material_name)

        if type_material_id:
            self.materials_floor(type_material_id, 'wall')
        else:
            print(f"Ошибка: тип материала '{type_material_name}' не найден в базе данных.")

    '''def order(self):
        self.clear_window()

        self.current_order_id = self.get_current_order_id()  # ID последнего созданного заказа
        self.order_window = QWidget(self)
        self.setCentralWidget(self.order_window)
        self.order_window.setFixedSize(700, 500)

        title = QLabel("Список материалов", self.order_window)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))
        title.setGeometry(QRect(0, 20, 700, 40))

        # --- Блок 1 ---
        self.block1_widget = QWidget(self.order_window)
        self.block1_widget.setGeometry(QRect(50, 70, 600, 150))
        self.block1_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.block1_layout = QHBoxLayout(self.block1_widget)

        self.block1_photo = QLabel(self.block1_widget)
        self.block1_photo.setFixedSize(230, 130)
        self.block1_photo.setStyleSheet("border: 1px solid black;")
        self.block1_photo.setAlignment(Qt.AlignCenter)

        self.block1_label = QLabel(self.block1_widget)
        self.block1_label.setAlignment(Qt.AlignLeft)
        self.block1_label.setFixedWidth(230)
        self.block1_label.setWordWrap(True)

        self.block1_button_delete = QPushButton("Удалить", self.block1_widget)
        self.block1_button_delete.clicked.connect(lambda: self.delete_material_from_order(0))
        self.block1_button_delete.setFixedSize(80, 30)

        self.block1_layout.addWidget(self.block1_photo)
        self.block1_layout.addSpacing(20)
        self.block1_layout.addWidget(self.block1_label)
        self.block1_layout.addStretch(1)
        self.block1_layout.addWidget(self.block1_button_delete)

        # --- Блок 2 ---
        self.block2_widget = QWidget(self.order_window)
        self.block2_widget.setGeometry(QRect(50, 250, 600, 150))
        self.block2_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.block2_layout = QHBoxLayout(self.block2_widget)

        self.block2_photo = QLabel(self.block2_widget)
        self.block2_photo.setFixedSize(230, 130)
        self.block2_photo.setStyleSheet("border: 1px solid black;")
        self.block2_photo.setAlignment(Qt.AlignCenter)

        self.block2_label = QLabel(self.block2_widget)
        self.block2_label.setAlignment(Qt.AlignLeft)
        self.block2_label.setFixedWidth(230)
        self.block2_label.setWordWrap(True)

        self.block2_button_delete = QPushButton("Удалить", self.block2_widget)
        self.block2_button_delete.clicked.connect(lambda: self.delete_material_from_order(1))
        self.block2_button_delete.setFixedSize(80, 30)

        self.block2_layout.addWidget(self.block2_photo)
        self.block2_layout.addSpacing(20)
        self.block2_layout.addWidget(self.block2_label)
        self.block2_layout.addStretch(1)
        self.block2_layout.addWidget(self.block2_button_delete)

        prev_button_arrow = QPushButton("<-", self.order_window)
        prev_button_arrow.setFixedSize(45, 20)
        prev_button_arrow.move(50, 430)
        prev_button_arrow.clicked.connect(self.show_previous_material)

        next_button_arrow = QPushButton("->", self.order_window)
        next_button_arrow.setFixedSize(45, 20)
        next_button_arrow.move(100, 430)
        next_button_arrow.clicked.connect(self.show_next_material)

        back_button = QPushButton("Назад", self.order_window)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 420)

        next_button = QPushButton("Заказать", self.order_window)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 420)

        self.order_id_for_display = self.current_order_id  # ID заказа для отображения материалов
        self.materials = self.load_order_items_from_db(self.order_id_for_display)
        self.update_material_blocks()

        self.order_window.show()'''

    def order(self):
        self.clear_window()
        self.current_material_index = 0

        self.order_window = QWidget(self)
        self.setCentralWidget(self.order_window)
        self.order_window.setFixedSize(700, 500)

        title = QLabel("Список материалов", self.order_window)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 16))
        title.setGeometry(QRect(0, 10, 700, 40))

        # --- Блок 1 ---
        self.block1_widget = QWidget(self.order_window)
        self.block1_widget.setGeometry(QRect(50, 45, 600, 190))
        self.block1_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.block1_layout = QHBoxLayout(self.block1_widget)

        self.block1_photo = QLabel(self.block1_widget)
        self.block1_photo.setFixedSize(230, 170)
        self.block1_photo.setStyleSheet("border: 1px solid black;")
        self.block1_photo.setAlignment(Qt.AlignCenter)

        self.block1_label = QLabel(self.block1_widget)
        self.block1_label.setAlignment(Qt.AlignLeft)
        self.block1_label.setFixedWidth(240)
        self.block1_label.setWordWrap(True)

        self.block1_button_delete = QPushButton("Удалить", self.block1_widget)
        self.block1_button_delete.clicked.connect(lambda: self.delete_material_from_order(0))
        self.block1_button_delete.setFixedSize(80, 30)

        self.block1_layout.addWidget(self.block1_photo)
        self.block1_layout.addSpacing(20)
        self.block1_layout.addWidget(self.block1_label)
        self.block1_layout.addStretch(1)
        self.block1_layout.addWidget(self.block1_button_delete)

        # --- Блок 2 ---
        self.block2_widget = QWidget(self.order_window)
        self.block2_widget.setGeometry(QRect(50, 250, 600, 190))
        self.block2_widget.setStyleSheet("border: 1px solid black; border-radius: 10px;")
        self.block2_layout = QHBoxLayout(self.block2_widget)

        self.block2_photo = QLabel(self.block2_widget)
        self.block2_photo.setFixedSize(230, 170)
        self.block2_photo.setStyleSheet("border: 1px solid black;")
        self.block2_photo.setAlignment(Qt.AlignCenter)

        self.block2_label = QLabel(self.block2_widget)
        self.block2_label.setAlignment(Qt.AlignLeft)
        self.block2_label.setFixedWidth(240)
        self.block2_label.setWordWrap(True)

        self.block2_button_delete = QPushButton("Удалить", self.block2_widget)
        self.block2_button_delete.clicked.connect(lambda: self.delete_material_from_order(1))
        self.block2_button_delete.setFixedSize(80, 30)

        self.block2_layout.addWidget(self.block2_photo)
        self.block2_layout.addSpacing(20)
        self.block2_layout.addWidget(self.block2_label)
        self.block2_layout.addStretch(1)
        self.block2_layout.addWidget(self.block2_button_delete)

        prev_button_arrow = QPushButton("<-", self.order_window)
        prev_button_arrow.setFixedSize(45, 20)
        prev_button_arrow.move(50, 470)
        prev_button_arrow.clicked.connect(self.show_previous_material)

        next_button_arrow = QPushButton("->", self.order_window)
        next_button_arrow.setFixedSize(45, 20)
        next_button_arrow.move(100, 470)
        next_button_arrow.clicked.connect(self.show_next_material)

        back_button = QPushButton("Назад", self.order_window)
        back_button.setFixedSize(90, 40)
        back_button.move(480, 455)
        back_button.clicked.connect(
            lambda: self.materials_floor(type_material_id=self.previous_material_type_id, source='wall'))

        next_button = QPushButton("Заказать", self.order_window)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 455)

        base_url = "http://127.0.0.1:8000/site/order_summary/"
        query = f"user_id={self.current_user_id}&project_name={self.project_name}&order_id={self.current_order_id}"
        full_url = f"{base_url}?{query}"

        next_button.clicked.connect(lambda: QDesktopServices.openUrl(QUrl(full_url)))

        self.total_cost_label = QLabel("Общая стоимость заказа: ", self.order_window)
        self.total_cost_label.setGeometry(QRect(150, 470, 300, 20))

        self.current_order_id = self.get_order_id_for_user_and_project()
        if self.current_order_id:
            self.materials = self.load_order_items_from_db(self.current_order_id)
            self.update_order_quantities_and_cost()
            self.update_material_blocks(show_order_info=True)
        else:
            # Обработка случая, когда заказ не найден
            print("Заказ не найден для текущего пользователя и проекта.")

        self.order_window.show()

    def get_order_id_for_user_and_project(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        # Получаем последний заказ для текущего пользователя и проекта
        cursor.execute("""
                SELECT o.id_order 
                FROM `order` o
                JOIN room_project rp ON o.id_project = rp.id_project
                WHERE rp.title = ? AND rp.id_client = ? 
                ORDER BY o.order_date DESC
                LIMIT 1
            """, (self.project_name, self.current_user_id))
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def load_order_items_from_db(self, order_id):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        query = """
                            SELECT 
                                m.name, m.producer, m.length, m.width, m.price, m.count_pack, m.photo  
                            FROM 
                                order_item AS oi
                            JOIN 
                                material AS m ON oi.id_material = m.id_material
                            WHERE oi.id_order = ?
                        """
        cursor.execute(query, (order_id,))
        materials = cursor.fetchall()
        conn.close()
        return materials

    def set_order_id_for_display(self, order_id):
        self.order_id_for_display = order_id
        self.materials = self.load_order_items_from_db(self.order_id_for_display)
        self.update_material_blocks()

    def get_current_order_id(self):
        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()

        cursor.execute("SELECT MAX(id_order) FROM `order`")
        result = cursor.fetchone()
        conn.close()

        return result[0] if result else None

    def delete_material_from_order(self, block_index):
        material_index = self.current_material_index + block_index
        if 0 <= material_index < len(self.materials):
            material_name = self.materials[material_index][0]
            try:
                material_id = self.get_material_id(material_name)
                if material_id:
                    conn = sqlite3.connect("database.db")
                    cursor = conn.cursor()

                    # Удаляем материал из заказа
                    cursor.execute(
                        "DELETE FROM order_item WHERE id_order = ? AND id_material = ?",
                        (self.current_order_id, material_id)
                    )
                    conn.commit()
                    conn.close()

                    print(f"Материал '{material_name}' удален из заказа (id_order: {self.current_order_id}).")

                    # Обновляем список материалов и блоки
                    self.materials = self.load_order_items_from_db(self.current_order_id)
                    self.order()
                else:
                    print(f"Ошибка: материал '{material_name}' не найден в базе данных.")
            except Exception as e:
                print(f"Ошибка при удалении материала из заказа: {e}")
        else:
            print("Материал не найден.")

    def calculate_material_packs_needed(self, material_id, project_name, material_type_id):

        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()

        try:
            # Получаем размеры комнаты из базы данных
            cursor.execute("SELECT length, width, height FROM room_project WHERE title = ?", (project_name,))
            room_length, room_width, room_height = cursor.fetchone()
            room_area = room_length * room_width
            self.room_height = room_height  # сохраняем для использования в расчетах для обоев

            cursor.execute("SELECT length, width, count_pack FROM material WHERE id_material=?", (material_id,))
            material_length, material_width, pack_size = cursor.fetchone()

            # Проверка типа материала
            if material_type_id != 7:  # не обои
                material_length /= 100
                material_width /= 100
                material_area = material_length * material_width
                packs_needed = math.ceil(room_area / material_area / pack_size)
            else:  # обои
                material_width /= 100  # длина рулона в метрах
                room_perimeter = 2 * (room_length + room_width)  # периметр в метрах

                strips = math.ceil(room_perimeter / material_width)  # number of strips, room_perimeter in cm
                cursor.execute("SELECT length FROM material WHERE id_material=?", (material_id,))

                strips_per_roll = math.floor(material_length / self.room_height / 100)
                packs_needed = math.ceil(strips / strips_per_roll)

            print(f"packs_needed для material_id {material_id}: {packs_needed}")
            return packs_needed

        except Exception as e:
            print(f"Ошибка при расчете количества упаковок: {e}")
            return 0  # <---  Возвращаем 0 в случае ошибки
        finally:
            conn.close()

    def calculate_material_cost(self, material_id, packs_needed):

        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute("SELECT price FROM material WHERE id_material=?", (material_id,))
            price_per_pack = cursor.fetchone()[0]
            total_cost = packs_needed * price_per_pack
        return total_cost

    def calculate_order_total_cost(self, order_id):
        """Рассчитывает общую стоимость заказа."""
        conn = sqlite3.connect('database.db')
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT SUM(oi.quantity * m.price)
                FROM order_item oi
                JOIN material m ON oi.id_material = m.id_material
                WHERE oi.id_order = ?
                """,
                (order_id,)
            )
            total_cost = cursor.fetchone()[0]
            if total_cost is None:  # Обработка случая, когда в заказе нет товаров
                total_cost = 0

            cursor.execute("UPDATE `order` SET amount = ? WHERE id_order = ?", (total_cost, order_id))
            conn.commit()
        except sqlite3.Error as e:
            print(f"Ошибка при обновлении общей стоимости заказа: {e}")
        finally:
            conn.close()
        return total_cost

    def update_order_quantities_and_cost(self):

        if not self.current_order_id:
            return
        print(f"Обновление количества для заказа {self.current_order_id}, проект: {self.project_name}")
        try:
            conn = sqlite3.connect("database.db")
            cursor = conn.cursor()

            cursor.execute("SELECT id_project, length, width, height FROM room_project WHERE title = ?",
                           (self.project_name,))
            id_project, room_length, room_width, self.room_height = cursor.fetchone()
            room_area = room_length * room_width

            cursor.execute("SELECT id_material FROM order_item WHERE id_order = ?", (self.current_order_id,))
            order_items = cursor.fetchall()

            for material_id, in order_items:
                cursor.execute("""SELECT id_type FROM material WHERE id_material = ?""", (material_id,))
                material_type_id = cursor.fetchone()[0]

                packs_needed = self.calculate_material_packs_needed(material_id, self.project_name, material_type_id)
                material_cost = self.calculate_material_cost(material_id, packs_needed)

                cursor.execute("""
                        UPDATE order_item
                        SET quantity = ?
                        WHERE id_order = ? AND id_material = ?
                    """, (packs_needed, self.current_order_id, material_id))

                conn.commit()

            total_cost = self.calculate_order_total_cost(self.current_order_id)
            conn.close()
            print("Количество и общая стоимость заказа обновлены")

        except sqlite3.Error as e:
            print(f"Ошибка при обновлении количества: {e}")

    def show_material_info_for_selection(self, label, photo_label, material):

        name, producer, length, width, price, count, photo_path = material
        text = f"""
                      Название: {name}
                      Производитель: {producer}
                      Размеры: {length}x{width} см
                      Цена: {price} руб.
                      Количество в упаковке: {count}
                  """
        label.setText(text)
        pixmap = QPixmap(photo_path)
        pixmap = pixmap.scaled(photo_label.size(), Qt.KeepAspectRatio)
        photo_label.setPixmap(pixmap)
        photo_label.setAlignment(Qt.AlignCenter)

    def show_material_info_for_order(self, label, photo_label, material):

        name, producer, length, width, price, count_in_pack, photo_path = material

        conn = sqlite3.connect("database.db")
        cursor = conn.cursor()
        try:
            cursor.execute(
                """
                SELECT oi.quantity, o.amount
                FROM order_item oi
                JOIN `order` o ON oi.id_order = o.id_order
                WHERE oi.id_order = ? AND oi.id_material = ?
                """,
                (self.current_order_id, self.get_material_id(name))
            )

            packs_needed, total_order_amount = cursor.fetchone()
            material_cost = self.calculate_material_cost(self.get_material_id(name), packs_needed)

            text = label.text()

            text = f"""
                        Название: {name}
                        Производитель: {producer}
                        Размеры: {length}x{width} см
                        Цена за 1 уп.: {price} руб.
                        Количество в упаковке: {count_in_pack} шт.
                        """

            text += f"""
                        Необходимо упаковок: {packs_needed} шт.
                        Итоговая стоимость материала: {material_cost} руб.
                        """

            label.setText(text)
            self.total_cost_label.setText(f"Общая стоимость заказа: {total_order_amount} руб.")

            self.total_cost_label.setText(f"Общая стоимость заказа: {total_order_amount} руб.")


        except Exception as e:  # <---  Объединены except

            print(f"Ошибка при получении данных из БД в show_material_in_block: {e}")

            packs_needed = 0

            total_order_amount = 0

            material_cost = 0

        finally:
            conn.close()

        pixmap = QPixmap(photo_path)
        pixmap = pixmap.scaled(photo_label.size(), Qt.KeepAspectRatio)
        photo_label.setPixmap(pixmap)
        photo_label.setAlignment(Qt.AlignCenter)


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    application()
