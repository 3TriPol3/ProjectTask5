from tkinter import *
from tkinter import ttk

from Controllers.BookController import BookController


class BookView(Tk):
    def __init__(self):
        super().__init__()

        # Атрибуты окна
        self.title("Система учета книг")
        self.geometry("1280x750")

        # Фрейм Добавить книгу
        self.add_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[18])
        self.add_frame.pack(anchor=CENTER, fill=X, padx=10, pady=10)

        # Заголовок "Добавить книгу"
        self.add_title_frame = ttk.Frame(self.add_frame, relief=SOLID, borderwidth=1, padding=[8, 10])
        self.add_title_frame.pack(anchor=CENTER, fill=X, padx=10, pady=10)
        self.add_title = ttk.Label(self.add_title_frame, text="Добавить Книгу")
        self.add_title.pack()

        # Поля ввода
        self.add_input_frame = ttk.Frame(self.add_frame, relief=SOLID, borderwidth=1, padding=[8, 10])
        self.add_input_frame.pack(fill=X, padx=10, pady=10)

        # Метки и поля ввода
        ttk.Label(self.add_input_frame, text="Название").grid(row=0, column=0, sticky="nsew", padx=5, pady=5)
        ttk.Label(self.add_input_frame, text="Автор").grid(row=0, column=1, sticky="nsew", padx=5, pady=5)
        ttk.Label(self.add_input_frame, text="Жанр").grid(row=0, column=2, sticky="nsew", padx=5, pady=5)
        ttk.Label(self.add_input_frame, text="Год издания").grid(row=0, column=3, sticky="nsew", padx=5, pady=5)

        self.add_title_entry = ttk.Entry(self.add_input_frame)
        self.add_title_entry.grid(row=1, column=0, sticky="nsew", padx=5, pady=5)

        self.add_author_entry = ttk.Entry(self.add_input_frame)
        self.add_author_entry.grid(row=1, column=1, sticky="nsew", padx=5, pady=5)

        self.add_genre_entry = ttk.Entry(self.add_input_frame)
        self.add_genre_entry.grid(row=1, column=2, sticky="nsew", padx=5, pady=5)

        self.add_year_entry = ttk.Entry(self.add_input_frame)
        self.add_year_entry.grid(row=1, column=3, sticky="nsew", padx=5, pady=5)

        # Кнопка добавления книги
        self.add_button = ttk.Button(self.add_input_frame, text="Добавить книгу", command=self.add_book)
        self.add_button.grid(row=1, column=4, sticky="nsew", padx=5, pady=5)

        # Фрейм Поиск книги
        self.search_frame = ttk.Frame(self, borderwidth=1, relief=SOLID, padding=[18])
        self.search_frame.pack(anchor=CENTER, fill=X, padx=10, pady=10)

        self.search_label = ttk.Label(self.search_frame, text="Поиск по автору или названию:")
        self.search_label.grid(row=0, column=0, padx=5, pady=5, sticky="w")

        self.search_entry = ttk.Entry(self.search_frame, width=40)
        self.search_entry.grid(row=0, column=1, padx=5, pady=5)

        self.search_button = ttk.Button(self.search_frame, text="Найти", command=self.search_books)
        self.search_button.grid(row=0, column=2, padx=5, pady=5)

        self.reset_button = ttk.Button(self.search_frame, text="Показать все", command=self.reset_view)
        self.reset_button.grid(row=0, column=3, padx=5, pady=5)

        # Фрейм Таблицы
        self.table_frame = ttk.Frame(self, padding=[20])
        self.table_frame.pack(anchor=CENTER, pady=10, padx=10)

        # Таблица
        self.columns = ('id', 'title', 'author', 'genre', 'year', 'status')
        self.table_data = ttk.Treeview(self.table_frame, columns=self.columns, show='headings')

        # Заголовки таблицы
        self.table_data.heading('id', text="ID")
        self.table_data.heading('title', text='Название')
        self.table_data.heading('author', text='Автор')
        self.table_data.heading('genre', text='Жанр')
        self.table_data.heading('year', text='Год издания')
        self.table_data.heading('status', text='Статус')

        self.table_data.column('id', width=50)
        self.table_data.column('title', width=200)
        self.table_data.column('author', width=150)
        self.table_data.column('genre', width=120)
        self.table_data.column('year', width=100)
        self.table_data.column('status', width=100)

        # Событие выбора строки
        self.table_data.bind("<<TreeviewSelect>>", self.row_selected)
        self.table()

        self.table_data.pack(fill=BOTH, expand=True)

        # Фрейм управления статусом книги
        self.action_frame = ttk.Frame(self, padding=[10])
        self.action_frame.pack(anchor=CENTER, pady=10)

        self.issue_button = ttk.Button(self.action_frame, text="Выдать книгу", command=self.issue_book)
        self.issue_button.grid(row=0, column=0, padx=10)

        self.return_button = ttk.Button(self.action_frame, text="Вернуть книгу", command=self.return_book)
        self.return_button.grid(row=0, column=1, padx=10)

        # Переменная для хранения ID выбранной книги
        self.selected_id = None

    # Обновление данных в таблице
    def table(self):
        for item in self.table_data.get_children():
            self.table_data.delete(item)

        for book in BookController.get_all():
            self.table_data.insert("", END, values=(
                book.id,
                book.title,
                book.author,
                book.genre,
                book.year,
                book.status
            ))

    # Добавление новой книги
    def add_book(self):
        title = self.add_title_entry.get().strip()
        author = self.add_author_entry.get().strip()
        genre = self.add_genre_entry.get().strip()
        year_str = self.add_year_entry.get().strip()

        if not all([title, author, genre, year_str]):
            return

        try:
            year = int(year_str)
            BookController.add(title=title, author=author, genre=genre, year=year)
            self.reset_view()
            self.clear_add_fields()
        except ValueError:
            pass

    # Поиск книги по автору или названию
    def search_books(self):
        query = self.search_entry.get().strip()
        if not query:
            self.reset_view()
            return

        # Очистка таблицы
        for item in self.table_data.get_children():
            self.table_data.delete(item)

        # Поиск по автору и названию
        books_by_author = BookController.find_by_author(query)
        books_by_title = BookController.find_by_title(query)

        seen_ids = set()
        for book in list(books_by_author) + list(books_by_title):
            if book.id not in seen_ids:
                self.table_data.insert("", END, values=(
                    book.id,
                    book.title,
                    book.author,
                    book.genre,
                    book.year,
                    book.status
                ))
                seen_ids.add(book.id)

    # Сброс фильтра и отображение всех книг
    def reset_view(self):
        self.search_entry.delete(0, END)
        self.table()

    # Очистка полей ввода при добавлении книги
    def clear_add_fields(self):
        self.add_title_entry.delete(0, END)
        self.add_author_entry.delete(0, END)
        self.add_genre_entry.delete(0, END)
        self.add_year_entry.delete(0, END)

    # Обработка выбора строки в таблице
    def row_selected(self, event):
        selected = self.table_data.selection()
        if not selected:
            return
        self.selected_id = self.table_data.item(selected[0], "values")[0]

    # Выдать книгу (изменить статус на 'выдана')
    def issue_book(self):
        if self.selected_id is None:
            return
        BookController.issue_book(self.selected_id)
        self.reset_view()
        self.selected_id = None

    # Вернуть книгу (изменить статус на 'доступна')
    def return_book(self):
        if self.selected_id is None:
            return
        BookController.return_book(self.selected_id)
        self.reset_view()
        self.selected_id = None

if __name__ == "__main__":
    app = BookView()
    app.mainloop()