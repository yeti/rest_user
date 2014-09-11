from django.conf.urls import patterns, url, include
from rest_user.rest_user import views

urlpatterns = patterns('',
    url(r'^sign_up/$', views.SignUp.as_view()),
    url(r'^login/$', views.Login.as_view()),
    url(r'^o/', include('oauth2_provider.urls', namespace='oauth2_provider')),
)

