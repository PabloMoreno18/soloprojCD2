"""main URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/2.2/topics/http/urls/
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
from .import views 

urlpatterns = [
    path('', views.index),
    path('register', views.create_user),
    path('login', views.user_login),
    path('dashboard', views.show_wall),
    path('create', views.add_game),
    path('new', views.new_game),
    path('add_comment/<int:id>', views.post_comment),
    path('show_one/<int:id>', views.one_game),
    path('show_one/<int:id>/update', views.update),
    path('show_one/<int:id>/delete', views.delete),
    path('delete/<int:id>', views.delete_comment),
    path('logout', views.sign_out)
]
