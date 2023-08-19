from django.urls import path
from .  import views
urlpatterns = [
  path('', views.gettest),
  # path('login', views.login),
  path('registerAdmin', views.RegisterAdmin),
  path('registerUser', views.RegisterUser),
  path('login', views.loginUser),
  path('logoutUser', views.logoutUser),
  path('getPatient', views.user),
  path('getAnalyses', views.getAnalyses),
]