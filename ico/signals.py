from django.db.models.signals import pre_save
from .models import Bid, TreasuryConfig
from datetime import datetime, timedelta
from django.conf import settings


treasury = TreasuryConfig.objects.get(id=settings.TREASURY_CONFIG)
def check_bid_window(sender, instance, **kwargs):
    if datetime.now() < timedelta(minutes=treasury.bid_window):
        instance.save()
    else:
        raise Exception("Bidding Closed")
    
pre_save.connect(check_bid_window, sender=Bid)