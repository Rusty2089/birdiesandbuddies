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
	print(content)
	return render(request, 'tourney/tourneyinfo.html', content)
	

@login_required
def enterscores(request):
	return render(request, 'tourney/enterscores.html', {})
