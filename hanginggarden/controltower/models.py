from django.db import models

# Create your models here.
class Article(models.Model):
    created_date = models.DateTimeField(auto_now_add=True)
    content = models.TextField()

class DataPoint(models.Model):
    name = models.CharField(max_length=100)
    value = models.IntegerField()

    def __str__(self):
        return self.name

class SavedData(models.Model):
    date = models.DateField()
    text = models.TextField()
    button_choice = models.CharField(max_length=100)
    images = models.ManyToManyField('Image', blank=True)

class Image(models.Model):
    image = models.ImageField(upload_to='images/')