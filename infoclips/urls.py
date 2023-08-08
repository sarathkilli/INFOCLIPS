"""infoclips URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
# from django.conf.urls import url
from django.urls import path
from . import webapp,views

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.get_name,name="script"),
    path('summy/', views.get_summy,name="summy"),
    path('team/', views.get_team,name="team"),
    path('ajax-summary/', views.ajax_summary, name="ajax_summary"),
    path('ajax-search/', views.ajax_search, name="ajax_search"),
    path('ajax-sentiment/', views.ajax_sentiment, name="ajax_sentiment"),
]