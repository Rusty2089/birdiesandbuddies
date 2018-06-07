from django.shortcuts import render
from django.http import HttpResponseRedirect

from tourney.forms import UserForm
from tourney.models import Profile

from django.contrib.auth.decorators import login_required, user_passes_test
#from tourney.decorators import profile_complete


@login_required
def profile_view(request):
    user = request.user
    form = EditProfileForm(initial={'first_name':user.first_name, 'last_name':user.last_name})
    context = {
        "form": form
    }
    return render(request, 'profile.html', context)

def edit_profile(request):

    user = request.user
    form = EditProfileForm(request.POST or None, initial={'first_name':user.first_name, 'last_name':user.last_name})
    if request.method == 'POST':
        if form.is_valid():


            user.first_name = request.POST['first_name']
            user.last_name = request.POST['last_name']

            user.save()
            return HttpResponseRedirect('%s'%(reverse('profile')))

    context = {
        "form": form
    }

    return render(request, "edit_profile.html", context)


def new_user_form(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		# check whether it's valid:
		if form.is_valid():
			u1 = Profile(
				user_id=request.user.id,
				display_name=request.POST['dislpay_name'],
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


@login_required
#@profile_complete
def profile_user_form(request):
	# if this is a POST request we need to process the form data
	args = {}
	if request.method == 'POST':
		# create a form instance and populate it with data from the request:
		form = UserForm(request.POST)
		# check whether it's valid:
		if form.is_valid(): #and form.clean_username():
			u1 = Profile(
				user_id=request.user.id,
				display_name=request.POST['display_name'],
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
