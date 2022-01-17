from django.urls import path
from rest_framework_simplejwt.views import TokenRefreshView

from . import views

app_name = "account"

urlpatterns = [
    path('csrf/', views.GetCSRFToken.as_view(), name="api-csrf"),
    path('login/', views.LoginView.as_view(), name="login"),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('signup/', views.SignUpView.as_view(), name="signup"),
    path('logout/', views.LogoutView.as_view(), name="logout"),
    path('user/', views.CheckLoggedIn.as_view(), name="user"),
]
