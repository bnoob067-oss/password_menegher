import os
import random 
import pyperclip 
import tkinter as tk
from tkinter import ttk, messagebox
from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import serialization, hashes
from cryptography.hazmat.backends import default_backend
import base64

# Генерация или загрузка ключей RSA
def generate_or_load_keys():
    private_key_path = "private_key.pem"
    public_key_path = "public_key.pem"
    
    if os.path.exists(private_key_path) and os.path.exists(public_key_path):
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(
                key_file.read(),
                password=None,
                backend=default_backend()
            )
        
        with open(public_key_path, "rb") as key_file:
            public_key = serialization.load_pem_public_key(
                key_file.read(),
                backend=default_backend()
            )
    else:
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        with open(private_key_path, "wb") as key_file:
            key_file.write(private_key.private_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PrivateFormat.PKCS8,
                encryption_algorithm=serialization.NoEncryption()
            ))
        
        with open(public_key_path, "wb") as key_file:
            key_file.write(public_key.public_bytes(
                encoding=serialization.Encoding.PEM,
                format=serialization.PublicFormat.SubjectPublicKeyInfo
            ))
    
    return private_key, public_key

def encrypt_password(password, public_key):
    encrypted = public_key.encrypt(
        password.encode('utf-8'),
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return base64.b64encode(encrypted).decode('utf-8')

def decrypt_password(encrypted_password, private_key):
    encrypted_bytes = base64.b64decode(encrypted_password.encode('utf-8'))
    decrypted = private_key.decrypt(
        encrypted_bytes,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return decrypted.decode('utf-8')

def low(): 
    entry.delete(0, tk.END) 
    length = var1.get() 
    
    if length == "Длина" or length == "":
        length = 12
    else:
        length = int(length)
    
    lowercase_letters = "abcdefghijklmnopqrstuvwxyz"
    uppercase_letters_and_lowercase = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz"
    all_characters = "ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*()"
    password = "" 

    if var.get() == 1: 
        for _ in range(length): 
            password += random.choice(lowercase_letters) 
        return password 
    elif var.get() == 0: 
        for _ in range(length): 
            password += random.choice(uppercase_letters_and_lowercase) 
        return password 
    elif var.get() == 3: 
        for _ in range(length): 
            password += random.choice(all_characters) 
        return password 
    else: 
        messagebox.showwarning("Внимание", "Выберите уровень сложности.")
        return ""

def generate(): 
    password1 = low() 
    if password1:
        entry.delete(0, tk.END)
        entry.insert(0, password1) 

def copy1(): 
    random_password = entry.get() 
    if random_password:
        pyperclip.copy(random_password) 
        messagebox.showinfo("Успех", "Пароль скопирован в буфер обмена!")

def checkExistence():
    if not os.path.exists("info.txt"):
        with open("info.txt", 'w', encoding='utf-8') as file:
            file.write("")

def appendNew():
    user_name = entry1.get().strip()
    site = entry2.get().strip()
    random_password = entry.get().strip()
    
    if not user_name or not site or not random_password:
        messagebox.showwarning("Внимание", "Пожалуйста, заполните все поля!")
        return
    
    encrypted_password = encrypt_password(random_password, public_key)
    
    with open("info.txt", 'a', encoding='utf-8') as file:
        file.write("------------------------------------\n")
        file.write(f"Имя пользователя: {user_name}\n")
        file.write(f"Зашифрованный пароль: {encrypted_password}\n")
        file.write(f"Сайт: {site}\n")
        file.write("------------------------------------\n\n")
    
    messagebox.showinfo("Успех", "Пароль успешно сохранен!")
    entry1.delete(0, tk.END)
    entry2.delete(0, tk.END)
    entry.delete(0, tk.END)

def readPasswords():
    if not os.path.exists("info.txt"):
        messagebox.showwarning("Внимание", "Файл с паролями не найден!")
        return
    
    try:
        with open("info.txt", 'r', encoding='utf-8') as file:
            content = file.read()
        
        if not content.strip():
            messagebox.showinfo("Информация", "Нет сохраненных паролей.")
            return
        
        read_window = tk.Toplevel(root)
        read_window.title("Все пароли")
        read_window.geometry("600x400")
        
        text_widget = tk.Text(read_window, wrap=tk.WORD, font=("Courier", 10))
        text_widget.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)
        
        scrollbar = tk.Scrollbar(text_widget)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        text_widget.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=text_widget.yview)
        
        lines = content.split('\n')
        decrypted_content = []
        
        for line in lines:
            if line.startswith("Зашифрованный пароль:"):
                encrypted_pwd = line.split(": ", 1)[1]
                try:
                    decrypted_pwd = decrypt_password(encrypted_pwd, private_key)
                    decrypted_content.append(f"Пароль: {decrypted_pwd}")
                except Exception as e:
                    decrypted_content.append(f"Пароль: [Ошибка дешифрования]")
            else:
                decrypted_content.append(line)
        
        text_widget.insert(1.0, '\n'.join(decrypted_content))
        text_widget.config(state=tk.DISABLED)
        
    except Exception as e:
        messagebox.showerror("Ошибка", f"Не удалось прочитать файл: {e}")

