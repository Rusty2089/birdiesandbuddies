from django.shortcuts import render
from django.http import HttpResponseRedirect
from tourney.models import Profile, Daily, Message, Course, Extra, Light
from django_tables2 import RequestConfig
from tourney.tables import DailyTable, SmallLeaderTable, MessageTable, ScoreCardTable, ReverseTable, LeaderTable
from tourney.forms import EnterScoreForm, MessageForm, CompileForm, ReverseCompileForm, LightsForm
from django.utils import timezone
from django.contrib.auth.decorators import login_required
from operator import itemgetter
import json

def login(request):
	return render(request, 'registration/login.html')

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
			course = instance.course
		else:
			group = 'None'
			teetime  = 'None'
			
		#make a list that becomes the small leaderboard
		small_lb_list = []
		small_lb_qs = qs.order_by('-net_tourney_score')[:7]
		for j in small_lb_qs:
			small_lb_list.append(tuple([j.golfer, j.net_tourney_score, j.thru]))
		
		table = SmallLeaderTable(qs)
		RequestConfig(request).configure(table)
		
		#Develop variables to pass for extra
		extraqs = Extra.objects.all()
		ctpliststart = extraqs.filter(type = 'Closest to the Pin')
		ctpliststart = ctpliststart.order_by('hole')
		ctplist = []
		for i in ctpliststart:
			ctplist.append(tuple([i.hole, i.leader]))
		ldliststart = extraqs.filter(type = 'Long Drive')
		ldliststart = ldliststart.order_by('hole')
		ldlist = []
		for i in ldliststart:		
			ldlist.append(tuple([i.hole, i.leader]))
		
		#messtable = MessageTable(Message.objects.all()) ###### DELTE ALL OF THIS??????????????
		#messtable.order_by = '-posttime'
		#messtable.exclude = ('posttime')
		#RequestConfig(request).configure(messtable)     ###### DELTE ALL OF THIS??????????????
	
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
		try:
			return render(request, 'tourney/index.html', {'name': name, 'group': group, 'teetime': teetime, 'course': course, 'table': table, 'form': form, 'small_lb_list': small_lb_list, 'messlist':messlist, 'ctplist': ctplist, 'ldlist': ldlist})
		except UnboundLocalError:
			return render(request, 'tourney/index.html', {'name': 'You need to be added to the Daily DB', 'group': 'None', 'teetime': 'None', 'course': 'None', 'table': table, 'form': form, 'small_lb_list': small_lb_list, 'messlist':messlist, 'ctplist': ctplist, 'ldlist': ldlist})
	else:
		return HttpResponseRedirect('newprofile/')
	
@login_required
def leaderboard(request):
	leadertable = LeaderTable(Daily.objects.all())
	leadertable.order_by = '-net_tourney_score'
	RequestConfig(request).configure(leadertable)
	qsDaily=Daily.objects.all() #new until return statement
	team_list = []
	for i in range(1, 8):
		team_i_list = [i, 0]
		score = 0
		team = qsDaily.filter(team = i)
		for j in range(5):
			try:
				team_i_list.append(team[j].golfer)
			except IndexError:
				team_i_list.append('')
			try:
				score = score + team[j].net_tourney_score
			except IndexError:
				continue
		team_i_list[1] = score
		team_list.append(tuple(team_i_list))
	team_list = sorted(team_list, key=itemgetter(1), reverse=True)
	print(team_list)
	return render(request, 'tourney/leaderboard.html', {'leadertable':leadertable, 'team_list':team_list})

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
		form = EnterScoreForm(request.POST)
		#if form.is_valid(): #THIS WAS Commented out because form was not validating with new EXTRA_NAMES added.  everything below was indented in one tab
		inst = qs.get(user_name = who.display_name) #sort the golfer list to match below
		group = inst.grouping  #sort the golfer list to match below
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
		try:
			extra_leader = request.POST['extra_names']
		except:
			pass
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
			
			#update net_tourney_score
			net_tourney_score = instance.r1_score + instance.r2_score + net_score
			setattr(instance, 'net_tourney_score', net_tourney_score)
			
			instance.save()
		
		#See if there is an extra and save extra
		eqs = Extra.objects.all()
		try:
			einstance = Extra.objects.get(hole=hole)
			einstance.leader = extra_leader
			einstance.save()
		except Extra.DoesNotExist:
			pass
			
		return HttpResponseRedirect('/enterscores/')
			
		#else:
		#	print('Form did not validate')
		#	return render(request, 'tourney/errortemplate.html')
	
