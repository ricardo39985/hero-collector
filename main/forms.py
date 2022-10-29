from django.forms import ModelForm
from .models import Battle


class BattleForm(ModelForm):
    class Meta:
        model = Battle
        fields = ['date', 'location']
