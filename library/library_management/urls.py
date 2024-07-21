from django.contrib import admin
from django.views.generic import TemplateView
from django.urls import path
from .views import add_book_web, delete_book_web, book_list

urlpatterns = [
    path('', add_book_web, name='add_book'),
    path('delete/<int:book_id>', delete_book_web, name="delete_book"),
    path('book_list/', book_list, name='book_list'),
    path('ok/', TemplateView.as_view(template_name='success_page.html'), name='success_page'),


]
