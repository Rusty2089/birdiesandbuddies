from django.contrib import admin
from django.urls import include, path, re_path
from django.contrib.auth import views as auth_views
from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.auth import logout
from tourney import views

urlpatterns = [
	path('', include('tourney.urls')),
	path('tourney/', include('tourney.urls'), name='tourney'),
	path('admin/', admin.site.urls),
	path("login/", views.login, name="login"),
	path("logout/", auth_views.LogoutView.as_view(), name="logout"),
	path('social-auth/', include('social_django.urls', namespace="social")),
	#re_path(r'^login/$', views.LoginView, name='login'),
	#re_path('login/', auth_views.LoginView, {'template_name': "users/registration/login.html"}, name='login'),
	#re_path(r'^logout/$', logout, {'next_page': settings.LOGOUT_REDIRECT_URL}, name='logout'),
	#re_path(r'^auth/', include('social_django.urls', namespace='social')),  # <- Here
] + static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)