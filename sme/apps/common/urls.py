from django.conf.urls import url

from .views import SigninView, SignupView, ProfileView

urlpatterns = [
    url(r'^login/$', SigninView.as_view(), name='login'),
    url(r'^register/$', SignupView.as_view(), name='register'),
    url(r'^profile/$', ProfileView.as_view(), name='profile')
]
