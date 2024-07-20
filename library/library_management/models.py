from django.db import models


class Books(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    year = models.IntegerField()
    status = models.CharField(max_length=30)

    def save(self, *args, **kwargs):
        self.title = self.title.lower()
        self.author = self.author.lower()
        self.status = self.status.lower()
        super(Books, self).save(*args, **kwargs)