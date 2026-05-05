import tkinter as tk
from tkinter import ttk
import string
import random
import json
def generate_password():
    length = int(length_slider.get())
    use_digits = digits_checkbox_var.get()
    use_letters = letters_checkbox_var.get()
    use_special_chars = special_chars_checkbox_var.get()
    chars = ''
    if use_digits:
        chars += string.digits
    if use_letters:
        chars += string.ascii_letters
    if use_special_chars:
        chars += string.punctuation
    password = ''.join(random.choice(chars) for _ in range(length))
    result_label.config(text=password)
    # Сохраняем историю
    history.append(password)
    save_history()
    update_table()
def save_history():
    with open('history.json', 'w') as f:
        json.dump(history, f)
def load_history():
    try:
        with open('history.json', 'r') as f:
            return json.load(f)
    except FileNotFoundError:
        return []
def update_table():
    table.delete(*table.get_children())  # Очистить таблицу
    for i, pwd in enumerate(reversed(history)):
        table.insert('', 'end', values=(len(history)-i, pwd))
root = tk.Tk()
root.title("Random Password Generator")
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))
length_slider = ttk.Scale(frame, from_=4, to=20, orient='horizontal')
length_slider.set(12)
length_slider.grid(row=0, columnspan=3, pady=10)
digits_checkbox_var = tk.IntVar(value=1)
letters_checkbox_var = tk.IntVar(value=1)
special_chars_checkbox_var = tk.IntVar(value=1)
ttk.Checkbutton(frame, text="Цифры", variable=digits_checkbox_var).grid(row=1, column=0)
ttk.Checkbutton(frame, text="Буквы", variable=letters_checkbox_var).grid(row=1, column=1)
ttk.Checkbutton(frame, text="Специальные символы", variable=special_chars_checkbox_var).grid(row=1, column=2)
generate_button = ttk.Button(frame, text="Генерировать пароль", command=generate_password)
generate_button.grid(row=2, columnspan=3, pady=10)
result_label = ttk.Label(frame, text="", font=("Arial", 14))
result_label.grid(row=3, columnspan=3, pady=10)
table_frame = ttk.Frame(frame)
table_frame.grid(row=4, columnspan=3, pady=10)
table = ttk.Treeview(table_frame, columns=("#1", "#2"), show="headings")
table.heading("#1", text="#")
table.heading("#2", text="Пароль")
table.pack(side="left", fill="both", expand=True)
scrollbar = ttk.Scrollbar(table_frame, orient="vertical", command=table.yview)
scrollbar.pack(side="right", fill="y")
table.configure(yscrollcommand=scrollbar.set)
history = load_history()
update_table()
root.mainloop()
