from django.conf.urls import url
from django.contrib.auth.views import LogoutView

from .views import (SigninView, SignupView, ProfileView,
                    EditProfileView, ConversationView, SearchView,
                    AddGroupView, GroupDetailView, AgreeTermsView,
                    CreateCourseView, CourseListingView, CourseDetailView,
                    CoursePayView, GroupConversationView,
                    CommentConversationView, ViewProfile)

urlpatterns = [
    url(r'^$', ProfileView.as_view(), name='home'),
    url(r'^accounts/login/$', SigninView.as_view(), name='login'),
    url(r'^login/$', SigninView.as_view(), name='login'),
    url(r'^register/$', SignupView.as_view(), name='register'),
    url(r'^logout/$', LogoutView.as_view(), name='logout'),
    url(r'^profile/$', ProfileView.as_view(), name='profile'),
    url(r'^view/profile/(?P<pk>\d+)/$', ViewProfile.as_view(), name='view-profile'),
    url(r'^edit/profile/(?P<profile_type>\w+)/$', EditProfileView.as_view(), name='edit-profile'),
    url(r'^send/message/(?P<to_user_id>\d+)/$', ConversationView.as_view(), name='conversation'),
    #url(r'^block/message/(?P<to_user_id>\d+)/$', ConversationBlockView.as_view(), name='conversation-block'),
    url(r'^search/(?P<whom>\w+)/$', SearchView.as_view(), name='search'),
    url(r'^add/group/$', AddGroupView.as_view(), name='add-group'),
    url(r'^group/detail/(?P<pk>\d+)/$', GroupDetailView.as_view(), name='group-detail'),
    url(r'^group/conversation/(?P<pk>\d+)/$', GroupConversationView.as_view(), name='group-conversation'),
    url(r'^agree/terms/$', AgreeTermsView.as_view(), name='agree-terms'),
    url(r'^create/course/$', CreateCourseView.as_view(), name='create-course'),
    url(r'^course/list/$', CourseListingView.as_view(), name='course-listing'),
    url(r'^course/detail/(?P<pk>\d+)/$', CourseDetailView.as_view(), name='course-detail'),
    url(r'^course/(?P<pk>\d+)/pay/$', CoursePayView.as_view(), name='pay-course'),
    url(r'^conversation/comment/(?P<pk>\d+)/$', CommentConversationView.as_view(), name='comment-conversation'),

    #url(r'^join/group/?P<pk>\d+)/$', JoinGroupView.as_view(), name='group-join'),
]
