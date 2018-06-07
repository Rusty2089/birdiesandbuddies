from django import forms
from django.forms import ModelForm
from tourney.models import Profile

GOLFING_CHOICES = (
	(True, 'Golfer'),
	(False, 'Groupie'),
	(None, 'Not Sure'),
)

class NewProfileForm(forms.Form):
	display_name = forms.CharField(label='User Name', max_length=15)
	first_name = forms.CharField(label='First Name', max_length=15)
	last_name = forms.CharField(label='Last Name', max_length=15)
	city = forms.CharField(label='Home City', max_length=30)
	state = forms.CharField(label='Home State', max_length=2)
	isgolfing = forms.ChoiceField(label='Golfer or Groupie', choices=GOLFING_CHOICES, initial=True)
	
class EditProfileForm(forms.ModelForm):
	first_name = forms.CharField(label='First Name', max_length=15)
	last_name = forms.CharField(label='Last Name', max_length=15)
	city = forms.CharField(label='Home City', max_length=30)
	state = forms.CharField(label='Home State', max_length=2)
	isgolfing = forms.ChoiceField(label='Golfer or Groupie', choices=GOLFING_CHOICES)
	
	class Meta:
		model = Profile
		fields = ['first_name', 'last_name', 'city', 'state', 'isgolfing']