"""
URL configuration for project project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.2/topics/http/urls/
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
from django.urls import path, include
from login.views import LoginView, LogoutView, CreateAccountView
from store.urls import router as cart_router, wish_router


urlpatterns = [
    path('admin/', admin.site.urls),
    path('other/', include('other.urls')),
    path('', include('store.urls')),
    path('login/', LoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(), name="logout"),
    path('create/', CreateAccountView.as_view(), name="create"),
    path('api/', include(cart_router.urls)),
    path('api1/', include(wish_router.urls))
]
