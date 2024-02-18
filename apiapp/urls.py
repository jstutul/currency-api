from django.urls import path
from apiapp.views import home,current_rate_api,insert_reviews_data,current_rate
urlpatterns = [
    path('', home),
    path('current_rate', current_rate_api, name='current_rate_api'),
    path('current_review', insert_reviews_data, name='current_review'),
    path('rates', current_rate, name='rates'),
]
