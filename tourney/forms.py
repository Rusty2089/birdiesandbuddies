from django import forms
from django.forms import ModelForm
from tourney.models import Profile, Daily, Message

GOLFING_CHOICES = (
	(True, 'Golfer'),
	(False, 'Groupie'),
	(None, 'Not Sure'),
)

SCORE_CHOICES = (
	('', 'Blank'),
	(0, 'Aweful (0)'),
	(1, 'Bogey (1pt)'),
	(2, 'Par (2pts)'),
	(4, 'Birdie (4pts)'),
	(8, 'Eagle (8pts)'),
	(10, '2x Eagle (10pts)'),
)

HOLE_CHOICES = (
	(1, 'Hole 1'),
	(2, 'Hole 2'),
	(3, 'Hole 3'),
	(4, 'Hole 4'),
	(5, 'Hole 5'),
	(6, 'Hole 6'),
	(7, 'Hole 7'),
	(8, 'Hole 8'),
	(9, 'Hole 9'),
	(10, 'Hole 10'),
	(11, 'Hole 11'),
	(12, 'Hole 12'),
	(13, 'Hole 13'),
	(14, 'Hole 14'),
	(15, 'Hole 15'),
	(16, 'Hole 16'),
	(17, 'Hole 17'),
	(18, 'Hole 18'),
)

class NewProfileForm(forms.Form):
	display_name = forms.CharField(label='User Name', max_length=20)
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
		
class EnterScoreForm(forms.Form):
	g1_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	g2_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	g3_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	g4_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	#hole_pass = forms.CharField(disabled=True)

	#class Meta:
		#model = Daily
		#fields = ['golfer', 'hole']
		
class MessageForm(forms.ModelForm):
	message = forms.CharField(label='Message', max_length = 200)
	
	class Meta:
		model = Message
		fields = ['message']