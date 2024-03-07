from django.conf.urls.static import static
from django.conf import settings
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView
from rest_framework import routers
from django.shortcuts import get_object_or_404
from . import views
from administrator import views as admin_views

router=routers.DefaultRouter()

# router.register('consumers',views.ConsumerViewSet,basename='consumers')
# router.register('customuser',views.CustomUserViewSet,basename='customuser')
router.register('userslist',views.ViewUsers,basename='users_list')

urlpatterns=[
    
    path('',include(router.urls)),
    
    path('token/verify/', views.MyTokenVerifyView.as_view(), name='token_verify'),
    
    
    path('user_registration',views.UserRegistration.as_view(),name='user_reg'),
    
    path('user-login',views.LoginView.as_view(),name='user_login'),
    
    path('login_page',views.dologin,name='login_page'),
    path('register_page',views.register,name='register_page'),
    path('check_mail',views.check_mail,name='check_mail'),
    path('forgot_password',views.forgot_password,name='forgot_password'),
    path('do_logout',views.dologout,name='do_logout'),
    
]+ static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)