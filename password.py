import os
import random 
import pyperclip 
from tkinter import *
from tkinter.ttk import *

# Функция для расчета пароля
def low(): 
    entry.delete(0, END) 

    # Получаем длину пароля
    length = var1.get() 

    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    uppercase_letters_and_lowercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    all_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789 !@#$%^&*()"
    password = "" 

    # Если выбрана низкая сложность
    if var.get() == 1: 
        for _ in range(length): 
            password += random.choice(lowercase_letters) 
        return password 

    # Если выбрана средняя сложность
    elif var.get() == 0: 
        for _ in range(length): 
            password += random.choice(uppercase_letters_and_lowercase) 
        return password 

    # Если выбрана высокая сложность
    elif var.get() == 3: 
        for _ in range(length): 
            password += random.choice(all_characters) 
        return password 
    else: 
        print("Выберите уровень сложности.") 


# Функция для генерации пароля
def generate(): 
    password1 = low() 
    entry.insert(10, password1) 


# Функция копирования пароля в буфер обмена
def copy1(): 
    random_password = entry.get() 
    pyperclip.copy(random_password) 

def checkExistence():
    # Проверяем наличие файла info.txt
    if os.path.exists("info.txt"):
        pass
    else:
        with open("info.txt", 'w'):
            pass

def appendNew():
    # Открываем файл для добавления новых записей
    with open("info.txt", 'a') as file:
        user_name = entry1.get() 
        site = entry2.get()
        random_password = entry.get()
        
        usrnm = "Имя пользователя: " + user_name + "\n"
        pwd = "Пароль: " + random_password + "\n"
        web = "Сайт: " + site + "\n"
        
        file.write("------------------------------------\n")
        file.write(usrnm)
        file.write(pwd)
        file.write(web)
        file.write("------------------------------------\n\n")

def readPasswords():
    # Автоматически открываем файл info.txt при нажатии кнопки
    try:
        os.startfile("info.txt")
    except Exception as e:
        print(f"Произошла ошибка: {e}")

# Основная функция
checkExistence()

# Создание графического интерфейса
root = Tk() 
var = IntVar() 
var1 = IntVar() 

# Заголовок окна
root.title("Менеджер паролей на Python") 

# Метка длины пароля
c_label = Label(root, text="Длина") 
c_label.grid(row=1) 

# Кнопки "Скопировать" и "Создать пароль"
copy_button = Button(root, text="Скопировать", command=copy1) 
copy_button.grid(row=0, column=2) 
generate_button = Button(root, text="Создать", command=generate) 
generate_button.grid(row=0, column=3) 

# Радиокнопки выбора уровня сложности
radio_low = Radiobutton(root, text="Низкий", variable=var, value=1) 
radio_low.grid(row=1, column=2, sticky='W') 
radio_medium = Radiobutton(root, text="Средний", variable=var, value=0) 
radio_medium.grid(row=1, column=3, sticky='W') 
radio_high = Radiobutton(root, text="Высокий", variable=var, value=3) 
radio_high.grid(row=1, column=4, sticky='W') 

# Раскрывающееся меню для выбора длины пароля
combo = Combobox(root, textvariable=var1) 
combo['values'] = (
    8, 9, 10, 11, 12, 13, 14, 15, 16, 
    17, 18, 19, 20, 21, 22, 23, 24, 25,
    26, 27, 28, 29, 30, 31, 32, "Длина"
) 
combo.current(0) 
combo.grid(column=1, row=1) 

# Поля ввода имени пользователя и сайта
userName = Label(root, text="Введите имя пользователя здесь") 
userName.grid(row=2) 
entry1 = Entry(root) 
entry1.grid(row=2, column=1) 

website = Label(root, text="Введите адрес сайта здесь") 
website.grid(row=3) 
entry2 = Entry(root) 
entry2.grid(row=3, column=1) 

random_password = Label(root, text="Сгенерированный пароль") 
random_password.grid(row=4) 
entry = Entry(root) 
entry.grid(row=4, column=1) 

# Кнопки сохранения и просмотра всех паролей
save_button = Button(root, text="Сохранить", command=appendNew) 
save_button.grid(row=2, column=2) 
show_button = Button(root, text="Показать все пароли", command=readPasswords) 
show_button.grid(row=2, column=3) 

# Запускаем основной цикл программы
root.mainloop()