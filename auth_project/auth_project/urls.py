# # myproject/urls.py
# from django.contrib import admin
# from django.urls import path, include

# urlpatterns = [
#     path('admin/', admin.site.urls),
#     path('auth/', include('auth_app.urls')),
# ]

from django.contrib import admin
from django.urls import path, include
from django.shortcuts import render
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('auth/', include('auth_app.urls')),
    path('dash/', include('dash_app.urls')),
    path('django_plotly_dash/', include('django_plotly_dash.urls')),  # Note: django_plotly_dash not a name of your app, it's referring to the inner namespace of this library.
    path('', views.home, name='home'),
]
