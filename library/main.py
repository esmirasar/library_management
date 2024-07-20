import os
import django

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'library.settings')

django.setup()

from library_management.views import add_book, delete_book, book_search, all_books, change_status


def main_loop():
    while True:
        print("\nБиблиотечное приложение")
        print("1. Добавить книгу")
        print("2. Удалить книгу")
        print("3. Поиск книги")
        print("4. Отобразить все книги")
        print("5. Изменить статус книги")
        print("6. Выйти")
        choice = input("Выберите действие: ")

        if choice == '1':
            add_book()
        elif choice == '2':
            delete_book()
        elif choice == '3':
            book_search()
        elif choice == '4':
            all_books()
        elif choice == '5':
            change_status()

        if choice == '6':
            break


if __name__ == "__main__":
    main_loop()