# CREATE A NEW FORM FOR WHEN PAGE IS FIRST LOADED
	else:
		if qs.filter(user_name = who).exists():
			instance = qs.get(user_name = who.display_name)
			group = instance.grouping
			if instance.thru < 18:
				hole = instance.thru + 1
			else:
				hole = 18
			thru = hole
			course = instance.course
			if hole <= 18:
				par_var = 'h' + str(hole) + '_par'
			else:
				par_var = 'h18_par'
			course_info = Course.objects.get(course_name = course)
			par = getattr(course_info, par_var)
			request.session['pass_hole'] = hole
			#request.session.modified = True
			if hole < 18:
				pf_hole = hole #pre-filled hole value for form selector
			else:
				pf_hole = 18
	
				
			golfer_qs = qs.filter(grouping = group)
			ordered_gqs = golfer_qs.order_by('user_name')
			golfer_list = list(ordered_gqs)
			
			#create extra_list for drop down of golfers for extra (closest to pin and long drive)
			extra_list = (('None','None'),(golfer_list[0].golfer, golfer_list[0].golfer),(golfer_list[1].golfer, golfer_list[1].golfer), (golfer_list[2].golfer, golfer_list[2].golfer), (golfer_list[3].golfer, golfer_list[3].golfer))
			
			#determine if hole is an extra and which kind of (Closest to the Pin or Long Drive)
			eqs = Extra.objects.all()
			try:
				einstance = Extra.objects.get(hole=hole)
				extra_type = einstance.type
				print(extra_type)
			except Extra.DoesNotExist:
				extra_type = 'None'
			
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
			
			
			
			
			#form = EnterScoreForm(initial={'g1_score': pf_g1_score, 'g2_score': pf_g2_score, 'g3_score': pf_g3_score, 'g4_score': pf_g4_score}) #here
			form = EnterScoreForm(extra_list, initial={'g1_score': pf_g1_score, 'g2_score': pf_g2_score, 'g3_score': pf_g3_score, 'g4_score': pf_g4_score}) #WORKS
		
			content = {
				'hole': hole,
				'group': group,
				'par': par,
				'extra_type': extra_type,
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
			
			if extra_type == 'Closest to the Pin' or extra_type == 'Long Drive':
				return render(request, 'tourney/enterscoresextra.html', content)
			else:
				return render(request, 'tourney/enterscores.html', content)
				
		else:
			form = EnterScoreForm()
			content = {
				'hole' : 'None',
				'group' : 'You need to be added to the Daily DB',
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
		course = instance.course
		par_var = 'h' + str(hole_id) + '_par'
		course_info = Course.objects.get(course_name = course)
		par = getattr(course_info, par_var)
		request.session['pass_hole'] = hole_id
		#request.session.modified = True
		#par = 

		golfer_qs = qs.filter(grouping = group)
		ordered_gqs = golfer_qs.order_by('user_name')
		golfer_list = list(ordered_gqs)
		
		extra_list = (('None','None'),(golfer_list[0].golfer, golfer_list[0].golfer),(golfer_list[1].golfer, golfer_list[1].golfer), (golfer_list[2].golfer, golfer_list[2].golfer), (golfer_list[3].golfer, golfer_list[3].golfer))

		try:
			einstance = Extra.objects.get(hole=hole_id)
			extra_type = einstance.type
			#print(extra_type)
		except Extra.DoesNotExist:
			extra_type = 'None'

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
		
		
		form = EnterScoreForm(extra_list, initial={'g1_score': pf_g1_score, 'g2_score': pf_g2_score, 'g3_score': pf_g3_score, 'g4_score': pf_g4_score})
		content = {
			'hole': pf_hole,
			'group': group,
			'par': par,
			'extra_type': extra_type,
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
		if extra_type == 'Closest to the Pin' or extra_type == 'Long Drive':
			return render(request, 'tourney/enterscoresextra.html', content)
		else:
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
		if compile_form.is_valid():
			#get the info from the form
			round = request.POST['round']
			course = request.POST['course']
			g1_tt = request.POST['g1_tt']
			g2_tt = request.POST['g2_tt']
			g3_tt = request.POST['g3_tt']
			g4_tt = request.POST['g4_tt']
			g5_tt = request.POST['g5_tt']
			g6_tt = request.POST['g6_tt']
			g7_tt = request.POST['g7_tt'] #ADDED FOR 28 Golfers for 2021
	
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
				team = user.team #new
				r1_score = user.r1_score # the score from round 1; will be zero while the first round is played
				r2_score = user.r2_score # the score from round 2; will be zero while the first two rounds are palyed
				r3_score = user.r3_score # the score from round 3; will be zero while the first two rounds are palyed
				instance = qsDaily.get(user_name = uname)
				instance.quota = quota
				instance.grouping = group
				instance.team = team #new
				instance.r1_score = r1_score
				instance.r2_score = r2_score
				instance.r3_score = r3_score
				#instance.net_day_points = instance.raw_day_points - quota
				instance.net_tourney_score = r1_score + r2_score + r3_score #+ instance.net_day_points #Computes starting score until scores are computed with enterscores view
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
				elif group == 6:
					instance.teetime = g6_tt
				elif group == 7:				#ADDED FOR 28 Golfers for 2021
					instance.teetime = g7_tt
				else:
					instance.teetime = g1_tt
				instance.save()
			
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

########################## COMPUTES NEW QUOTA, GROUPS, AND SAVES NEW QUOTA, GROUP, AND NET SCORE INTO PROFILE ############################
@login_required
def reverse_compile(request):
	reverse_compile_form = ReverseCompileForm(request.POST or None)
	if request.method == 'POST':
		if reverse_compile_form.is_valid():
			#get the info from the form
			round = request.POST['round']
			
			#make the variables going into Profile for getattr using 'round'
			score_var = round + '_score'
			if round == 'r1':
				print('round 1')
				group_var = 'r2_group'
				quota_var = 'r2_quota'
			if round == 'r2':
				group_var = 'r3_group'
				quota_var = 'r3_quota'
			if round == 'r3':
				group_var = 'r4_group'
				quota_var = 'r4_quota'
	
			#load Profile and Daily as a queryset
			qsProfile = Profile.objects.filter(isgolfing=True)
			qsDaily = Daily.objects.order_by('net_tourney_score', 'golfer') #ordered to populate groups based on net tourney score
			
			#get info to save into Profile from Daily
			np = 1 # nth players in a group (this will increase during the for loop until np_end is reached)
			gn = 1 # group number (this will incerease during the for loop)
			np_end = 4 # total number of golfers in a group
			for user in qsDaily:
				uname = user.user_name			
				score = user.net_day_points
				quota = 0
				if user.quota >= 25 and (user.raw_day_points - user.quota) > 2:
					quota = user.quota + 2
				else:
					quota = (user.quota + user.raw_day_points) // 2 + ((user.quota + user.raw_day_points) % 2 > 0)
				instance = qsProfile.get(display_name = uname)
				setattr(instance, score_var, score)
				setattr(instance, quota_var, quota)
				if np <= np_end:
					setattr(instance, group_var, gn)
					np += 1
				else:
					np = 2
					gn += 1
					setattr(instance, group_var, gn)
				instance.save()
			
			
			
			return HttpResponseRedirect('/reversecompile/')
	table = DailyTable(Daily.objects.all())
	RequestConfig(request).configure(table)
	reverse_table = ReverseTable(Profile.objects.filter(isgolfing = True))
	RequestConfig(request).configure(reverse_table)
	return render(request, 'tourney/reversecompile.html', {'table': table, 'reverse_table': reverse_table, 'reverse_compile_form': reverse_compile_form})

##################################### SEND REUNION OUR PAIRINGS ###############################
def reunion(request):
	reunion_list = []
	qs = Daily.objects.order_by('grouping')
	for user in qs:
		reunion_list.append(tuple([user.grouping, user.golfer, user.course, user.teetime]))
	return render(request, 'tourney/reunion.html', {'reunion_list': reunion_list})

##################################### B&B HISTORY ##########################################
def history(request):
	return render(request, 'tourney/history.html')
	
##################################### LIGHTS ##########################################
def goletalights_json(request):
	qs = Light.objects.order_by('-postTime')[0]
	creator = qs.creator
	RoofColors = qs.RoofColors
	RoofEffect = qs.RoofEffect
	PalmColors = qs.PalmColors
	PalmEffect = qs.PalmEffect
	FloorColors = qs.FloodColors
	SconceColors = qs.SconceColors
	return render(request, 'tourney/goletalights_json.html', {'creator': creator, 'RoofColors': RoofColors, 'RoofEffect': RoofEffect, 'PalmColors': PalmColors, 'PalmEffect': PalmEffect, 'FloodColors': FloodColors, 'SconceColors': SconceColors})
	
def goletalights(request):
	form = LightsForm(request.POST or None)
	if request.method == 'POST':
		if form.is_valid():
			creator = request.POST['creator']
			#postTime = timezone.now()
			RoofColors = json.dumps(request.POST.getlist('RoofColors',[])) #json.dumps() saves the list with double quotes
			PalmColors = json.dumps(request.POST.getlist('PalmColors',[]))
			FloodColors = json.dumps(request.POST.getlist('FloodColors',[]))
			SconceColors = json.dumps(request.POST.getlist('SconceColors',[]))
			p = Light.objects.create(creator=creator, RoofColors=RoofColors, PalmColors=PalmColors, FloodColors=FloodColors, SconceColors=SconceColors)
			return HttpResponseRedirect('/goletalights/')

	# if a GET (or any other method) we'll create a blank form
	return render(request, 'tourney/goletalights.html', {'form': form})