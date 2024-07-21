from django.shortcuts import render, redirect, get_object_or_404
from django.core.exceptions import ValidationError

from .models import Books
from .forms import BooksAddForm

'''функция для добавления книги в библиотеку через форму'''


def add_book_web(request: str) -> render:
    '''Функция для добавления книги в библиотеку через веб-форму.'''
    if request.method == 'POST':
        form = BooksAddForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BooksAddForm()
    return render(request, 'add_book.html', {'form': form})


def add_book_console() -> None:
    '''функция для добавления книги в библиотеку через консоль'''
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


def delete_book_web(request: str, book_id: int) -> render:
    '''функция для удаления книги из библиотеки через форму'''
    book = get_object_or_404(Books, id=book_id)
    book.delete()
    return render(request, 'book_list.html')


def delete_book_console() -> None:
    '''функция для удаления книги из библиотеки через консоль'''
    book_id = int(input('Введите ID книги, которую нужно удалить: '))
    try:
        book = Books.objects.get(id=book_id)
        book.delete()
        print(f'Книга с ID "{book_id}" удалена')
    except Exception as e:
        print(f'Произошла ошибка: {e}')
    except Books.DoesNotExist:
        print('Книга с таким ID не существует')


def book_search() -> None:
    '''функция для поиска книги через консоль'''
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


def book_list(request: str) -> render:
    '''функция для вывода списка книг через форму'''
    query = request.GET.get('searсh')
    if query:
        books = Books.objects.filter(title__icontains=query) | Books.objects.filter(
            author__icontains=query) | Books.objects.filter(year__icontains=query)
    else:
        books = Books.objects.all()
    return render(request, 'book_list.html', {'books': books})


def all_books() -> None:
    '''функция для вывода всех книг в консоль'''
    try:
        books_list = Books.objects.all().values()
        for i in books_list:
            print(i, sep='\n')
    except Exception as e:
        print(f'Произошла ошибка: {e}')


'''функция для изменения статуса книги'''


def change_status_web(request: str, book_id: int) -> render:
    '''функция для изменения статуса через форму'''
    book = get_object_or_404(Books, id=book_id)
    if book.status == 'в наличии':
        book.status = 'выдана'
    else:
        book.status = 'в наличии'
    book.save()
    return redirect('book_list')


def change_status_console() -> None:
    '''функция для изменения статуса через консоль'''
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
