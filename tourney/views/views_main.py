from django.shortcuts import render
from django.http import HttpResponseRedirect
from tourney.models import Profile

from django.contrib.auth.decorators import login_required


@login_required
def leaderboard(request):
	return render(request, 'tourney/leaderboard.html', {})

@login_required
def scorecards(request):
	return render(request, 'tourney/scorecards.html', {})

@login_required
def tourneyinfo(request):
	queryset=Profile.objects.all()
	golfers=queryset.filter(isgolfing=True)
	golferDict = {}
	for g in golfers:
		valueDict = {}
		valueDict['name'] = g.first_name + ' ' + g.last_name
		valueDict['aka'] = g.display_name
		valueDict['hometown'] = g.city + ', ' + g.state
		golferDict[g.display_name] = valueDict
	
	groupies=queryset.filter(isgolfing=False)
	groupieDict = {}
	for g in groupies:
		valueDict = {}
		valueDict['name'] = g.first_name + ' ' + g.last_name
		valueDict['aka'] = g.display_name
		valueDict['hometown'] = g.city + ', ' + g.state
		groupieDict[g.display_name] = valueDict
	
	content = {'golfers': golferDict, 'groupies': groupieDict}
	#print(content) <--can print and view in logs for troubleshooting
	return render(request, 'tourney/tourneyinfo.html', content)
	

@login_required
def enterscores(request):
	#uname = request.user.username #locates the logged in users user_name
	#instance = Daily.objects.get(user_id = uname) #pulls the Daily db data for the logged in user
	#grouping = instance.grouping #identifies the group the golfer is in
	
	#TODO
	#determine what happens if a group is not assigned
	#find and display the other golfers in that group
	#determine what happens if too few golfers
	#determine what happens if too many golfers
	#find hole number based on previously entered holes; auto fill the hole select bar with this value
	#display course name
	#display hole par
	#auto fill the scores for the particular hole selected based on what's been entered in the db
	#POST scores to Daily.objects by user_name
	#display that the scores were saved.... pause
	#index to the next hole with new par, blank scores, etc.

	#Variables to pass on to html = hole, par, course, g1 name, g1 prescore, g2 name, g2 prescore, g3, name, g3 prescore, g4 name, g4 prescore
	
	return render(request, 'tourney/enterscores.html', {})
	
	
@login_required
def compile(request):
	return render(request, 'tourney/compile.html', {})
