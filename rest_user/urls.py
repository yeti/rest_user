from django.conf.urls import patterns, url
from rest_user.rest_user import views

urlpatterns = patterns('',
    url(r'^sign_up/$', views.SignUp.as_view()),
)

