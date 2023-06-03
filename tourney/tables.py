# tables.py
import django_tables2 as tables
from tourney.models import Daily, Message, Profile

class DailyTable(tables.Table):
    class Meta:
        model = Daily
        #template_name = 'django_tables2/bootstrap.html'
        fields = ('golfer', 'user_name', 'quota', 'grouping', 'team', 'roomTeam', 'course', 'teetime', 'r1_score', 'r2_score', 'r3_score')
		
class SmallLeaderTable(tables.Table):
	net_day_points = tables.Column(
		verbose_name = 'Daily Net', 
		attrs={
		"th": {"id": "foo"},
		"td": {"align": "center"}
		}	
		)
	thru = tables.Column(	
		verbose_name = 'Thru', 
		attrs={
		"th": {"id": "foo"},
		"td": {"align": "center"}
		}	
		)
		
	class Meta:
		model = Daily
		fields = ('golfer', 'net_day_points', 'thru')
		
##################### LEADERBOARD ########################
class LeaderTable(tables.Table):
	thru = tables.Column(verbose_name = 'Thru',)
	r1_score = tables.Column(verbose_name = 'Round 1',)
	r2_score = tables.Column(verbose_name = 'Round 2',)
	net_day_points = tables.Column(verbose_name = 'Daily Net',)
	net_tourney_score = tables.Column(verbose_name = 'Tourney',)
		
	class Meta:
		model = Daily
		fields = ('golfer', 'r1_score', 'r2_score', 'net_day_points', 'net_tourney_score', 'thru')
		
class MessageTable(tables.Table):
	message = tables.Column(verbose_name= 'Messages' )

	class Meta:
		model = Message
		fields = ('message', 'posttime',)
		

		
class ScoreCardTable(tables.Table):
	net_day_points = tables.Column(verbose_name = 'Daily Net',)
	thru = tables.Column(verbose_name = 'Thru',)
	h1_pts = tables.Column(verbose_name = 'H1',)
	h2_pts = tables.Column(verbose_name = 'H2',)
	h3_pts = tables.Column(verbose_name = 'H3',)
	h4_pts = tables.Column(verbose_name = 'H4',)
	h5_pts = tables.Column(verbose_name = 'H5',)
	h6_pts = tables.Column(verbose_name = 'H6',)
	h7_pts = tables.Column(verbose_name = 'H7',)
	h8_pts = tables.Column(verbose_name = 'H8',)
	h9_pts = tables.Column(verbose_name = 'H9',)
	h10_pts = tables.Column(verbose_name = 'H10',)
	h11_pts = tables.Column(verbose_name = 'H11',)
	h12_pts = tables.Column(verbose_name = 'H12',)
	h13_pts = tables.Column(verbose_name = 'H13',)
	h14_pts = tables.Column(verbose_name = 'H14',)
	h15_pts = tables.Column(verbose_name = 'H15',)
	h16_pts = tables.Column(verbose_name = 'H16',)
	h17_pts = tables.Column(verbose_name = 'H17',)
	h18_pts = tables.Column(verbose_name = 'H18',)
	raw_day_points = tables.Column(verbose_name = 'Daily Raw',)
	r1_score = tables.Column(verbose_name = 'Round 1',)
	r2_score = tables.Column(verbose_name = 'Round 2',)
	net_tourney_score = tables.Column(verbose_name = 'Tourney',)
		
	class Meta:
		model = Daily
		exclude = ('id', 'user_name', 'grouping', 'teetime', 'course', 'startscore')
		

class ReverseTable(tables.Table):
	#name = tables.Column(verbose_name= 'Messages' )
	class Meta:
		model = Profile
		exclude = ('user_id', 'display_name', 'city', 'state', 'isgolfing')