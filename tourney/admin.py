from django.contrib import admin

from .models import Profile #https://docs.djangoproject.com/en/2.0/intro/tutorial02/
from .models import Course
from .models import Daily
from .models import Message
from .models import Extra
from .models import Light

class ProfileAdmin(admin.ModelAdmin):

admin.site.register(Profile, ProfileAdmin)
	list_display = [field.name for field in Profile._meta.get_fields()  if not field.is_relation]
admin.site.register(Course)
admin.site.register(Daily)
admin.site.register(Message)
admin.site.register(Extra)
admin.site.register(Light)