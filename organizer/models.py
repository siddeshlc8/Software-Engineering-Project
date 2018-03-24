from django.db import models
from django.contrib.auth.models import User
# Create your models here.

class Organizer(User):
    nationality=models.CharField(max_length=20, null=True, blank=True)
    state=models.CharField(max_length=20, null=True, blank=True)
    phone_no = models.CharField(max_length=12, null=True, blank=True)

    def profile(self):
        value = {
            'First Name': getattr(self, 'first_name'),
            'Last Name': getattr(self, 'last_name'),
            'Phone Number': getattr(self, 'phone_no'),
            'Email Address': getattr(self, 'email'),
            'Nationality': getattr(self, 'nationality'),
            'State': getattr(self, 'state'),
                 }
        return value


