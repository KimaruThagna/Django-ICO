
from django.urls import path
from views import bid_data, user_data
urlpatterns = [
    path('', bid_data, name="bid_data"),
    path('/users/', user_data, name="user_data")
]
