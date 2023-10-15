from django.urls import path
from authy import views
from django.contrib.auth import views as auth_views


urlpatterns = [
    # app views
    path('sign-up/',views.sign_up, name = 'sign-up'),
    path('change-password', views.change_password, name ='change_password'),
    path('change-password-done', views.change_password_done, name ='change_password'),

    # authentifications views
    
    path('', auth_views.LoginView.as_view(), name='login'),
    
    path('sign-out/', auth_views.LogoutView.as_view(), name='sign-out'),
    
    path('passwordreset/', auth_views.PasswordResetView.as_view(),
        name='password_reset'
    ),

    path('passwordreset/done/', 
        auth_views.PasswordResetDoneView.as_view(),
        name='password_reset'
    ),
    
    path('passwordreset/<uidb64>/<token>/', 
        auth_views.PasswordResetConfirmView.as_view(),
        name='password_reset_confirm'
    ),
    
    
]
