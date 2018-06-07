from django.contrib import admin

from .models import Profile #https://docs.djangoproject.com/en/2.0/intro/tutorial02/
from .models import Course
from .models import RoundData
from .models import Daily

admin.site.register(Profile)
admin.site.register(Course)
admin.site.register(RoundData)
admin.site.register(Daily)