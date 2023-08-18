from django.urls import path
from .import views

urlpatterns = [
    path('login/',views.LoginView.as_view(),name='login'),
    path('singup/',views.SingupView.as_view(),name='singup'),
    path('veryfy/',views.Veryfy_Singup_View.as_view(),name='veryfy'),
    path('logout/',views.LogoutView.as_view(),name='logout'),
    path('password_reset/',views.Password_Reset_User_View.as_view(),name='password_reset_form'),
    path('password_reset_done/',views.Password_Reset_Done_View.as_view(),name='password_reset_done'),
    path('password_reset_confirm/<uidb64>/<token>/',views.Password_Reset_Confirm_View.as_view(),name='password_reset_confirm'),
    path('password_reset_complete/',views.Password_Reset_Complete_View.as_view(),name='password_reset_complete'),
    # Api urls...
    path('login_api/',views.LoginAPIView.as_view(),name='login_api'),
    path('singup_api/',views.SingupAPIView.as_view(),name='singup_api'),
    path('user_list_create_api/',views.UserListCreateAPIView.as_view(),name='user_list_create_api'),
    path('user_retrieve_update_destroy_api/<int:pk>/',views.UserRetrieveUpdateDestroyAPIView.as_view(),name='user_retrieve_update_destroy_api'),

]
