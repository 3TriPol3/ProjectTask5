from Models.Base import *

class Book(BaseModel):
    '''
    Данный класс описывает таблицу в БД с книгами
    '''
    id = PrimaryKeyField() # id
    title = CharField() # Название
    author = CharField() # Автор
    genre = CharField() # Жанр
    year = IntegerField() # Год
    status = CharField() # Статус

if __name__ == "__main__":
    mysql_db.create_tables([Book])