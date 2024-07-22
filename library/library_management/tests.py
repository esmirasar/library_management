from io import StringIO
from django.core.management import call_command
from django.test import TestCase, Client
from django.urls import reverse
from .forms import BooksAddForm
from .models import Books


class AddBookWebTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.url = reverse('add_book')

    def test_add_book_web_get(self):
        '''проверка get-запроса. Т.е что get возвращает корректный Http-статус и использует правильный шаблон и форму'''
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'add_book.html')
        self.assertIsInstance(response.context['form'], BooksAddForm)

    def test_add_book_web_post(self):
        ''' Проверка на то, что POST-запрос корректно сохраняет данные в бд '''

        data = {
            'title': 'Test_Book',
            'author': 'Test_Author',
            'year': 2000
        }
        response = self.client.post(self.url, data)
        self.assertRedirects(response, reverse('book_list'))
        self.assertTrue(Books.objects.filter(title='test_book').exists())


class DeleteBookWebTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Books.objects.create(title='Test_Book', author='Test_Author', year=2021)
        self.url = reverse('delete_book', args=[self.book.id])

    def test_delete_book_web(self):
        '''проверка на то, что функция корректно удаляет книгу из бд'''
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('book_list'))
        self.assertFalse(Books.objects.filter(id=self.book.id).exists())


class ChangeStatusWebTestCase(TestCase):
    def setUp(self):
        self.client = Client()
        self.book = Books.objects.create(title='Test_Book', author='Test_Author', year=2021)
        self.url = reverse('change_status', args=[self.book.id])

    def test_change_status_web(self):
        '''проверка на то, что функция меняет статус книги'''
        response = self.client.post(self.url)
        self.assertRedirects(response, reverse('book_list'))
        self.book.refresh_from_db()
        self.assertEqual(self.book.status, 'выдана')
