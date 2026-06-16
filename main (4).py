import tkinter as tk
from tkinter import messagebox


class BMICalculator:
    def __init__(self):
        self.window = tk.Tk()
        self.window.title("⚖️ BMI Калькулятор")
        self.window.geometry("380x550")
        self.window.configure(bg='#F0F4F8')
        self.window.resizable(False, False)

        # Заголовок
        tk.Label(
            text="⚖️ ИНДЕКС МАССЫ ТЕЛА",
            font=("Arial", 16, "bold"),
            bg='#F0F4F8',
            fg='#2C3E50'
        ).pack(pady=20)

        # Выбор пола
        tk.Label(text="Пол:", font=("Arial", 12), bg='#F0F4F8').pack()
        self.gender_var = tk.StringVar(value="male")

        gender_frame = tk.Frame(bg='#F0F4F8')
        gender_frame.pack(pady=5)

        tk.Radiobutton(gender_frame, text="👨 Мужской", variable=self.gender_var,
                       value="male", font=("Arial", 11), bg='#F0F4F8').pack(side='left', padx=10)
        tk.Radiobutton(gender_frame, text="👩 Женский", variable=self.gender_var,
                       value="female", font=("Arial", 11), bg='#F0F4F8').pack(side='left', padx=10)

        # Ввод веса
        tk.Label(text="Вес (кг):", font=("Arial", 12), bg='#F0F4F8').pack(pady=(15, 5))
        self.weight_entry = tk.Entry(font=("Arial", 14), width=15, justify='center', bd=3)
        self.weight_entry.pack()

        # Ввод роста
        tk.Label(text="Рост (см):", font=("Arial", 12), bg='#F0F4F8').pack(pady=(15, 5))
        self.height_entry = tk.Entry(font=("Arial", 14), width=15, justify='center', bd=3)
        self.height_entry.pack()

        # Кнопка расчёта
        tk.Button(
            text="📊 РАССЧИТАТЬ BMI",
            command=self.calculate_bmi,
            bg='#3498DB',
            fg='white',
            font=("Arial", 14, "bold"),
            width=20,
            height=2,
            relief='raised',
            bd=3
        ).pack(pady=20)

        # Результат
        self.result_frame = tk.Frame(bg='white', relief='sunken', bd=2)
        self.result_frame.pack(pady=10, padx=30, fill='x')

        self.result_label = tk.Label(
            self.result_frame,
            text="Введите данные\nи нажмите Рассчитать",
            font=("Arial", 13),
            bg='white',
            fg='#7F8C8D',
            height=3
        )
        self.result_label.pack(pady=10)

        # Шкала BMI
        self.scale_frame = tk.Frame(bg='#F0F4F8')
        self.scale_frame.pack(pady=15)

        self.scale_canvas = tk.Canvas(self.scale_frame, width=300, height=30, bg='#F0F4F8', highlightthickness=0)
        self.scale_canvas.pack()

        # Кнопка очистки
        tk.Button(
            text="🗑️ Очистить",
            command=self.clear_fields,
            bg='#E74C3C',
            fg='white',
            font=("Arial", 11),
            width=15,
            height=1
        ).pack(pady=5)

        # Меню
        self.menu_bar = tk.Menu(self.window)
        self.window.config(menu=self.menu_bar)

        self.file_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="📁 Файл", menu=self.file_menu)
        self.file_menu.add_command(label="📋 Копировать результат", command=self.copy_result)
        self.file_menu.add_command(label="🗑️ Очистить", command=self.clear_fields)
        self.file_menu.add_separator()
        self.file_menu.add_command(label="🚪 Выход", command=self.exit_app)

        self.help_menu = tk.Menu(self.menu_bar, tearoff=0)
        self.menu_bar.add_cascade(label="❓ Справка", menu=self.help_menu)
        self.help_menu.add_command(label="📖 Таблица BMI", command=self.show_bmi_table)
        self.help_menu.add_command(label="ℹ️ О программе", command=self.show_about)

        # Горячие клавиши
        self.window.bind('<Return>', lambda e: self.calculate_bmi())
        self.window.bind('<Escape>', lambda e: self.clear_fields())

    def calculate_bmi(self):
        try:
            weight = float(self.weight_entry.get())
            height = float(self.height_entry.get()) / 100  # в метры
        except ValueError:
            messagebox.showerror("❌ Ошибка", "Введите числа в поля веса и роста!")
            return

        if weight <= 0 or weight > 500:
            messagebox.showerror("❌ Ошибка", "Некорректный вес! (1-500 кг)")
            return

        if height <= 0 or height > 2.5:
            messagebox.showerror("❌ Ошибка", "Некорректный рост! (1-250 см)")
            return

        # Расчёт BMI
        bmi = weight / (height * height)
        bmi = round(bmi, 1)

        # Определение категории
        if bmi < 16:
            category = "Выраженный дефицит"
            color = "#E74C3C"
            emoji = "⚠️"
        elif bmi < 18.5:
            category = "Недостаточный вес"
            color = "#F39C12"
            emoji = "⚡"
        elif bmi < 25:
            category = "Нормальный вес"
            color = "#27AE60"
            emoji = "✅"
        elif bmi < 30:
            category = "Избыточный вес"
            color = "#F39C12"
            emoji = "⚠️"
        elif bmi < 35:
            category = "Ожирение 1 степени"
            color = "#E74C3C"
            emoji = "🔴"
        elif bmi < 40:
            category = "Ожирение 2 степени"
            color = "#C0392B"
            emoji = "🔴"
        else:
            category = "Ожирение 3 степени"
            color = "#922B21"
            emoji = "💀"

        # Отображение результата
        self.result_label.config(
            text=f"BMI: {bmi}\n{emoji} {category}",
            fg=color
        )

        # Рисование шкалы
        self.draw_scale(bmi)

    def draw_scale(self, bmi):
        self.scale_canvas.delete("all")

        # Цветовые зоны
        zones = [
            (0, 16, "#3498DB"),  # Синий - дефицит
            (16, 18.5, "#F39C12"),  # Оранжевый - недостаток
            (18.5, 25, "#27AE60"),  # Зелёный - норма
            (25, 30, "#F39C12"),  # Оранжевый - избыток
            (30, 35, "#E74C3C"),  # Красный - ожирение 1
            (35, 40, "#C0392B"),  # Тёмно-красный - ожирение 2
        ]

        for start, end, color in zones:
            x1 = (start / 40) * 300
            x2 = (end / 40) * 300
            self.scale_canvas.create_rectangle(x1, 0, x2, 30, fill=color, outline="")

        # Указатель
        if bmi <= 40:
            x = (bmi / 40) * 300
            self.scale_canvas.create_line(x, 0, x, 30, fill="black", width=3)
            self.scale_canvas.create_text(x, 15, text="▼", font=("Arial", 8), fill="black")

        # Подписи
        for val in [0, 16, 18.5, 25, 30, 35, 40]:
            x = (val / 40) * 300
            self.scale_canvas.create_text(x, 35, text=str(val), font=("Arial", 7))

    def clear_fields(self):
        self.weight_entry.delete(0, tk.END)
        self.height_entry.delete(0, tk.END)
        self.result_label.config(text="Введите данные\nи нажмите Рассчитать", fg='#7F8C8D')
        self.scale_canvas.delete("all")

    def copy_result(self):
        text = self.result_label.cget("text")
        if "BMI:" in text:
            self.window.clipboard_clear()
            self.window.clipboard_append(text)
            messagebox.showinfo("📋 Копирование", "Результат скопирован!")
        else:
            messagebox.showwarning("⚠️ Внимание", "Нет результата для копирования!")

    def show_bmi_table(self):
        table = """
📖 ТАБЛИЦА ИНДЕКСА МАССЫ ТЕЛА

🔵 < 16.0 - Выраженный дефицит
🟠 16.0-18.5 - Недостаточный вес
🟢 18.5-25.0 - НОРМАЛЬНЫЙ ВЕС ✅
🟠 25.0-30.0 - Избыточный вес
🔴 30.0-35.0 - Ожирение 1 степени
🔴 35.0-40.0 - Ожирение 2 степени
💀 > 40.0 - Ожирение 3 степени

Формула: BMI = Вес(кг) / Рост(м)²
        """
        messagebox.showinfo("📖 Таблица BMI", table)

    def show_about(self):
        about = """
⚖️ BMI КАЛЬКУЛЯТОР
Версия 1.0

Простой калькулятор для расчёта
Индекса Массы Тела (BMI).

Функции:
• Расчёт BMI
• Визуальная шкала
• Категории веса
• Копирование результата

© 2024 BMI Calculator
        """
        messagebox.showinfo("ℹ️ О программе", about)

    def exit_app(self):
        if messagebox.askyesno("🚪 Выход", "Закрыть калькулятор?"):
            self.window.destroy()

    def run(self):
        self.window.mainloop()


if __name__ == "__main__":
    app = BMICalculator()
    app.run()