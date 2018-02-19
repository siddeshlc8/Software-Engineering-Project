from django.db import models

# Create your models here.


class Team(models.Model):
    name = models.CharField(max_length=20, unique=True)
    owner = models.CharField(max_length=20)
    logo = models.ImageField()

    def __str__(self):
        return self.name
