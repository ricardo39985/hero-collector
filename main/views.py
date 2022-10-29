from django.shortcuts import render, redirect
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.views.generic import ListView, DetailView
from django.contrib.auth import login
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from .models import Hero, Ability, Photo
from .forms import BattleForm
import uuid
import boto3
import os

# Create your views here.


def home(request):
    return render(request, 'home.html')


def about(request):
    return render(request, 'about.html')


@login_required
def heroes_index(request):
    heroes = Hero.objects.filter(user=request.user)
    return render(request, 'heroes/index.html', {
        'heroes': heroes
    })


@login_required
def heroes_detail(request, hero_id):
    hero = Hero.objects.get(id=hero_id)
    id_list = hero.abilities.all().values_list('id')
    abilities_that_hero_doesnt_have = Ability.objects.exclude(id__in=id_list)
    battle_form = BattleForm()
    return render(
        request,
        'heroes/detail.html',
        {
            'hero': hero,
            'battle_form': battle_form,
            'abilities': abilities_that_hero_doesnt_have
        }
    )


class HeroCreate(LoginRequiredMixin, CreateView):
    model = Hero
    fields = ['name', 'universe', 'description']
    def form_valid(self, form):
        print(self.__dict__)
        form.instance.user = self.request.user
        return super().form_valid(form)


class HeroUpdate(LoginRequiredMixin, UpdateView):
    model = Hero
    fields = ['universe', 'description']


class HeroDelete(LoginRequiredMixin, DeleteView):
    model = Hero
    success_url = '/heroes/'


@login_required
def add_battle(request, hero_id):
    form = BattleForm(request.POST)
    if form.is_valid():
        new_battle = form.save(commit=False)
        new_battle.hero_id = hero_id
        new_battle.save()
    return redirect('detail', hero_id=hero_id)


@login_required
def assoc_ability(request, hero_id, ability_id):
    Hero.objects.get(id=hero_id).abilities.add(ability_id)
    return redirect('detail', hero_id=hero_id)


@login_required
def unassoc_ability(request, hero_id, toy_id):
  Hero.objects.get(id=hero_id).abilities.remove(toy_id)
  return redirect('detail', hero_id=hero_id)

class AbilityList(LoginRequiredMixin, ListView):
    model = Ability


class AbilityDetail(LoginRequiredMixin, DetailView):
    model = Ability


class AbilityCreate(LoginRequiredMixin, CreateView):
    model = Ability
    fields = '__all__'


class AbilityUpdate(LoginRequiredMixin, UpdateView):
    model = Ability
    fields = ['name', 'level']


class AbilityDelete(LoginRequiredMixin, DeleteView):
    model = Ability
    success_url = '/abilities/'


@login_required
def add_photo(request, hero_id):
    photo_file = request.FILES.get('photo-file', None)
    if photo_file:
        s3 = boto3.client('s3')
        key = uuid.uuid4().hex[:6] + \
            photo_file.name[photo_file.name.rfind('.'):]
        try:
            bucket = os.environ['S3_BUCKET']
            s3.upload_fileobj(photo_file, bucket, key)
            url = f"{os.environ['S3_BASE_URL']}{bucket}/{key}"
            Photo.objects.create(url=url, hero_id=hero_id)
        except Exception as e:
            print('An error occured uploading file to S3')
            print(e)
    return redirect('detail', hero_id=hero_id)


def signup(request):
    error_message = ''
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            return redirect('index')
        else:
            error_message = 'Invalid sign up - try again'
    form = UserCreationForm()
    context = {'form': form, 'error_message': error_message}
    return render(request, 'registration/signup.html', context)
