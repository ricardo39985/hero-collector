from django.contrib import admin
from .models import Hero, Battle, Ability, Photo

# Register your models here.
admin.site.register(Hero)
admin.site.register(Battle)
admin.site.register(Ability)
admin.site.register(Photo)
