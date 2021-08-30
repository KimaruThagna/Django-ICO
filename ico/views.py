from django.shortcuts import render
from .models import Bid, Users
# Create your views here.


def bid_data(request):
    con = {
        "bids": Bid.objects.all()
    }
    return render(request, 'ico/bid_data.html', context=con)


def user_data(request):
    con = {
        "users": Users.objects.all()
    }
    return render(request, 'ico/user_data.html', context=con)