from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Organizer(User):
    nationality=models.CharField(max_length=20)
    state=models.CharField(max_length=20)
    phone_no = models.CharField(max_length=12)

