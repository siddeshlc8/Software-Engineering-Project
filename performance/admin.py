from django.contrib import admin
from .models import PerformanceTotal, PerformanceMatchWise

# Register your models here.

admin.site.register(PerformanceTotal)
admin.site.register(PerformanceMatchWise)