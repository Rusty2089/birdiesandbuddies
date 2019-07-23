from django.db import models

# Create your models here.

class Profile(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=20, unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    city = models.CharField(max_length=20, default='City')
    state = models.CharField(max_length=2, default='FL')
    isgolfing = models.NullBooleanField(default=True)
    r1_quota = models.PositiveSmallIntegerField(default = 0)
    r1_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
    r1_score = models.SmallIntegerField(default = 0)
    r2_quota = models.PositiveSmallIntegerField(default = 0)
    r2_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
    r2_score = models.SmallIntegerField(default = 0)
    r3_quota = models.PositiveSmallIntegerField(default = 0)
    r3_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
    r3_score = models.SmallIntegerField(default = 0)
    r4_quota = models.PositiveSmallIntegerField(default = 0)
    r4_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
	
    def __str__(self): #to return display_name instead of _id
        return self.display_name

class Daily(models.Model):
	user_name = models.CharField(max_length=20, unique=True, null=True)
	golfer = models.CharField(max_length=30, unique=True, null=True)
	grouping = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5), (6, 6)), default = 0)
	teetime = models.TimeField(auto_now=False, null=True)
	course = models.CharField(max_length=30, null=True)
	#startscore = models.SmallIntegerField(default = 0)
	quota = models.PositiveSmallIntegerField(default = 0)
	h1_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h2_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h3_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h4_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h5_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h6_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h7_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h8_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h9_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h10_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h11_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h12_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h13_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h14_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h15_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h16_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h17_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	h18_pts = models.PositiveSmallIntegerField(choices = ((0, '0'), (1, '1'), (2, '2'), (4, '4'), (8, '8'), (10, '10')), blank=True, null=True)
	thru = models.PositiveSmallIntegerField(default = 0)
	raw_day_points = models.PositiveSmallIntegerField(default = 0)
	net_day_points = models.SmallIntegerField(default = 0)
	r1_score = models.SmallIntegerField(default = 0) #the score posted from round 1
	r2_score = models.SmallIntegerField(default = 0) #the score posted from round 2
	net_tourney_score = models.SmallIntegerField(default = 0)
	
	def __str__(self): #to return user_name instead of _id
		return self.user_name
		
	#((0, 'Aweful'), (1, 'Bogey'), (2, 'Par'), (4, 'Birdie'), (8, 'Eagle'), (10, 'D_Eagle')), blank=True, null=True)
		
#class RoundData(models.Model):
#	round = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3)))
#	course = models.CharField(max_length = 30, choices = (('Nicklaus', 'Nicklaus'), ('Palmer', 'Palmer')))
#	group1_ttime = models.TimeField(auto_now=False)
#	group2_ttime = models.TimeField(auto_now=False)
#	group3_ttime = models.TimeField(auto_now=False)
#	group4_ttime = models.TimeField(auto_now=False)
#	group5_ttime = models.TimeField(auto_now=False)
	
class Course(models.Model):
    course_name = models.CharField(max_length = 30, choices = (('Nicklaus', 'Nicklaus'), ('Palmer', 'Palmer')))
    h1_par = models.PositiveSmallIntegerField()
    h2_par = models.PositiveSmallIntegerField()
    h3_par = models.PositiveSmallIntegerField()
    h4_par = models.PositiveSmallIntegerField()
    h5_par = models.PositiveSmallIntegerField()
    h6_par = models.PositiveSmallIntegerField()
    h7_par = models.PositiveSmallIntegerField()
    h8_par = models.PositiveSmallIntegerField()
    h9_par = models.PositiveSmallIntegerField()
    h10_par = models.PositiveSmallIntegerField()
    h11_par = models.PositiveSmallIntegerField()
    h12_par = models.PositiveSmallIntegerField()
    h13_par = models.PositiveSmallIntegerField()
    h14_par = models.PositiveSmallIntegerField()
    h15_par = models.PositiveSmallIntegerField()
    h16_par = models.PositiveSmallIntegerField()
    h17_par = models.PositiveSmallIntegerField()
    h18_par = models.PositiveSmallIntegerField()
    def __str__(self): #to return course_name instead of _id
        return self.course_name
		
class Message(models.Model):
	author = models.CharField(max_length=15)
	message = models.TextField(max_length=200, null=True)
	posttime = models.DateTimeField(null=True)
	
		
