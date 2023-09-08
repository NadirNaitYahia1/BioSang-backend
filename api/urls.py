from django.urls import path
from .  import views
urlpatterns = [
  path('user/login', views.loginUser),
  # path('', views.gettest),
  path('registerAdmin', views.RegisterAdmin),
  path('registerUser', views.RegisterUser),
  # path('logoutUser', views.logoutUser),
  path('getAnalyses', views.getAnalyses),
  # path('getAnalyses', views.getAnalyses),
  # --------------------------------------------ADMIN--------------------------------------------
  path('admin/login', views.loginAdmin),
]