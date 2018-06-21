from django.shortcuts import render
from django.http import HttpResponseRedirect
from tourney.models import Profile, Daily, Message
from django_tables2 import RequestConfig
from tourney.tables import DailyTable, SmallLeaderTable, MessageTable
from tourney.forms import EnterScoreForm, MessageForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

@login_required
def main(request):
	uid = request.user.username
	who = Profile.objects.filter(user_id=uid)
	qs = Daily.objects.all()
	if who.exists():
		who = who[0]
		name = who.first_name + ' ' + who.last_name
		#qs = Daily.objects.all()
		if qs.filter(user_name = who).exists():
			instance = qs.get(user_name = who.display_name)
			group = instance.grouping
			teetime = instance.teetime
		else:
			group = 'None'
			teetime  = 'None'
		table = SmallLeaderTable(qs)
		RequestConfig(request).configure(table)
		
		messtable = MessageTable(Message.objects.all())
		messtable.order_by = '-posttime'
		messtable.exclude = ('posttime')
		RequestConfig(request).configure(messtable)
	
		messlist = []
		messqs = Message.objects.order_by('-posttime')[:20]
		for i in messqs:
			messlist.append(tuple([i.author, i.message]))
		print(messlist)
	
		form = MessageForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				author = who.display_name
				message = request.POST['message']
				posttime = timezone.now()
				p = Message.objects.create(author=author, message=message, posttime=posttime)
				return HttpResponseRedirect('/main/')
		return render(request, 'tourney/index.html', {'name': name, 'group': group, 'teetime': teetime, 'table': table, 'form': form, 'messtable':messtable, 'messlist':messlist})
	
	else:
		return HttpResponseRedirect('newprofile/')
	
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
	uid = request.user.username
	who = Profile.objects.get(user_id=uid)
	qs = Daily.objects.all()
	if qs.filter(user_name = who).exists():
		instance = qs.get(user_name = who.display_name)
		group = instance.grouping	
		thru = instance.thru
		if thru < 18:
			pf_hole = thru + 1 #pre-filled hole value for form selector
		else:
			pf_hole = 18
	
		#par = 
	
		golfer_qs = qs.filter(grouping = group)
		golfer_list = list(golfer_qs)
	
		try:	
			g1_name = golfer_list[0].golfer
			g1_ts = golfer_list[0].net_tourney_score
			g1_user_name = golfer_list[0].user_name #what's used to POST to Daily
		except IndexError:
			g1_name = 'None Assigned'
			g1_ts = 0
			g1_user_name = ''
		try:
			g2_name = golfer_list[1].golfer
			g2_ts = golfer_list[1].net_tourney_score
			g2_user_name = golfer_list[1].user_name #what's used to POST to Daily
		except IndexError:
			g2_name = 'None Assigned'
			g2_ts = 0
			g2_user_name = ''
		try:
			g3_name = golfer_list[2].golfer
			g3_ts = golfer_list[2].net_tourney_score
			g3_user_name = golfer_list[2].user_name #what's used to POST to Daily
		except IndexError:
			g3_name = 'None Assigned'
			g3_ts = 0
			g3_user_name = ''		
		try:
			g4_name = golfer_list[3].golfer
			g4_ts = golfer_list[3].net_tourney_score
			g4_user_name = golfer_list[3].user_name #what's used to POST to Daily
		except IndexError:
			g4_name = 'None Assigned'
			g4_ts = 0
			g4_user_name = ''		
		
		
		form = EnterScoreForm(request.POST or None, initial={'hole':pf_hole})
		if request.method == 'POST':
			if form.is_valid():
				hole = request.POST['hole'] #returns the hole number as an integer
				thru = hole + 1 #indexes the thru value up one
				hole_str = 'h' + str(hole) #should be a string like 'h1'
				
				#instance.first_name=request.POST['g1_score']
				#instance.last_name=request.POST['g2_score']
				#instance.city=request.POST['g3_score']
				#instance.state=request.POST['g4_score']
				#instance.isgolfing=request.POST['hole']
				#update thru
				#instance.save()
				# redirect to a new URL:
				return HttpResponseRedirect('/enterscores/')

		# if a GET (or any other method) we'll create a blank form
		content = {
			'group' : group,
			'g1_name': g1_name,
			'g1_ts': g1_ts,
			'g2_name': g2_name,
			'g2_ts': g2_ts,
			'g3_name': g3_name,
			'g3_ts': g3_ts,
			'g4_name': g4_name,
			'g4_ts': g4_ts,
			'form':form,
			}
		
		return render(request, 'tourney/enterscores.html', content)
	
	else:
		form = EnterScoreForm(request.POST or None)
		if request.method == 'POST':
			return HttpResponseRedirect('/enterscores/')
		content = {
			'group' : 0,
			'g1_name': '',
			'g1_ts': 0,
			'g2_name': '',
			'g2_ts': 0,
			'g3_name': '',
			'g3_ts': 0,
			'g4_name': '',
			'g4_ts': 0,
			'form':form,
			}
		
		return render(request, 'tourney/enterscores.html', content)
			
	#TODO
	#determine what happens if too few golfers
	#determine what happens if too many golfers
	#find hole number based on previously entered holes; auto fill the hole select bar with this value
	#display course name
	#display hole par
	#POST scores to Daily.objects by user_name
	#display that the scores were saved.... pause
	#index to the next hole with new par, blank scores, etc.

	#Variables to pass on to html = hole, par, course, g1 name, g1 prescore, g2 name, g2 prescore, g3, name, g3 prescore, g4 name, g4 prescore
		
	
@login_required
def compile(request):
    if(request.POST.get('button')):
        if(request.POST.get('whichround') == 'blank'):
            print('Select a Round') #---- Replace with render
        else:
            quota = request.POST.get('whichround') + '_quota'
            score = request.POST.get('whichround') + '_startscore'
            dailyq = Daily.objects.all()
            profileq = Profile.objects.all()
            for user in dailyq:
                profilerow = profileq.get(display_name=user)
                newquota = getattr(profilerow, quota)
                newscore = getattr(profilerow, score)
                dailyrow = dailyq.get(user_name=user)
                dailyrow.quota = newquota
                dailyrow.startscore = newscore
                dailyrow.save()
                			
    table = DailyTable(Daily.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tourney/compile.html', {'table': table})

@login_required
def delete_daily(request):
    Daily.objects.all().delete()
    table = DailyTable(Daily.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tourney/compile.html', {'table': table})

@login_required	
def golfers_daily(request):
    qs = Profile.objects.filter(isgolfing=True)
    for user in qs:
        name = user.first_name + ' ' + user.last_name
        g = Daily(golfer = name, user_name = user)
        g.save()
    table = DailyTable(Daily.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tourney/compile.html', {'table': table})
#	return render(request, 'tourney/compile.html', {})

@login_required
def groups_daily(request):
	return render(request, 'tourney/compile.html', {})
