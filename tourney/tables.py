# tables.py
import django_tables2 as tables
from tourney.models import Daily, Message

class DailyTable(tables.Table):
    class Meta:
        model = Daily
        #template_name = 'django_tables2/bootstrap.html'
        fields = ('golfer', 'user_name', 'quota', 'grouping', 'courese', 'teetime', 'r1_score', 'r2_score')
		
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
		
class MessageTable(tables.Table):
	message = tables.Column(verbose_name= 'Messages' )

	class Meta:
		model = Message
		fields = ('message', 'posttime',)
		

		
class ScoreCardTable(tables.Table):
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
		exclude = ('id', 'user_name', 'grouping', 'teetime', 'startscore')