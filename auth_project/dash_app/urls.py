from django.urls import path, include
from .views import DashView, StudentProfile, AttendenecView, dash_home, graph_explained, attendence_graph
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('dash_home/', DashView.as_view(), name='dash_home'),
    path('student_profile', StudentProfile.as_view(), name='student_profile'),
    path('dash_home_graph/', dash_home, name='dash_home_graph'),
    path('graph_explained/', graph_explained, name='graph_explained'),
    path('attendence_update/', AttendenecView.as_view(), name='attendence_update'),
    path('attendence_graph/', attendence_graph, name='attendence_graph'),
    # path('try/', try_function, name='try')
]