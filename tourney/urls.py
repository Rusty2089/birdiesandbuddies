from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
	path('main/', views.main, name='main'),
	path('leaderboard/', views.leaderboard, name='leaderboard'),
	path('scorecards/', views.scorecards, name='scorecards'),
	path('tourneyinfo/', views.tourneyinfo, name='tourneyinfo'),
	path('enterscores/', views.enterscores, name='enterscores'),
	path('newprofile/', views.new_profile, name='newprofile'),
	path('editprofile/', views.edit_profile, name='editprofile'),
]