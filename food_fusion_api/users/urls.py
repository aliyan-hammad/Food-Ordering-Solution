from django.urls import path
from .views import UserRegistrationView,UserLoginView,logout


urlpatterns=[
    path('register/',UserRegistrationView.as_view(),name='user-registeration'),
    path('login/',UserLoginView.as_view(),name="user-login"),
    path('logout/',logout,name='user-logout')
]