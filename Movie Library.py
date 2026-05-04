import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

class MovieLibraryApp:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library")
        self.movies = []
        
        # Автоматическая загрузка данных при запуске приложения
        self.load_data()

        # --- Поля ввода ---
        ttk.Label(root, text="Название:").grid(row=0, column=0, padx=5, pady=5)
        self.title_entry = ttk.Entry(root, width=30)
        self.title_entry.grid(row=0, column=1, padx=5, pady=5)

        ttk.Label(root, text="Жанр:").grid(row=1, column=0, padx=5, pady=5)
        self.genre_entry = ttk.Entry(root, width=30)
        self.genre_entry.grid(row=1, column=1, padx=5, pady=5)

        ttk.Label(root, text="Год:").grid(row=2, column=0, padx=5, pady=5)
        self.year_entry = ttk.Entry(root, width=10)
        self.year_entry.grid(row=2, column=1, sticky="w", padx=5, pady=5)

        ttk.Label(root, text="Рейтинг:").grid(row=3, column=0, padx=5, pady=5)
        self.rating_entry = ttk.Entry(root, width=10)
        self.rating_entry.grid(row=3, column=1, sticky="w", padx=5, pady=5)

        # --- Кнопка добавления ---
        ttk.Button(root, text="Добавить фильм", command=self.add_movie).grid(row=4, column=0, columnspan=2, pady=10)

        # --- Таблица ---
        self.columns = ("title", "genre", "year", "rating")
        self.tree = ttk.Treeview(root, columns=self.columns, show="headings")
        for col in self.columns:
            self.tree.heading(col, text=col.capitalize())
            self.tree.column(col, width=120)
        self.tree.grid(row=5, column=0, columnspan=2, padx=5, pady=5, sticky="nsew")
        
        # Заполняем таблицу данными при запуске
        self.update_tree()

        # --- Фильтры ---
        ttk.Label(root, text="Фильтр по жанру:").grid(row=6, column=0, padx=5, pady=5)
        self.filter_genre = ttk.Entry(root, width=20)
        self.filter_genre.grid(row=6, column=1, padx=5, pady=5)
        
        ttk.Label(root, text="Фильтр по году:").grid(row=7, column=0, padx=5, pady=5)
        self.filter_year = ttk.Entry(root, width=10)
        self.filter_year.grid(row=7, column=1, sticky="w", padx=5, pady=5)
        
        # Кнопка фильтрации теперь очищает поля фильтров после применения
        ttk.Button(root, text="Фильтровать", command=self.apply_filters).grid(row=8, column=0, columnspan=2, pady=5)

        # --- Кнопки сохранения/загрузки ---
        ttk.Button(root, text="Сохранить в JSON", command=self.save_data).grid(row=9, column=0, pady=10)
        
        # Кнопка "Сбросить фильтры" для удобства пользователя
        ttk.Button(root, text="Сбросить фильтры", command=self.reset_filters).grid(row=9, column=1, pady=(10, 30))
        
    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year_str = self.year_entry.get().strip()
        rating_str = self.rating_entry.get().strip()

        if not title or not genre or not year_str or not rating_str:
            messagebox.showerror("Ошибка", "Все поля обязательны для заполнения!")
            return

        # --- УЛУЧШЕННАЯ ВАЛИДАЦИЯ ГОДА ---
        if not year_str.isdigit():
            messagebox.showerror("Ошибка", "Год должен быть числом.")
            return
            
        year = int(year_str)
        if not (1895 <= year <= 2026):
            messagebox.showerror("Ошибка", f"Год должен быть в диапазоне от 1895 до 2026.")
            return

         # --- УЛУЧШЕННАЯ ВАЛИДАЦИЯ РЕЙТИНГА ---
        try:
            rating = float(rating_str)
            if not (0 <= rating <= 10):
                raise ValueError("Рейтинг вне диапазона")
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом от 0 до 10.")
            return

        # Если все проверки пройдены
        self.movies.append({
            "title": title,
            "genre": genre,
            "year": year,
            "rating": round(rating, 1) # Округляем для красоты отображения
        })

        self.clear_entries()
        self.update_tree() # Обновляем таблицу после добавления

    def clear_entries(self):
        """Очищает поля ввода."""
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

    def update_tree(self):
        """Полностью обновляет данные в таблице."""
        for i in self.tree.get_children():
            self.tree.delete(i)
        
        # Важно: всегда работаем с исходным списком self.movies
        for movie in self.movies:
            self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))
    
    def apply_filters(self):
         """Применяет фильтры к исходному списку и обновляет таблицу."""
         genre_filter = self.filter_genre.get().strip().lower()
         year_filter = self.filter_year.get().strip()
         
         filtered_movies = self.movies.copy() # Работаем с копией исходного списка

         if genre_filter:
             filtered_movies = [m for m in filtered_movies if genre_filter in m["genre"].lower()]
             
         if year_filter.isdigit():
             filtered_movies = [m for m in filtered_movies if m["year"] == int(year_filter)]
         
         # Обновляем таблицу только отфильтрованными данными
         for i in self.tree.get_children():
             self.tree.delete(i)
         for movie in filtered_movies:
             self.tree.insert("", tk.END, values=(movie["title"], movie["genre"], movie["year"], movie["rating"]))
             
    def reset_filters(self):
         """Сбрасывает фильтры и показывает полный список."""
         self.filter_genre.delete(0, tk.END)
         self.filter_year.delete(0, tk.END)
         self.update_tree() # Показываем все фильмы

    def save_data(self):
         """Сохраняет текущий список фильмов в файл."""
         try:
             with open("data.json", "w", encoding="utf-8") as f:
                 json.dump(self.movies, f, ensure_ascii=False, indent=4)
             messagebox.showinfo("Успех", "Данные сохранены в data.json")
         except Exception as e:
             messagebox.showerror("Ошибка сохранения", f"Не удалось сохранить файл: {e}")

    def load_data(self):
         """Загружает данные из файла при инициализации."""
         if os.path.exists("data.json"):
             try:
                 with open("data.json", "r", encoding="utf-8") as f:
                     self.movies = json.load(f)
             except (json.JSONDecodeError, Exception) as e:
                 messagebox.showerror("Ошибка загрузки", f"Не удалось прочитать файл data.json: {e}")
                 self.movies = [] # На случай ошибки начинаем с пустого списка

    def load_data_gui(self):
         """Загрузка данных по нажатию кнопки (оставлена для совместимости)."""
         self.load_data()
         self.update_tree()
         
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibraryApp(root)
    root.mainloop()
