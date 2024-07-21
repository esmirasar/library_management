from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import Books
from .forms import BooksAddForm

'''функция для добавления книги в библиотеку через форму'''


def add_book_web(request):
    if request.method == 'POST':
        form = BooksAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')  # Перенаправление на страницу успешного добавления
    else:
        form = BooksAddForm()
    return render(request, 'add_book.html', {'form': form})


'''функция для добавления книги в библиотеку через консоль'''


def add_book_console():
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
        print(f'Книга успешно добавлена в библиотеку!')
    except ValueError:
        print("Кажется одно из полей некорректно")
    except Exception as e:
        print(f'Произошла ошибка: {e}')


'''функция для удаления книги из библиотеки через форму'''


def delete_book_web(request, book_id):
    book = get_object_or_404(Books, id=book_id)
    book.delete()
    return render(request, 'book_list.html')


'''функция для удаления книги из библиотеки через консоль'''


def delete_book_console():
    book_id = int(input('Введите ID книги, которую нужно удалить: '))
    try:
        book = Books.objects.get(id=book_id)
        book.delete()
        print(f'Книга с ID "{book_id}" удалена')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
    except Books.DoesNotExist:
        print('Книга с таким ID не существует')


'''функция для поиска книги в библиотеке'''


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


'''функция для вывода всех книг через форму'''


def book_list(request):
    books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})


'''функция для вывода всех книг в консоль'''


def all_books():
    try:
        books_list = Books.objects.all().values()
        for i in books_list:
            print(i, sep='\n')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


'''функция для изменения статуса книги'''


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
