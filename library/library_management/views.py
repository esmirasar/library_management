from django.shortcuts import render
from django.core.exceptions import ValidationError
from .models import Books


def add_book():
    title = input('Введите название книги: ')
    author = input('Введите автора книги: ')
    year = int(input("Введите год издания: "))
    try:
        title = input('Введите название книги: ')
        author = input('Введите автора книги: ')
        year = int(input("Введите год издания: "))
        new_book = Books(title=title,
                         author=author,
                         year=year,
                         status='в наличии')

        new_book.full_clean()
        new_book.save()
        print(f'Книга успешно добавлена в библиотеку и хранится с ID: {new_book.id}')
    except ValueError:
        print("Кажется одно из полей некорректно")
    except ValidationError:
        print("Ошибка валидации")
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def delete_book():
    book_id = int(input('Введите ID книги, которую нужно удалить: '))
    try:
        book = Books.objects.get(id=book_id)
        book.delete()
        print(f'Книга с ID "{book_id}" удалена')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
    except Books.DoesNotExist:
        print('Книга с таким ID не существует')


def book_search():
    print("Вы можете искать книги по таким параметрам, как:",
          "1.Title", "2.Author", "3.Year", sep='\n')
    try:
        number = int(input("Введите номер нужного параметра для поиска:"))
        parameter = input("Введите сам параметр: ")
        if number == 1:
            books_list = Books.objects.filter(title=parameter.lower()).values()
        elif number == 2:
            books_list = Books.objects.filter(author=parameter.lower()).values()
        elif number == 3:
            books_list = Books.objects.filter(year=int(parameter)).values()
        else:
            print("Неверный номер параметра.")
            return

        if books_list:
            for book in books_list:
                print(book)
        else:
            print("Книги с такими параметрами не найдены.")

    except ValueError as e:
        print(f'Произошла ошибка: {e}')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def all_books():
    try:
        books_list = Books.objects.all().values()
        for i in books_list:
            print(i, sep='\n')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


def change_status():
    try:
        print("Доступные статусы:", "1. В наличии", "2. Выдана")
        book_id = int(input('Введите ID книги, статус которой нужно сменить: '))
        new_status = int(input('Введите номер нового статуса: '))
        book = Books.objects.get(id=book_id)
        if new_status == 1:
            book.status = "В наличии"
        elif new_status == 2:
            book.status = "Выдана"
        book.save()
        print(f'Статус книги изменен на "{book.status}"')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
    except Books.DoesNotExist:
        print('Книга с таким ID не существует')
