from django.urls import path
from . import views

urlpatterns = [
    path('', views.HomeView.as_view(), name='home_page'),
    path('about-us/', views.AboutUsView.as_view(), name='about_us_page'),
    path('about-us/service/', views.ServiceView, name='services_page'),
    path('about-us/agent/', views.AgentView, name='agent_page')
]
