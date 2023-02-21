from django.urls import path

from . import views

urlpatterns = [
    path('<str:sub>/<int:pageno>/', views.ani, name='ani'),
    path("bref/<path:url>/", views.brefani, name='brefani'),
]

