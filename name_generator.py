"""
name_generator.py - Генератор случайных имён на Python (CLI + GUI)
Поддерживает культуры: en, ru, es, de, fr, it.
Режимы: имя, имя+фамилия, никнейм.
Экспорт в TXT, CSV.
"""
import argparse
import json
import random
import sys
import os
from pathlib import Path

# ========== БАЗА ДАННЫХ ==========
NAMES = {
    "en": {
        "male": ["James", "John", "Robert", "Michael", "William", "David", "Richard", "Joseph", "Thomas", "Charles"],
        "female": ["Mary", "Patricia", "Jennifer", "Linda", "Barbara", "Elizabeth", "Susan", "Jessica", "Sarah", "Karen"],
        "surname": ["Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis", "Rodriguez", "Martinez"]
    },
    "ru": {
        "male": ["Александр", "Дмитрий", "Максим", "Сергей", "Андрей", "Алексей", "Иван", "Евгений", "Михаил", "Николай"],
        "female": ["Анна", "Мария", "Екатерина", "Ольга", "Татьяна", "Наталья", "Ирина", "Елена", "Светлана", "Юлия"],
        "surname": ["Иванов", "Петров", "Сидоров", "Кузнецов", "Смирнов", "Волков", "Морозов", "Новиков", "Козлов", "Лебедев"]
    },
    "es": {
        "male": ["Alejandro", "Carlos", "David", "Francisco", "Javier", "José", "Juan", "Luis", "Manuel", "Miguel"],
        "female": ["Ana", "Carmen", "Elena", "Isabel", "Laura", "Lucía", "María", "Marta", "Paula", "Sara"],
        "surname": ["García", "López", "Martínez", "Rodríguez", "González", "Pérez", "Sánchez", "Ramírez", "Torres", "Rivera"]
    },
    "de": {
        "male": ["Hans", "Peter", "Michael", "Klaus", "Andreas", "Thomas", "Stefan", "Jürgen", "Wolfgang", "Heinz"],
        "female": ["Anna", "Maria", "Andrea", "Susanne", "Karin", "Petra", "Monika", "Margarete", "Ursula", "Sabine"],
        "surname": ["Müller", "Schmidt", "Schneider", "Fischer", "Weber", "Meyer", "Wagner", "Becker", "Schulz", "Hoffmann"]
    },
    "fr": {
        "male": ["Jean", "Pierre", "Michel", "Philippe", "André", "Jacques", "François", "Paul", "Daniel", "Louis"],
        "female": ["Marie", "Jeanne", "Françoise", "Catherine", "Nathalie", "Isabelle", "Sophie", "Anne", "Élisabeth", "Christine"],
        "surname": ["Martin", "Bernard", "Dubois", "Thomas", "Robert", "Richard", "Petit", "Durand", "Leroy", "Moreau"]
    },
    "it": {
        "male": ["Giuseppe", "Antonio", "Giovanni", "Francesco", "Luigi", "Angelo", "Pietro", "Salvatore", "Vincenzo", "Mario"],
        "female": ["Maria", "Anna", "Giuseppa", "Antonia", "Rosa", "Teresa", "Lucia", "Francesca", "Angela", "Caterina"],
        "surname": ["Rossi", "Russo", "Ferrari", "Esposito", "Bianchi", "Romano", "Colombo", "Ricci", "Marino", "Greco"]
    }
}

ADJECTIVES = {
    "en": ["Brave", "Clever", "Swift", "Bold", "Wise", "Fierce", "Gentle", "Loyal", "Valiant", "Bright"],
    "ru": ["Храбрый", "Умный", "Быстрый", "Смелый", "Мудрый", "Свирепый", "Нежный", "Верный", "Доблестный", "Светлый"],
    "es": ["Valiente", "Inteligente", "Rápido", "Audaz", "Sabio", "Feroz", "Gentil", "Leal", "Valeroso", "Brillante"],
    "de": ["Tapfer", "Klug", "Schnell", "Kühn", "Weise", "Wild", "Sanft", "Treu", "Mutig", "Hell"],
    "fr": ["Brave", "Intelligent", "Rapide", "Audacieux", "Sage", "Féroce", "Doux", "Loyal", "Vaillant", "Brillant"],
    "it": ["Coraggioso", "Intelligente", "Veloce", "Audace", "Saggio", "Feroce", "Gentile", "Leale", "Valoroso", "Brillante"]
}

