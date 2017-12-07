from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import (SigninView, SignupView, ProfileView,
                    EditProfileView, ConversationView, SearchView,
                    AddGroupView, GroupDetailView)

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='home'),
    url(r'^accounts/login/$', SigninView.as_view(), name='login'),
    url(r'^login/$', SigninView.as_view(), name='login'),
    url(r'^register/$', SignupView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^edit/profile/(?P<pk>\d+)/$', EditProfileView.as_view(), name='edit-profile'),
    url(r'^send/message/(?P<to_user_id>\d+)/$', ConversationView.as_view(), name='conversation'),
    #url(r'^block/message/(?P<to_user_id>\d+)/$', ConversationBlockView.as_view(), name='conversation-block'),
    url(r'^search/(?P<whom>\w+)/$', SearchView.as_view(), name='search'),
    url(r'^add/group/$', AddGroupView.as_view(), name='add-group'),
    url(r'^group/detail/(?P<pk>\d+)/$', GroupDetailView.as_view(), name='group-detail'),
    #url(r'^join/group/?P<pk>\d+)/$', JoinGroupView.as_view(), name='group-join'),
]
