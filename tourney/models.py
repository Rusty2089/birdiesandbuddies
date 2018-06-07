from django.db import models

# Create your models here.

class Daily(models.Model):
	display_name = models.CharField(max_length=15, unique=True)
	grouping = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
	quota = models.PositiveSmallIntegerField(default = 0)
	h1_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h2_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h3_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h4_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h5_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h6_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h7_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h8_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h9_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h10_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h11_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h12_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h13_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h14_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h15_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h16_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h17_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	h18_pts = models.PositiveSmallIntegerField(choices = (('aweful', 0), ('bogey', 1), ('par', 2), ('birdy', 4), ('eagle', 8), ('d_eagle', 10)))
	raw_day_points = models.PositiveSmallIntegerField()
	net_day_points = models.SmallIntegerField()
	net_tourney_score = models.SmallIntegerField()
	
	def __str__(self): #to return display_name instead of _id
		return self.display_name
		
class RoundData(models.Model):
	current_round = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3)))
	group1_ttime = models.TimeField(auto_now=False)
	group2_ttime = models.TimeField(auto_now=False)
	group3_ttime = models.TimeField(auto_now=False)
	group4_ttime = models.TimeField(auto_now=False)
	group5_ttime = models.TimeField(auto_now=False)
	
class Profile(models.Model):
    user_id = models.CharField(max_length=100, unique=True)
    display_name = models.CharField(max_length=15, unique=True)
    first_name = models.CharField(max_length=15)
    last_name = models.CharField(max_length=15)
    city = models.CharField(max_length=20, default='City')
    state = models.CharField(max_length=2, default='FL')
    isgolfing = models.NullBooleanField(default=True)
    r1_quota = models.PositiveSmallIntegerField(default = 0)
    r1_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
    r1_rawscore = models.SmallIntegerField(default = 0)
    r1_netscore = models.SmallIntegerField(default = 0)
    r2_quota = models.PositiveSmallIntegerField(default = 0)
    r2_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
    r2_startscore = models.SmallIntegerField(default = 0)	
    r2_rawscore = models.SmallIntegerField(default = 0)
    r2_netscore = models.SmallIntegerField(default = 0)
    r3_quota = models.PositiveSmallIntegerField(default = 0)
    r3_group = models.PositiveSmallIntegerField(choices = ((1, 1), (2, 2), (3, 3), (4, 4), (5, 5)), default = 0)
    r3_startscore = models.SmallIntegerField(default = 0)	
    r3_rawscore = models.SmallIntegerField(default = 0)
    r3_netscore = models.SmallIntegerField(default = 0)
	
    def __str__(self): #to return display_name instead of _id
        return self.display_name
	
class Course(models.Model):
    course_name = models.CharField(max_length=40)
    course_city = models.CharField(max_length=20)
    course_state = models.CharField(max_length=2)
    hole01_par = models.PositiveSmallIntegerField()
    hole02_par = models.PositiveSmallIntegerField()
    hole03_par = models.PositiveSmallIntegerField()
    hole04_par = models.PositiveSmallIntegerField()
    hole05_par = models.PositiveSmallIntegerField()
    hole06_par = models.PositiveSmallIntegerField()
    hole07_par = models.PositiveSmallIntegerField()
    hole08_par = models.PositiveSmallIntegerField()
    hole09_par = models.PositiveSmallIntegerField()
    hole10_par = models.PositiveSmallIntegerField()
    hole11_par = models.PositiveSmallIntegerField()
    hole12_par = models.PositiveSmallIntegerField()
    hole13_par = models.PositiveSmallIntegerField()
    hole14_par = models.PositiveSmallIntegerField()
    hole15_par = models.PositiveSmallIntegerField()
    hole16_par = models.PositiveSmallIntegerField()
    hole17_par = models.PositiveSmallIntegerField()
    hole18_par = models.PositiveSmallIntegerField()
    def __str__(self): #to return course_name instead of _id
        return self.course_name
		
