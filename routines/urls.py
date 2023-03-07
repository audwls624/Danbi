from django.urls import path
from . import views

urlpatterns = [
    path('info', views.RoutineInfoView.as_view(), name='info_view'),
]
