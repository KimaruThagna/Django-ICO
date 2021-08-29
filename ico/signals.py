from django.db.models.signals import pre_save
from .models import Bid
from datetime import datetime, timedelta
from django.conf import settings



def check_bid_window(sender, instance, **kwargs):
    if datetime.now() < timedelta(minutes=settings.BID_WINDOW):
        instance.save()
    else:
        raise Exception("Bidding Closed")
    
pre_save.connect(check_bid_window, sender=Bid)