from django.urls import path

from . import views

urlpatterns = [
    path('', views.main, name='main'),
	path('main/', views.main, name='main'),
	path('leaderboard/', views.leaderboard, name='leaderboard'),
	path('scorecards/', views.scorecards, name='scorecards'),
	path('tourneyinfo/', views.tourneyinfo, name='tourneyinfo'),
	path('enterscores/', views.enterscores, name='enterscores'),
	# ex: /5/
    path('<int:hole_id>/', views.changeholes, name='changeholes'),
	path('newprofile/', views.new_profile, name='newprofile'),
	path('editprofile/', views.edit_profile, name='editprofile'),
	path('compile/', views.compile, name='compile'),
	path('reversecompile/', views.reverse_compile, name='reversecompile'),
	path('delete_daily/', views.delete_daily, name='delete_daily'),
	path('golfers_daily/', views.golfers_daily, name='golfers_daily'),
	path('groups_daily/', views.groups_daily, name='groups_daily'),
	path('reunion/', views.reunion, name='reunion'),

]