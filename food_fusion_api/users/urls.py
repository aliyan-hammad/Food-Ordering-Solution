from django.urls import path
from .views import GetCreateUpdateProfile,UserLoginView,logout,ChangePassword,GetCustomersRecord,GetVendorDetail


urlpatterns=[
    path('register/',GetCreateUpdateProfile.as_view(),name='user-registeration'),
    path('profile/',GetCreateUpdateProfile.as_view(),name='profile-update'),
    path('customer/profile/',GetCreateUpdateProfile.as_view(),name='profile-view'),
    path('login/',UserLoginView.as_view(),name="user-login"),
    path('logout/',logout,name='user-logout'),
    path('password/',ChangePassword.as_view(),name='change-password'),
    path('customers/',GetCustomersRecord.as_view(),name='customer-record'),
    path("vendors/",GetVendorDetail.as_view(),name='vendor-detail'),
]