from django.shortcuts import render
from django.http import HttpResponseRedirect
from tourney.models import Profile, Daily, Message
from django_tables2 import RequestConfig
from tourney.tables import DailyTable, SmallLeaderTable, MessageTable, ScoreCardTable
from tourney.forms import EnterScoreForm, MessageForm, CompileForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required

#########################################################          MAIN              ####################################

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
			
		#make a list that becomes the small leaderboard
		small_lb_list = []
		small_lb_qs = qs.order_by('-net_day_points')[:7]   #CHANGE TO NER_TOURNEY_POINTS
		for j in small_lb_qs:
			small_lb_list.append(tuple([j.golfer, j.net_day_points, j.thru]))
		
		table = SmallLeaderTable(qs)
		RequestConfig(request).configure(table)
		
		messtable = MessageTable(Message.objects.all()) ###### DELTE ALL OF THIS??????????????
		messtable.order_by = '-posttime'
		messtable.exclude = ('posttime')
		RequestConfig(request).configure(messtable)     ###### DELTE ALL OF THIS??????????????
	
		messlist = []
		messqs = Message.objects.order_by('-posttime')[:20]
		for i in messqs:
			messlist.append(tuple([i.author, i.message]))
	
		form = MessageForm(request.POST or None)
		if request.method == 'POST':
			if form.is_valid():
				author = who.display_name
				message = request.POST['message']
				posttime = timezone.now()
				p = Message.objects.create(author=author, message=message, posttime=posttime)
				return HttpResponseRedirect('/main/')
		return render(request, 'tourney/index.html', {'name': name, 'group': group, 'teetime': teetime, 'table': table, 'form': form, 'small_lb_list': small_lb_list, 'messtable':messtable, 'messlist':messlist})
	
	else:
		return HttpResponseRedirect('newprofile/')
	
@login_required
def leaderboard(request):
	return render(request, 'tourney/leaderboard.html', {})
	

############################################        SCORE CARDS          ##################################################	


@login_required
def scorecards(request):
	scoretable = ScoreCardTable(Daily.objects.all())
	scoretable.order_by = 'golfer'
	RequestConfig(request).configure(scoretable)
	return render(request, 'tourney/scorecards.html', {'scoretable':scoretable})

#############################################       TOURNEY INFO         ###################################################	

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
	
################################################       ENTER SCORES          ###############################################

@login_required
def enterscores(request):
	uid = request.user.username
	who = Profile.objects.get(user_id=uid)
	qs = Daily.objects.all()
	user_list=[]
	if request.method == 'POST':
		form = EnterScoreForm(request.POST)    # or None)   #, initial={'hole':pf_hole})
		if form.is_valid():
			#hole = int(request.POST['hole']) #returns the hole number as an integer
			
			inst = qs.get(user_name = who.display_name) #sort the golfer list to match below
			group = inst.grouping  #sort the golfer list to match below
			#hole = request.POST['hole_pass']
			#hole = inst.thru + 1
			hole = request.session.get('pass_hole')
			thru = hole
			hole_score = 'h' + str(hole) + '_pts' #should be a string like 'h1_pts' so it can be used with setattr()
			golfer_qs = qs.filter(grouping = group)  #sort the golfer list to match below
			ordered_gqs = golfer_qs.order_by('user_name')  #sort the golfer list to match below
			#golfer_list = list(ordered_gqs)  #sort the golfer list to match below
			
			#update thru and hole scores in Daily
			g1_score = request.POST['g1_score']
			g2_score = request.POST['g2_score']
			g3_score = request.POST['g3_score']
			g4_score = request.POST['g4_score']
			score_list = [g1_score, g2_score, g3_score, g4_score]
			n = 0
			for i in ordered_gqs:
				instance = qs.get(user_name = i)
				instance.thru = thru
				pts = int(score_list[n])
				n += 1
				setattr(instance, hole_score, pts)
				
				#update raw_daily_points
				points_sum = 0
				for p in range(1,19):  
					hole_attr = 'h' + str(p) + '_pts'
					try:
						points_sum += getattr(instance, hole_attr)
					except TypeError:
						pass
				setattr(instance, 'raw_day_points', points_sum)
				
				#update net_day_points
				net_score = getattr(instance, 'raw_day_points') - instance.quota
				setattr(instance, 'net_day_points', net_score)
				instance.save()
			return HttpResponseRedirect('/enterscores/')
	
