import sqlite3
import datetime

from PyQt5 import QtWidgets
from PyQt5.QtGui import QFont, QPixmap
from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QWidget, QVBoxLayout, QDialog, QLineEdit, \
    QHBoxLayout, QRadioButton
from PyQt5.QtCore import Qt, QRect

import sys

class Window(QMainWindow):
    def __init__(self):
        super(Window, self).__init__()

        self.setWindowTitle("РосСтройТорг расчет")
        self.setFixedSize(700, 500)


        #тут будет регистрация/вход

        self.current_material_index = 0
        self.current_order_id = None  # ID текущего заказа
        self.project_name = 'project_name'
        #self.materials_floor(1) # не забудь перейти на главное окно
        #self.main_window()
        #self.order()
        self.type_of_floor()


    def main_window(self):
        self.clear_window()

        central_widget = QWidget(self)
        self.setCentralWidget(central_widget)

        title = QLabel("РосСтройТорг расчет", self)
        title.setAlignment(Qt.AlignCenter)
        title.setFont(QFont("Arial", 22))
        title.setGeometry(QRect(0, 20, 700, 50))  # позиция и размер

        projects = QLabel("Проект комнаты 1\nПроект комнаты 2\nПроект комнаты 3\nПроект комнаты 4", self) #должен быть вывод кнопок проектов
        projects.setFont(QFont("Arial", 14))
        projects.setAlignment(Qt.AlignCenter)
        projects.setGeometry(QRect(0, 150, 700, 100))

        create_project_button = QPushButton("Создать проект", self)
        create_project_button.clicked.connect(self.create_project)
        create_project_button.setFixedSize(200, 50)
        create_project_button.setGeometry(QRect(250, 350, 200, 50))

        central_widget.setLayout(QtWidgets.QVBoxLayout())

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
                conn = sqlite3.connect("database.db")
                cursor = conn.cursor()

                cursor.execute(
                    "INSERT INTO room_project (id_client, length, width, height, title) VALUES (?, ?, ?, ?, ?)",
                    (1, 0, 0, 0, project_name
                ))
                conn.commit()
                conn.close()
                self.project_name = project_name
                print(f"Название проекта '{project_name}' сохранено в базе данных.")
                dialog.accept()
            except Exception as e:
                print(f"Ошибка при сохранении проекта: {e}")
        else:
            print("Название проекта не может быть пустым.")

    def input_room(self):
        pass

    def type_of_floor(self):
        self.clear_window()
        self.floor_type_window = QWidget(self)
        self.floor_type_window.setWindowTitle(" ")
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
        next_button.clicked.connect(self.on_next_button_clicked)  # Подключаем обработчик

        self.floor_type_window.show()

    def on_next_button_clicked(self):
        if self.radio_button1.isChecked():
            type_material_name = "Ламинат"
        elif self.radio_button2.isChecked():
            type_material_name = "Паркет"
        elif self.radio_button3.isChecked():
            type_material_name = "Плитка для пола"
        else:
            type_material_name = ""  # Или какое-то значение по умолчанию

        type_material_id = self.get_type_material_id_by_name(type_material_name)

        if type_material_id:
            self.materials_floor(type_material_id, 'floor')
        else:
            print(f"Ошибка: тип материала '{type_material_name}' не найден в базе данных.")
            # Добавьте обработку ошибки, например, вывод сообщения пользователю

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

        self.materials_window = QWidget(self)
        self.materials_window.setWindowTitle("Материалы")
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
        material_index = self.current_material_index + block_index
        if 0 <= material_index < len(self.materials):
            material_name = self.materials[material_index][0]

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

                    self.update_order_items()  # Обновляем элементы заказа (если нужно)
                else:
                    print(f"Ошибка: материал '{material_name}' не найден в базе данных.")
            except Exception as e:
                print(f"Ошибка при добавлении материала в заказ: {e}")
        else:
            print("Материал не найден.")

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

    #обновляет записи в обоих блоках
    def update_material_blocks(self):
        for i, (label, photo_label) in enumerate(
                [(self.block1_label, self.block1_photo), (self.block2_label, self.block2_photo)]
        ):
            material_index = self.current_material_index + i
            if len(self.materials) > material_index:
                self.show_material_in_block(label, photo_label, material_index)
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
            # Добавьте обработку ошибки, например, вывод сообщения пользователю


    def order(self):
        '''self.order_window = QWidget(self)
        self.order_window.setWindowTitle("Заказ")
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
        # ... (загрузка изображения) ...
        self.block1_photo.setAlignment(Qt.AlignCenter)

        self.block1_label = QLabel(self.block1_widget)
        self.block1_label.setAlignment(Qt.AlignLeft)
        self.block1_label.setFixedWidth(230)
        self.block1_label.setWordWrap(True)

        self.block1_button_delete = QPushButton("Удалить", self.block1_widget)
        # self.block1_button_delete.clicked.connect(lambda: self.delete_material_from_order(0))
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
        # ... (загрузка изображения) ...
        self.block2_photo.setAlignment(Qt.AlignCenter)

        self.block2_label = QLabel(self.block2_widget)
        self.block2_label.setAlignment(Qt.AlignLeft)
        self.block2_label.setFixedWidth(230)
        self.block2_label.setWordWrap(True)

        self.block2_button_delete = QPushButton("Удалить", self.block2_widget)
        # self.block2_button_delete.clicked.connect(lambda: self.delete_material_from_order(1))
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

        next_button = QPushButton("Далее", self.order_window)
        next_button.setFixedSize(90, 40)
        next_button.move(580, 420)

        self.current_material_index = 0
        self.materials = self.load_order_items_from_db()
        self.update_material_blocks()  # Обновляем оба блока
'''
        self.clear_window()
        self.current_order_id = self.get_current_order_id()  # ID последнего созданного заказа
        self.order_window = QWidget(self)
        self.order_window.setWindowTitle("Заказ")
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

        self.order_window.show()



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
                    self.update_material_blocks()
                else:
                    print(f"Ошибка: материал '{material_name}' не найден в базе данных.")
            except Exception as e:
                print(f"Ошибка при удалении материала из заказа: {e}")
        else:
            print("Материал не найден.")


def application():
    app = QApplication(sys.argv)
    window = Window()

    window.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
    application()