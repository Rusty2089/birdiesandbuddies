from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.db import IntegrityError

from tourney.forms import NewProfileForm, EditProfileForm
from tourney.models import Profile

from django.contrib.auth.decorators import login_required
#from tourney.decorators import profile_complete

@login_required
def new_profile(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = NewProfileForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			try:
				u1 = Profile(
					user_id=request.user.username,
					display_name=request.POST['display_name'],
					first_name=request.POST['first_name'],
					last_name=request.POST['last_name'],
					city=request.POST['city'],
					state=request.POST['state'],
					email=request.POST['email'],
				)
				u1.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/editprofile/')
			except IntegrityError as e:
				return render(request, 'tourney/newprofile.html', {'form': form, 'message': 'Sorry, please try another User Name.'})
	# if a GET (or any other method) we'll create a blank form
	else:
		form = NewProfileForm()
		return render(request, 'tourney/newprofile.html', {'form': form})

@login_required
def edit_profile(request):
	uname = request.user.username
	instance = Profile.objects.get(user_id = uname)
	form = EditProfileForm(request.POST or None, initial={'first_name':instance.first_name, 'last_name':instance.last_name, 'city':instance.city, 'state':instance.state, 'isgolfing':instance.isgolfing})
	if request.method == 'POST':
		if form.is_valid():
			
			instance.first_name=request.POST['first_name']
			instance.last_name=request.POST['last_name']
			instance.city=request.POST['city']
			instance.state=request.POST['state']
			instance.isgolfing=request.POST['isgolfing']
			
			instance.save()
		# redirect to a new URL:
		return HttpResponseRedirect('/editprofile/')

	# if a GET (or any other method) we'll create a blank form
	dname = instance.display_name
	return render(request, 'tourney/editprofile.html', {'form': form, 'username': dname})


