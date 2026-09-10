from django.urls import path
from .views import *

urlpatterns = [
    path('api/share/',ShareFileCreateView.as_view(),name="share_files"),
    path('api/share/list/',ShareFileListView.as_view(),name="shared_files_retrieved"),
    path('api/room_code/create/',RoomCreateView.as_view(),name="room_code_generate"),
    path('api/room_code/',RoomListView.as_view(),name='room_code_list'),
    path('api/room_code/join/',RoomJoinView.as_view(),name='room_code_join')
]
