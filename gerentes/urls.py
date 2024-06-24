from django.urls import path 
from . import views
urlpatterns = [
    path('',  views.gerentes, name= 'gerentes')
]