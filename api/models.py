from django.db import models

# Create your models here.


class Author(models.Model):
    name = models.CharField(max_length=200)
    contry = models.CharField(max_length=400)
    age = models.IntegerField()


class Books(models.Model):
    name = models.CharField(max_length=200)
    published_year = models.IntegerField()
    pages = models.IntegerField()
    author = models.ForeignKey(Author, on_delete=models.CASCADE)
    price = models.IntegerField()

    def __str__(self):
        return self.name + " " + self.author
