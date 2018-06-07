from django.http import HttpResponseRedirect
from tourney.models import Profile
from django.contrib.auth.models import User


#def profile_complete(function):
#	who = Profile.objects.get
#	if not Profile.objects.filter(user_id=uid).exists():
#		return HttpResponseRedirect('/newprofile/')