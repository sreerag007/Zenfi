from django.urls import path
from .views import *

urlpatterns = [
    path('google_auth/',GoogleAuthView.as_view(),name='google_sign_up'),
    path('complete_sign_up/',ProfileCompleteView.as_view(),name='complete_sign_up'),
    path('profile/update/',ProfileUpdateView.as_view(),name='profile/update/'),
    path('profile/check-session/',CheckUserSessionView.as_view(),name='profile/check/session')
]