NOUNS = {
    "en": ["Wolf", "Eagle", "Lion", "Tiger", "Bear", "Hawk", "Dragon", "Phoenix", "Raven", "Falcon"],
    "ru": ["Волк", "Орёл", "Лев", "Тигр", "Медведь", "Ястреб", "Дракон", "Феникс", "Ворон", "Сокол"],
    "es": ["Lobo", "Águila", "León", "Tigre", "Oso", "Halcón", "Dragón", "Fénix", "Cuervo", "Halcón"],
    "de": ["Wolf", "Adler", "Löwe", "Tiger", "Bär", "Falke", "Drache", "Phönix", "Rabe", "Falke"],
    "fr": ["Loup", "Aigle", "Lion", "Tigre", "Ours", "Faucon", "Dragon", "Phénix", "Corbeau", "Faucon"],
    "it": ["Lupo", "Aquila", "Leone", "Tigre", "Orso", "Falco", "Drago", "Fenice", "Corvo", "Falco"]
}

# ========== ЛОГИКА ==========
class NameGenerator:
    def __init__(self, culture="en", gender="any", seed=None):
        self.culture = culture
        self.gender = gender
        if seed is not None:
            random.seed(seed)
        self.data = NAMES.get(culture, NAMES["en"])
        self.adj = ADJECTIVES.get(culture, ADJECTIVES["en"])
        self.nouns = NOUNS.get(culture, NOUNS["en"])

    def get_names(self, gender=None):
        g = gender or self.gender
        if g == "male":
            pool = self.data["male"]
        elif g == "female":
            pool = self.data["female"]
        else:
            pool = self.data["male"] + self.data["female"]
        return pool

    def get_surnames(self):
        return self.data["surname"]

    def generate_name(self, full=False, nickname=False, gender=None):
        if nickname:
            adj = random.choice(self.adj)
            noun = random.choice(self.nouns)
            return f"{adj} {noun}"
        first = random.choice(self.get_names(gender))
        if full:
            surname = random.choice(self.get_surnames())
            return f"{first} {surname}"
        return first

    def generate_batch(self, count=1, full=False, nickname=False, gender=None, as_list=False):
        result = []
        for _ in range(count):
            result.append(self.generate_name(full, nickname, gender))
        return result

    def export(self, names, filepath, fmt="txt"):
        with open(filepath, 'w', encoding='utf-8') as f:
            if fmt == "csv":
                for name in names:
                    f.write(f"{name}\n")  # упрощённо, можно с заголовками
            else:
                f.write("\n".join(names))

# ========== CLI ==========
def cli():
    parser = argparse.ArgumentParser(description="Генератор случайных имён")
    parser.add_argument("-c", "--count", type=int, default=1, help="Количество имён")
    parser.add_argument("--culture", default="en", choices=NAMES.keys(), help="Культура")
    parser.add_argument("--gender", choices=["male", "female", "any"], default="any", help="Пол")
    parser.add_argument("--full", action="store_true", help="Добавить фамилию")
    parser.add_argument("--nickname", action="store_true", help="Сгенерировать никнейм")
    parser.add_argument("--seed", type=int, help="Seed для воспроизводимости")
    parser.add_argument("--output", help="Файл для сохранения (txt или csv)")
    parser.add_argument("--format", choices=["txt", "csv"], default="txt", help="Формат экспорта")
    parser.add_argument("--gui", action="store_true", help="Запустить GUI (если доступен)")
    args = parser.parse_args()

    if args.gui:
        try:
            from tkinter import Tk
            from gui import NameGeneratorGUI  # отдельный модуль
            root = Tk()
            app = NameGeneratorGUI(root)
            root.mainloop()
        except ImportError:
            print("Tkinter не установлен. Запустите без --gui.")
        return

    gen = NameGenerator(args.culture, args.gender, args.seed)
    names = gen.generate_batch(args.count, args.full, args.nickname, args.gender)
    for name in names:
        print(name)
    if args.output:
        gen.export(names, args.output, args.format)
        print(f"Сохранено в {args.output}")

