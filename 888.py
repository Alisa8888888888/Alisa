import tkinter as tk
from tkinter import ttk, messagebox
import json
import os
from datetime import datetime

DATA_FILE = "expenses.json"

class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = self.load_data()

        # Поля ввода
        frame_input = tk.LabelFrame(root, text="Добавить расход", padx=10, pady=10)
        frame_input.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_input, text="Сумма:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(frame_input)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(frame_input, text="Категория:").grid(row=0, column=2)
        self.category_cb = ttk.Combobox(frame_input, values=["Еда", "Транспорт", "Развлечения", "Жилье", "Другое"])
        self.category_cb.grid(row=0, column=3)

        tk.Label(frame_input, text="Дата (ГГГГ-ММ-ДД):").grid(row=1, column=0)
        self.date_entry = tk.Entry(frame_input)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=1, column=1)

        btn_add = tk.Button(frame_input, text="Добавить расход", command=self.add_expense, bg="green", fg="white")
        btn_add.grid(row=1, column=2, columnspan=2, sticky="we", padx=5)

        # Фильтры
        frame_filter = tk.LabelFrame(root, text="Фильтрация и Итоги", padx=10, pady=10)
        frame_filter.pack(padx=10, pady=5, fill="x")

        tk.Label(frame_filter, text="Фильтр категории:").grid(row=0, column=0)
        self.filter_cat = ttk.Combobox(frame_filter, values=["Все"] + ["Еда", "Транспорт", "Развлечения", "Жилье", "Другое"])
        self.filter_cat.set("Все")
        self.filter_cat.grid(row=0, column=1)

        btn_filter = tk.Button(frame_filter, text="Применить фильтр", command=self.update_table)
        btn_filter.grid(row=0, column=2, padx=5)

        self.total_label = tk.Label(frame_filter, text="Итого: 0", font=("Arial", 10, "bold"))
        self.total_label.grid(row=0, column=3, padx=20)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Дата", "Категория", "Сумма"), show='headings')
        self.tree.heading("Дата", text="Дата")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Сумма", text="Сумма")
        self.tree.pack(padx=10, pady=10, fill="both", expand=True)

        self.update_table()

    def load_data(self):
        if os.path.exists(DATA_FILE):
            with open(DATA_FILE, "r", encoding="utf-8") as f:
                return json.load(f)
        return []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, indent=4, ensure_ascii=False)

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_cb.get()
        date_str = self.date_entry.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность суммы (>0) и даты (ГГГГ-ММ-ДД)")
            return

        if not category:
            messagebox.showwarning("Внимание", "Выберите категорию")
            return

        self.expenses.append({"date": date_str, "category": category, "amount": amount})
        self.save_data()
        self.update_table()
        self.amount_entry.delete(0, tk.END)

    def update_table(self):
        for item in self.tree.get_children():
            self.tree.delete(item)
        
        filter_cat = self.filter_cat.get()
        total = 0

        for exp in self.expenses:
            if filter_cat == "Все" or exp["category"] == filter_cat:
                self.tree.insert("", tk.END, values=(exp["date"], exp["category"], exp["amount"]))
                total += exp["amount"]
        
        self.total_label.config(text=f"Итого: {total:.2f}")

if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()
