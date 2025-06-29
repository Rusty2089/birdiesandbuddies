from django.contrib import admin

from .models import Profile #https://docs.djangoproject.com/en/2.0/intro/tutorial02/
from .models import Course
from .models import Daily
from .models import Message
from .models import Extra
from .models import Light

class ProfileAdmin(admin.ModelAdmin):
	list_display = ('id', 'display_name', 'first_name', 'last_name', 'isgolfing', 'r1_quota', 'r1_group', 'team', 'roomTeam')
	list_editable = ('display_name', 'first_name', 'last_name', 'isgolfing', 'r1_quota', 'r1_group', 'team', 'roomTeam')
	#list_editable = ('isgolfing', 'r1_quota', 'r1_group', 'r1_group', 'team', 'roomTeam')
	#list_display_links = None
	
class DailyAdmin(admin.ModelAdmin):
	list_display = [field.name for field in Daily._meta.get_fields()  if not field.is_relation]
	list_editable = [field.name for field in Daily._meta.get_fields()  if not field.is_relation]
	list_display_links = None

admin.site.register(Profile, ProfileAdmin)
admin.site.register(Course)
admin.site.register(Daily, DailyAdmin)
admin.site.register(Message)
admin.site.register(Extra)
admin.site.register(Light)