# CREATE A NEW FORM FOR WHEN PAGE IS FIRST LOADED
	else:
		if qs.filter(user_name = who).exists():
			instance = qs.get(user_name = who.display_name)
			group = instance.grouping	
			hole = instance.thru + 1
			thru = hole
			request.session['pass_hole'] = hole
			#request.session.modified = True
			if hole < 18:
				pf_hole = hole #pre-filled hole value for form selector
			else:
				pf_hole = 18
	
			#par = 
	
			golfer_qs = qs.filter(grouping = group)
			ordered_gqs = golfer_qs.order_by('user_name')
			golfer_list = list(ordered_gqs)
			
	
			try:	
				g1_name = golfer_list[0].golfer
				g1_rdp = golfer_list[0].raw_day_points
				g1_user_name = golfer_list[0].user_name #what's used to POST to Daily
			except IndexError:
				g1_name = 'None Assigned'
				g1_rdp = 0
				g1_user_name = ''
			try:
				g2_name = golfer_list[1].golfer
				g2_rdp = golfer_list[1].raw_day_points
				g2_user_name = golfer_list[1].user_name #what's used to POST to Daily
			except IndexError:
				g2_name = 'None Assigned'
				g2_rdp = 0
				g2_user_name = ''
			try:
				g3_name = golfer_list[2].golfer
				g3_rdp = golfer_list[2].raw_day_points
				g3_user_name = golfer_list[2].user_name #what's used to POST to Daily
			except IndexError:
				g3_name = 'None Assigned'
				g3_rdp = 0
				g3_user_name = ''		
			try:
				g4_name = golfer_list[3].golfer
				g4_rdp = golfer_list[3].raw_day_points
				g4_user_name = golfer_list[3].user_name #what's used to POST to Daily
			except IndexError:
				g4_name = 'None Assigned'
				g4_rdp = 0
				g4_user_name = ''		
		
			# if a GET (or any other method) we'll create a blank form
			hpt_attr = 'h' + str(pf_hole) + '_pts' #to set the key for the getattr function
			
			#pre fill scores into a new form
			try:
				pf_g1_score = getattr(golfer_list[0], hpt_attr)
			except IndexError:	
				pf_g1_score = None
			try:	
				pf_g2_score = getattr(golfer_list[1], hpt_attr)
			except IndexError:
				pf_g2_score = None
			try:
				pf_g3_score = getattr(golfer_list[2], hpt_attr)
			except IndexError:	
				pf_g3_score = None
			try:
				pf_g4_score = getattr(golfer_list[3], hpt_attr)
			except IndexError:
				pf_g4_score = None
			
			
			form = EnterScoreForm(initial={'g1_score': pf_g1_score, 'g2_score': pf_g2_score, 'g3_score': pf_g3_score, 'g4_score': pf_g4_score})
			content = {
				'hole': hole,
				'group' : group,
				'g1_name': g1_name,
				'g1_rdp': g1_rdp,
				'g2_name': g2_name,
				'g2_rdp': g2_rdp,
				'g3_name': g3_name,
				'g3_rdp': g3_rdp,
				'g4_name': g4_name,
				'g4_rdp': g4_rdp,
				'form':form,
				}
			return render(request, 'tourney/enterscores.html', content)
	
		else:
			form = EnterScoreForm()
			content = {
				'hole' : pf_hole,
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
	#display that the scores were saved.... pause
	#index to the next hole with new par, blank scores, etc.

################################################       CHANGE HOLES / ENTER SCORES          ###############################################

@login_required
def changeholes(request, hole_id):
	uid = request.user.username
	who = Profile.objects.get(user_id=uid)
	qs = Daily.objects.all()
	user_list=[]
	"""
	if request.method == 'POST':
		form = EnterScoreForm(request.POST)    # or None)   #, initial={'hole':pf_hole})
		if form.is_valid():
			#hole = int(request.POST['hole']) #returns the hole number as an integer
			hole = hole_id
			thru = hole
			hole_score = 'h' + str(hole) + '_pts' #should be a string like 'h1_pts' so it can be used with setattr()

			inst = qs.get(user_name = who.display_name) #sort the golfer list to match below
			group = inst.grouping  #sort the golfer list to match below
			golfer_qs = qs.filter(grouping = group)  #sort the golfer list to match below
			ordered_gqs = golfer_qs.order_by('user_name')  #sort the golfer list to match below
			#golfer_list = list(ordered_gqs)  #sort the golfer list to match below
			
			#update thru and hole scores in Daily
			g1_score = request.POST['g1_score']
			g2_score = request.POST['g2_score']
			g3_score = request.POST['g3_score']
			g4_score = request.POST['g4_score']
			score_list = [g1_score, g2_score, g3_score, g4_score]
			n = 0
			for i in ordered_gqs:
				instance = qs.get(user_name = i)
				instance.thru = thru
				pts = int(score_list[n])
				n += 1
				setattr(instance, hole_score, pts)
				
				#update raw_daily_points
				points_sum = 0
				for p in range(1,19):  
					hole_attr = 'h' + str(p) + '_pts'
					try:
						points_sum += getattr(instance, hole_attr)
					except TypeError:
						pass
				setattr(instance, 'raw_day_points', points_sum)
				
				#update net_day_points
				net_score = getattr(instance, 'raw_day_points') - instance.quota
				setattr(instance, 'net_day_points', net_score)
				instance.save()
			return HttpResponseRedirect('/enterscores/')
	"""
# CREATE A NEW FORM FOR WHEN PAGE IS FIRST LOADED FROM A HOLE CHANGE
	#else:
	if qs.filter(user_name = who).exists():
		instance = qs.get(user_name = who.display_name)
		group = instance.grouping	
		#thru = instance.thru
		pf_hole = hole_id
		request.session['pass_hole'] = hole_id
		#request.session.modified = True
		#par = 

		golfer_qs = qs.filter(grouping = group)
		ordered_gqs = golfer_qs.order_by('user_name')
		golfer_list = list(ordered_gqs)
		

		try:	
			g1_name = golfer_list[0].golfer
			g1_rdp = golfer_list[0].raw_day_points
			g1_user_name = golfer_list[0].user_name #what's used to POST to Daily
		except IndexError:
			g1_name = 'None Assigned'
			g1_rdp = 0
			g1_user_name = ''
		try:
			g2_name = golfer_list[1].golfer
			g2_rdp = golfer_list[1].raw_day_points
			g2_user_name = golfer_list[1].user_name #what's used to POST to Daily
		except IndexError:
			g2_name = 'None Assigned'
			g2_rdp = 0
			g2_user_name = ''
		try:
			g3_name = golfer_list[2].golfer
			g3_rdp = golfer_list[2].raw_day_points
			g3_user_name = golfer_list[2].user_name #what's used to POST to Daily
		except IndexError:
			g3_name = 'None Assigned'
			g3_rdp = 0
			g3_user_name = ''		
		try:
			g4_name = golfer_list[3].golfer
			g4_rdp = golfer_list[3].raw_day_points
			g4_user_name = golfer_list[3].user_name #what's used to POST to Daily
		except IndexError:
			g4_name = 'None Assigned'
			g4_rdp = 0
			g4_user_name = ''		
	
		# if a GET (or any other method) we'll create a blank form
		hpt_attr = 'h' + str(pf_hole) + '_pts' #to set the key for the getattr function
		
		#pre fill scores into a new form
		try:
			pf_g1_score = getattr(golfer_list[0], hpt_attr)
		except IndexError:	
			pf_g1_score = None
		try:	
			pf_g2_score = getattr(golfer_list[1], hpt_attr)
		except IndexError:
			pf_g2_score = None
		try:
			pf_g3_score = getattr(golfer_list[2], hpt_attr)
		except IndexError:	
			pf_g3_score = None
		try:
			pf_g4_score = getattr(golfer_list[3], hpt_attr)
		except IndexError:
			pf_g4_score = None
		
		
		form = EnterScoreForm(initial={'g1_score': pf_g1_score, 'g2_score': pf_g2_score, 'g3_score': pf_g3_score, 'g4_score': pf_g4_score})
		content = {
			'hole': pf_hole,
			'group' : group,
			'g1_name': g1_name,
			'g1_rdp': g1_rdp,
			'g2_name': g2_name,
			'g2_rdp': g2_rdp,
			'g3_name': g3_name,
			'g3_rdp': g3_rdp,
			'g4_name': g4_name,
			'g4_rdp': g4_rdp,
			'form':form,
			}
		return render(request, 'tourney/enterscores.html', content)

	else:
		form = EnterScoreForm()
		content = {
			'hole': pf_hole,
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
	
###################################             COMPILE             #################################################


##########################  LOADS DAILY WITH QUOTA, GROUP, ROUND 1 SCORE, ROUND 2 SCORE
@login_required
def compile(request):
	compile_form = CompileForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			#get the info from the form
			round = request.POST['round']
			course = request.POST['course']
			g1_tt = request.POST['g1_tt']
			g2_tt = request.POST['g2_tt']
			g3_tt = request.POST['g3_tt']
			g4_tt = request.POST['g4_tt']
			g5_tt = request.POST['g5_tt']
	
			#make the variables for getattr using 'round'
			group_var = round + '_group'
			quota_var = round + '_quota'
	
			#load Profile and Daily as a queryset
			qsProfile = Profile.objects.filter(isgolfing=True)
			qsDaily = Daily.objects.all()
			
			#Move info from Profile to Daily (quota, group, r1 score, r2 score, r3 score)
			for user in qsProfile:
				uname = user.display_name
				quota = getattr(user, quota_var)
				group = getattr(user, group_var)
				r1_score = user.r1_score # the score from round 1; will be zero while the first round is played
				r2_score = user.r2_score # the score from round 2; will be zero while the first two rounds are palyed
				r3_score = user.r3_score # the score from round 3; will be zero while the first two rounds are palyed
				instance = qsDaily.get(user_name = user)
				instance.quota = quota
				instance.group = group
				instance.r1_score = r1_score
				instance.r2_score = r2_score
				instance.r3_score = r3_score
				instance.net_tourney_score = r1_score + r2_score + r3_score #Computes starting score until scores are computed with enterscores view
				instance.course = course
				if group == 1:
					instance.teetime = g1_tt
				elif group == 2:
					instance.teetime = g2_tt
				elif group == 3:
					instance.teetime = g3_tt
				elif group == 4:
					instance.teetime = g4_tt
				elif group == 5:
					instance.teetime = g5_tt
				else:
					instance.teetime = g1_tt
				instance.save()
			
			
			#Compute current score
			
			return HttpResponseRedirect('/compile/')
	table = DailyTable(Daily.objects.all())
	RequestConfig(request).configure(table)
	return render(request, 'tourney/compile.html', {'table': table, 'compile_form': compile_form})

	
######################### DELETES DAILY  #########################################
@login_required
def delete_daily(request):
    Daily.objects.all().delete()
    table = DailyTable(Daily.objects.all())
    RequestConfig(request).configure(table)
    return render(request, 'tourney/compile.html', {'table': table})

	
########################### LOADS GOLFERS INTO DAILY  ###############################
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
