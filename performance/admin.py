from django.contrib import admin
from .models import PerformanceTotal, BattingInnings, BowlingInnings

# Register your models here.

admin.site.register(PerformanceTotal)
admin.site.register(BattingInnings)
admin.site.register(BowlingInnings)