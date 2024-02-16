from django.urls import path
from apiapp.views import home
urlpatterns = [
    path('', home),
]
