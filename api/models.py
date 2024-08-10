from django.db import models

# Create your models here.


class Books(models.Model):
    name = models.CharField(max_length=200)
    published_year = models.IntegerField()
    pages = models.IntegerField()
    author = models.CharField(max_length=200)
    price = models.IntegerField()

    def __str__(self):
        return self.name + " " + self.author
