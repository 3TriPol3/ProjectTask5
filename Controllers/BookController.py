from Models.Book import Book

class BookController:
    '''
    добавить книгу,
    найти по автору/названию,
    выдать книгу,
    вернуть книгу.
    '''

    # Добавить книгу
    @classmethod
    def add(cls, title, author, genre, year, status="доступна"):
        try:
            Book.create(
                title=title,
                author=author,
                genre=genre,
                year=year,
                status=status
            )
        except Exception as item:
            print(f"Ошибка добавления книги: {item}")

    # Получить все книги
    @classmethod
    def get(cls):
        return Book.select()

    # Найти книги по автору
    @classmethod
    def find_by_author(cls, author):
        return Book.select().where(Book.author.contains(author))

    # Найти книги по названию
    @classmethod
    def find_by_title(cls, title):
        return Book.select().where(Book.title.contains(title))

    # Выдать книгу (изменить статус на "выдана")
    @classmethod
    def issue_book(cls, book_id):
        try:
            book = Book.get_by_id(book_id)
            if book.status.strip() == "выдана":
                print("Книга уже выдана.")
            else:
                Book.update(status="выдана").where(Book.id == book_id).execute()
                print(f"Книга '{book.title}' успешно выдана.")
        except Book.DoesNotExist:
            print("Книга с таким ID не найдена.")

    # Вернуть книгу (изменить статус на "доступна")
    @classmethod
    def return_book(cls, book_id):
        try:
            book = Book.get_by_id(book_id)
            if book.status.strip() == "доступна":
                print("Книга уже в библиотеке.")
            else:
                Book.update(status="доступна").where(Book.id == book_id).execute()
                print(f"Книга '{book.title}' успешно возвращена.")
        except Book.DoesNotExist:
            print("Книга с таким ID не найдена.")

    # Удалить пост по - id
    @classmethod
    def delete(cls, id):
        Book.delete_by_id(id)


if __name__ == "__main__":
    # Добавим тестовые данные
    BookController.add(  # Добавить Книгу в таблицу
        title="Мастер и Маргарита",
        author="М. Булгаков",
        genre="Роман",
        year=1966
    )

    # BookController.add("Мастер и Маргарита", "М. Булгаков", "Роман", 1966)
    # BookController.add("Преступление и наказание", "Ф. Достоевский", "Роман", 1866)

    # Вывести все книги
    for item in BookController.get():  # Выводит список записей из таблицы БД
        print(item.title, item.author, item.genre, item.year, item.status)

    # Поиск по автору
    for item in BookController.find_by_author("Булгаков"):
        print(f"'{item.title}' — {item.author}")

    # Выдать книгу
    BookController.issue_book(1)
    # Вернуть книгу
    BookController.return_book(1)