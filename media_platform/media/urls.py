from django.urls import path
from .views import ChannelListView, ChannelDetailView, ContentDetailView, ContentListView, GroupListView, GroupDetailView

# app_name = 'app'
urlpatterns = [
    path('contents/', ContentListView.as_view()),
    path('contents/<int:pk>/', view=ContentDetailView.as_view(), name='content-detail'),
    path('channels/', view=ChannelListView.as_view(), name='channel-list'),
    path('channels/<int:pk>/', view=ChannelDetailView.as_view(), name='channel-detail'),
    path('groups/', view=GroupListView.as_view(), name='group-list'),
    path('groups/<int:pk>/', view=GroupDetailView.as_view(), name='group-detail'),
]