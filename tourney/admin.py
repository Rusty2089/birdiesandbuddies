from django.contrib import admin

from .models import Profile #https://docs.djangoproject.com/en/2.0/intro/tutorial02/
from .models import Course
from .models import Daily
from .models import Message
from .models import Extra

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(Daily)
admin.site.register(Message)
admin.site.register(Extra)
admin.site.register(Lights)