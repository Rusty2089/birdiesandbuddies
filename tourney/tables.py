# tables.py
import django_tables2 as tables
from tourney.models import Daily

class DailyTable(tables.Table):
    class Meta:
        model = Daily
        #template_name = 'django_tables2/bootstrap.html'
        fields = ('golfer', 'user_name', 'grouping', 'startscore', 'quota')
		
class SmallLeaderTable(tables.Table):
    class Meta:
        model = Daily
        #template_name = 'django_tables2/bootstrap.html'
        fields = ('golfer', 'net_tourney_score', 'quota')