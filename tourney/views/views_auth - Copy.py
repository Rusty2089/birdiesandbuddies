from django.shortcuts import render
from django.http import HttpResponseRedirect

from tourney.forms import UserForm
from tourney.models import User

def main(request):
	if request.user.is_authenticated:
		uid = request.user.id
		#uid = request.user.username
		
		return render(request, 'tourney/index.html', {'uid': uid})
	else:
		return render(request, 'tourney/login.html', {})
	
def leaderboard(request):
	if request.user.is_authenticated:
		return render(request, 'tourney/leaderboard.html', {})
	else:
		return render(request, 'tourney/login.html', {})
		
def scorecards(request):
	if request.user.is_authenticated:
		return render(request, 'tourney/scorecards.html', {})
	else:
		return render(request, 'tourney/login.html', {})
		
def tourneyinfo(request):
	if request.user.is_authenticated:
		return render(request, 'tourney/tourneyinfo.html', {})
	else:
		return render(request, 'tourney/login.html', {})
		
def enterscores(request):
	if request.user.is_authenticated:
		return render(request, 'tourney/enterscores.html', {})
	else:
		return render(request, 'tourney/login.html', {})


		
def new_user_form(request):
	if request.user.is_authenticated:
		# if this is a POST request we need to process the form data
		if request.method == 'POST':
			# create a form instance and populate it with data from the request:
			form = UserForm(request.POST)
			# check whether it's valid:
			if form.is_valid():
				u1 = User(
					user_id=request.user.id,
					user_name=request.POST['user_name'],
					first_name=request.POST['first_name'],
					last_name=request.POST['last_name'],
					city=request.POST['city'],
					state=request.POST['state'],
					isgolfing=request.POST['isgolfing'],
				)
				u1.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/profile/')

		# if a GET (or any other method) we'll create a blank form
		else:
			form = UserForm()

		return render(request, 'tourney/newuser.html', {'form': form})
		
	else:
		return render(request, 'tourney/login.html', {})
		
		
def profile_user_form(request):
	if request.user.is_authenticated:
		# if this is a POST request we need to process the form data
		args = {}
		if request.method == 'POST':
			# create a form instance and populate it with data from the request:
			form = UserForm(request.POST)
			# check whether it's valid:
			if form.is_valid(): #and form.clean_username():
				u1 = User(
					user_id=request.user.id,
					user_name=request.POST['user_name'],
					first_name=request.POST['first_name'],
					last_name=request.POST['last_name'],
					city=request.POST['city'],
					state=request.POST['state'],
					isgolfing=request.POST['isgolfing'],
				)
				u1.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/profile/')

		# if a GET (or any other method) we'll create a blank form
		else:
			form = UserForm()
		
		args['form'] = form
		return render(request, 'tourney/profile.html', args)
		
	else:
		return render(request, 'tourney/login.html', {})