def deletePasswords():
    def perform_delete():
        username = delete_entry.get().strip()
        if not username:
            messagebox.showwarning("Внимание", "Введите имя пользователя для удаления!")
            return
        
        if not os.path.exists("info.txt"):
            messagebox.showwarning("Внимание", "Файл с паролями не найден!")
            delete_window.destroy()
            return
        
        with open("info.txt", 'r', encoding='utf-8') as file:
            lines = file.readlines()
        
        new_lines = []
        found = False
        skip_block = False
        current_block = []
        
        for line in lines:
            if line.startswith("------------------------------------"):
                if skip_block:
                    current_block = []
                    skip_block = False
                    continue
                elif current_block:
                    new_lines.extend(current_block)
                    current_block = [line]
                else:
                    current_block = [line]
            else:
                if not skip_block:
                    current_block.append(line)
                    if line.startswith("Имя пользователя:") and username in line:
                        found = True
                        skip_block = True
                        current_block = []
        
        if current_block and not skip_block:
            new_lines.extend(current_block)
        
        if found:
            with open("info.txt", 'w', encoding='utf-8') as file:
                file.writelines(new_lines)
            messagebox.showinfo("Успех", f"Пароли для пользователя '{username}' успешно удалены!")
        else:
            messagebox.showwarning("Внимание", f"Пользователь '{username}' не найден!")
        
        delete_window.destroy()
    
    delete_window = tk.Toplevel(root)
    delete_window.title("Удалить пароль")
    delete_window.geometry("400x150")
    delete_window.resizable(False, False)
    
    ttk.Label(delete_window, text="Введите имя пользователя для удаления всех его паролей:", 
              font=("Arial", 10)).pack(pady=10)
    
    delete_entry = ttk.Entry(delete_window, width=40, font=("Arial", 10))
    delete_entry.pack(pady=5)
    
    button_frame = ttk.Frame(delete_window)
    button_frame.pack(pady=10)
    
    tk.Button(button_frame, text="Удалить", command=perform_delete, 
             bg="red", fg="white").pack(side=tk.LEFT, padx=5)
    tk.Button(button_frame, text="Отмена", command=delete_window.destroy).pack(side=tk.LEFT, padx=5)
    
    delete_entry.focus()

# Генерируем или загружаем ключи
private_key, public_key = generate_or_load_keys()

checkExistence()

# Создание графического интерфейса
root = tk.Tk() 
root.title("Менеджер паролей на Python (с шифрованием RSA)") 
root.geometry("700x300")
root.resizable(False, False)

var = tk.IntVar(value=1) 
var1 = tk.IntVar(value=12) 

# Метка длины пароля (ttk.Label - без fg/bg)
ttk.Label(root, text="Длина:").grid(row=1, column=0, sticky='w', padx=5)

# Кнопки (tk.Button для цвета)
tk.Button(root, text="Скопировать", command=copy1, width=12, bg="lightblue").grid(row=0, column=2, padx=5) 
tk.Button(root, text="Создать пароль", command=generate, width=12, bg="lightgreen").grid(row=0, column=3, padx=5) 

# Радиокнопки (ttk.Radiobutton)
ttk.Radiobutton(root, text="Низкий", variable=var, value=1).grid(row=1, column=2, sticky='w') 
ttk.Radiobutton(root, text="Средний", variable=var, value=0).grid(row=1, column=3, sticky='w') 
ttk.Radiobutton(root, text="Высокий", variable=var, value=3).grid(row=1, column=4, sticky='w') 

# Раскрывающееся меню
combo = ttk.Combobox(root, textvariable=var1, values=[8,9,10,11,12,13,14,15,16,17,18,19,20,21,22,23,24,25,26,27,28,29,30,31,32], width=5) 
combo.current(4)
combo.grid(column=1, row=1, sticky='w') 

# Поля ввода (ttk.Entry)
ttk.Label(root, text="Имя пользователя:").grid(row=2, column=0, sticky='w', padx=5, pady=5) 
entry1 = ttk.Entry(root, width=30) 
entry1.grid(row=2, column=1, padx=5) 

ttk.Label(root, text="Адрес сайта:").grid(row=3, column=0, sticky='w', padx=5, pady=5) 
entry2 = ttk.Entry(root, width=30) 
entry2.grid(row=3, column=1, padx=5) 

ttk.Label(root, text="Сгенерированный пароль:").grid(row=4, column=0, sticky='w', padx=5, pady=5) 
entry = ttk.Entry(root, width=30) 
entry.grid(row=4, column=1, padx=5) 

# Кнопки управления (tk.Button для цвета)
tk.Button(root, text="Сохранить", command=appendNew, width=12, bg="green", fg="white").grid(row=2, column=2, padx=5) 
tk.Button(root, text="Показать все", command=readPasswords, width=12, bg="lightblue").grid(row=2, column=3, padx=5) 
tk.Button(root, text="Удалить пароль", command=deletePasswords, width=15, bg="orange").grid(row=3, column=2, padx=5) 

# ИНФОРМАЦИОННАЯ МЕТКА - ИСПОЛЬЗУЕМ tk.Label (поддерживает fg)
tk.Label(root, text="🔒 Пароли сохраняются в зашифрованном виде (RSA-2048)", 
         font=("Arial", 9), fg="blue").grid(row=5, column=0, columnspan=4, pady=10)

root.mainloop()
