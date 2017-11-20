from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import SigninView, SignupView, ProfileView, EditProfileView

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='home'),
    url(r'^login/$', SigninView.as_view(), name='login'),
    url(r'^register/$', SignupView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^edit/profile/(?P<pk>\d+)/$', EditProfileView.as_view(), name='edit-profile')
]
