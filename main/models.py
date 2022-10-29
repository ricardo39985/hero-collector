from django.db import models
from django.urls import reverse
from datetime import date
from django.contrib.auth.models import User

LOCATIONS = (
    ('B', 'Earth'),
    ('L', 'Apocalypse'),
    ('D', 'Asgard'),
)

# Create your models here.


class Ability(models.Model):
    power = models.CharField(max_length=50)
    level = models.IntegerField()

    def __str__(self):
        return self.power

    def get_absolute_url(self):
        return reverse('abilitiess_detail', kwargs={'pk': self.id})


class Hero(models.Model):
    name = models.CharField(max_length=100)
    universe = models.CharField(max_length=100)
    description = models.TextField(max_length=250)
    abilities = models.ManyToManyField(Ability)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

    def __str__(self):
        return f'{self.name} ({self.id})'

    def get_absolute_url(self):
        return reverse('detail', kwargs={'hero_id': self.id})

    def fought_today(self):
        return self.battle_set.filter(date=date.today()).count() >= len(LOCATIONS)


class Battle(models.Model):
    date = models.DateField('Battle Date')
    location = models.CharField(
        max_length=1,
        choices=LOCATIONS,
        default=LOCATIONS[0][0]
    )

    hero = models.ForeignKey(
        Hero,
        on_delete=models.CASCADE
    )

    def __str__(self):
        return f'{self.location()} on {self.date}'

    class Meta:
        ordering = ['-date']


class Photo(models.Model):
    url = models.CharField(max_length=200)
    hero = models.ForeignKey(Hero, on_delete=models.CASCADE)

    def __str__(self):
        return f"Photo for hero_id: {self.hero_id} @{self.url}"
