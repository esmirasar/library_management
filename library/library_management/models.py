from django.db import models
from django.core.exceptions import ValidationError
from django.utils import timezone


class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    status = models.CharField(max_length=30, default='в наличии')
    '''переопределяю метод clean для проверки введенного года'''

    def clean(self):
        super().clean()
        entered_year = timezone.now().year
        if self.year > entered_year:
            raise ValidationError(f'Год издания не может быть больше текущего года')

    '''переопределяю метод save для перевода всех данных в бд в нижкий регистр, для удобного поиска данных в бд'''

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.author = self.author.lower()
        self.status = self.status.lower()
        super(Books, self).save(*args, **kwargs)
