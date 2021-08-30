from django.conf import settings
from django.shortcuts import render
from .models import Bid, Users, TreasuryConfig
from django.conf import settings
# Create your views here.

treasury = TreasuryConfig.objects.get(id=settings.TREASURY_CONFIG)
def bid_data(request):
    con = {
        "bids": Bid.objects.all(),
       "window": treasury.bid_window,
       "balance": treasury.treasury_supply,
    }
    return render(request, 'ico/bid_data.html', context=con)


def user_data(request):
    con = {
        "users": Users.objects.all(),
        "window": treasury.bid_window,
        "balance": treasury.treasury_supply,
    }
    return render(request, 'ico/user_data.html', context=con)