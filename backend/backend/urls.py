"""
URL configuration for backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from api.views import RegisterView, LoginView, get_user, TextListView, AddTextView, DeleteTextView, UpdateTextView, RandomTextView, SaveResultView, GetResultsView
from rest_framework_simplejwt.views import TokenRefreshView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/register/', RegisterView.as_view(), name='register'),
    path('api/login/', LoginView.as_view(), name='login'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/getUser/', get_user, name='get_user'),
    path('api/textList/', TextListView.as_view(), name='texts'),
    path('api/randomText/', RandomTextView.as_view(), name='random_text'),
    path('api/addText/', AddTextView.as_view(), name='add_text'),
    path('api/deleteText/', DeleteTextView.as_view(), name='delete_text'),
    path('api/updateText/', UpdateTextView.as_view(), name='update_text'),
    path('api/saveResult/', SaveResultView.as_view(), name='save_result'),
    path('api/getResults/', GetResultsView.as_view(), name='get_result'),
]