# ========== GUI (упрощённый) ==========
try:
    import tkinter as tk
    from tkinter import ttk, messagebox
    GUI_AVAILABLE = True
except ImportError:
    GUI_AVAILABLE = False

if GUI_AVAILABLE:
    class NameGeneratorGUI:
        def __init__(self, root):
            self.root = root
            self.root.title("Генератор имён")
            self.root.geometry("500x400")
            self.root.resizable(False, False)
            self.gen = NameGenerator()
            self.create_widgets()

        def create_widgets(self):
            # Культура
            tk.Label(self.root, text="Культура:").grid(row=0, column=0, padx=5, pady=5, sticky="w")
            self.culture_var = tk.StringVar(value="en")
            culture_menu = ttk.Combobox(self.root, textvariable=self.culture_var, values=list(NAMES.keys()))
            culture_menu.grid(row=0, column=1, padx=5, pady=5)
            # Пол
            tk.Label(self.root, text="Пол:").grid(row=1, column=0, padx=5, pady=5, sticky="w")
            self.gender_var = tk.StringVar(value="any")
            gender_menu = ttk.Combobox(self.root, textvariable=self.gender_var, values=["any", "male", "female"])
            gender_menu.grid(row=1, column=1, padx=5, pady=5)
            # Количество
            tk.Label(self.root, text="Количество:").grid(row=2, column=0, padx=5, pady=5, sticky="w")
            self.count_var = tk.IntVar(value=1)
            tk.Spinbox(self.root, from_=1, to=100, textvariable=self.count_var, width=10).grid(row=2, column=1, padx=5, pady=5)
            # Опции
            self.full_var = tk.BooleanVar()
            tk.Checkbutton(self.root, text="Имя + фамилия", variable=self.full_var).grid(row=3, column=0, columnspan=2, pady=2)
            self.nick_var = tk.BooleanVar()
            tk.Checkbutton(self.root, text="Никнейм", variable=self.nick_var).grid(row=4, column=0, columnspan=2, pady=2)
            # Кнопка
            tk.Button(self.root, text="Сгенерировать", command=self.generate).grid(row=5, column=0, columnspan=2, pady=10)
            # Результат
            self.result_text = tk.Text(self.root, height=10, width=50)
            self.result_text.grid(row=6, column=0, columnspan=2, padx=5, pady=5)
            # Кнопка сохранения
            tk.Button(self.root, text="Сохранить в файл", command=self.save).grid(row=7, column=0, columnspan=2, pady=5)

        def generate(self):
            culture = self.culture_var.get()
            gender = self.gender_var.get()
            count = self.count_var.get()
            full = self.full_var.get()
            nick = self.nick_var.get()
            self.gen = NameGenerator(culture, gender)
            names = self.gen.generate_batch(count, full, nick, gender)
            self.result_text.delete(1.0, tk.END)
            self.result_text.insert(tk.END, "\n".join(names))

        def save(self):
            content = self.result_text.get(1.0, tk.END).strip()
            if not content:
                messagebox.showwarning("Нет данных", "Сначала сгенерируйте имена")
                return
            from tkinter import filedialog
            f = filedialog.asksaveasfilename(defaultextension=".txt", filetypes=[("Text files", "*.txt"), ("CSV files", "*.csv")])
            if f:
                with open(f, 'w', encoding='utf-8') as file:
                    file.write(content)
                messagebox.showinfo("Сохранено", f"Сохранено в {f}")

if __name__ == "__main__":
    cli()
