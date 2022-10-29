from django.urls import path
from . import views

urlpatterns = [
     path('', views.home, name='home'),
  path('about/', views.about, name='about'),
  path('heroes/', views.heroes_index, name='index'),
  path('heroes/<int:hero_id>/', views.heroes_detail, name='detail'),
  path('heroes/create/', views.HeroCreate.as_view(), name='heroes_create'),
  path('heroes/<int:pk>/update/', views.HeroUpdate.as_view(), name='heroes_update'),
  path('heroes/<int:pk>/delete/', views.HeroDelete.as_view(), name='heroes_delete'),
  path('heroes/<int:hero_id>/add_battle/', views.add_battle, name='add_battle'),
  path('heroes/<int:hero_id>/assoc_ability/<int:ability_id>/', views.assoc_ability, name='assoc_ability'),
  path('heroes/<int:hero_id>/unassoc_ability/<int:ability_id>/', views.unassoc_ability, name='unassoc_ability'),
  path('heroes/<int:hero_id>/add_photo/', views.add_photo, name='add_photo'),
  path('abilities/', views.AbilityList.as_view(), name='abilities_index'),
  path('abilities/<int:pk>/', views.AbilityDetail.as_view(), name='abilities_detail'),
  path('abilities/create/', views.AbilityCreate.as_view(), name='abilities_create'),
  path('abilities/<int:pk>/update/', views.AbilityUpdate.as_view(), name='abilities_update'),
  path('abilities/<int:pk>/delete/', views.AbilityDelete.as_view(), name='abilities_delete'),
  path('accounts/signup/', views.signup, name='signup')
]
