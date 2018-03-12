from django.contrib import admin
from .models import Tournament, Team,Match,Score, ScoreCard

# Register your models here.

admin.site.register(Tournament)
admin.site.register(Team)
admin.site.register(Match)
admin.site.register(Score)
admin.site.register(ScoreCard)