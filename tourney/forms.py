from django import forms
from django.forms import ModelForm
from multiselectfield import MultiSelectFormField
from tourney.models import Profile, Daily, Message, Light

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

ROUND_CHOICES = (
	('r1', 'Round 1'),
	('r2', 'Round 2'),
	('r3', 'Round 3'),
)

COURSE_CHOICES = (
	('Nicklaus', 'Nicklaus'),
	('Palmer', 'Palmer'),
	('Copperhead', 'Copperhead'),
	('Island', 'Island'),
	('North', 'North'),
    ('South', 'South'),
	('Ocean', 'Ocean'),
	('Conservatory', 'Conservatory'),
	('Las Colinas', 'Las Colinas'),
	('El Campeon', 'El Campeon'),
	('International', 'International')
)

COLOR_CHOICES = (
	('White', 'White'),
	('Red', 'Red'),
	('Orange', 'Orange'),
	('Yellow', 'Yellow'),
	('Green', 'Green'),
	('Blue', 'Blue'), 
	('Purple', 'Purple')
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
	def __init__(self, extra_list, *args, **kwargs): #NEW
		super(EnterScoreForm, self).__init__(*args, **kwargs) #NEW
		self.fields['extra_names'] = forms.ChoiceField(choices=extra_list) #NEW
	
	g1_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	g2_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	g3_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
	g4_score = forms.ChoiceField(label='Score', choices=SCORE_CHOICES)
			
class MessageForm(forms.ModelForm):
	message = forms.CharField(label='Message', max_length = 200)
	
	class Meta:
		model = Message
		fields = ['message']
		
		
		
class CompileForm(forms.Form):
	round = forms.ChoiceField(label='Round to setup: ', choices=ROUND_CHOICES)
	course = forms.ChoiceField(label='Course: ', choices=COURSE_CHOICES)
    #tees = forms.CharField(label='Tee Color', max_length=15)
	g1_tt = forms.TimeField(label='Group 1 Tee Time: ')
	g2_tt = forms.TimeField(label='Group 2 Tee Time: ')
	g3_tt = forms.TimeField(label='Group 3 Tee Time: ')
	g4_tt = forms.TimeField(label='Group 4 Tee Time: ')
	g5_tt = forms.TimeField(label='Group 5 Tee Time: ')
	g6_tt = forms.TimeField(label='Group 6 Tee Time: ')
	g7_tt = forms.TimeField(label='Group 7 Tee Time: ')
	
class ReverseCompileForm(forms.Form):
	round = forms.ChoiceField(label='Round to save: ', choices=ROUND_CHOICES)
	
class LightsForm(forms.ModelForm):
	creator = forms.CharField(label='Your Name', max_length=15)
	RoofColors = forms.MultipleChoiceField(label='Roof Line',choices=COLOR_CHOICES, widget=forms.CheckboxSelectMultiple)
	PalmColors = forms.MultipleChoiceField(label='Tree Trunks',choices=COLOR_CHOICES, widget=forms.CheckboxSelectMultiple)
	FloodColors = forms.ChoiceField(label='Flood Lights', choices=COLOR_CHOICES)
	SconceColors = forms.ChoiceField(label='Sconces', choices=COLOR_CHOICES)
	StripePalmColor = forms.ChoiceField(label='Candy Cane Palm', choices=COLOR_CHOICES)
	GarageFrameColors = forms.MultipleChoiceField(label= 'Garage Frames',choices=COLOR_CHOICES, widget=forms.CheckboxSelectMultiple) 
	SnowFlakeColors = forms.MultipleChoiceField(label='Snow Flakes',choices=COLOR_CHOICES, widget=forms.CheckboxSelectMultiple)
	
	class Meta:
		model = Light
		fields = ['creator', 'RoofColors', 'PalmColors', 'FloodColors', 'SconceColors', 'StripePalmColor', 'GarageFrameColors', 'SnowFlakeColors']