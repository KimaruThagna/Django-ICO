import time
from datetime import timedelta
from random import randint
from django.conf import settings
from faker import Faker
from .models import Users, Bid, TreasuryConfig
from django.db.models import Max
import logging
from background_task import background

faker = Faker()

treasury = TreasuryConfig.objects.get(id=settings.TREASURY_CONFIG)

def generate_user_records(number_of_records=5):
    logging.info(">>>>>>>>>>Generating User Data")
    for i in range(number_of_records):
        data = {"name":faker.name()}
        Users.objects.create(**data)
        
        
        
def generate_bid_records(number_of_records=3):
     logging.info(">>>>>>>>>>Generating Bids")
     for i in range(number_of_records):
        data = {"userid":Users.objects.get(id=randint(1,len(Users.objects.all()))),
                "number_of_tokens":randint(1,treasury.token_max_bid),
                "bidding_price":randint(10,treasury.token_max_price),
                }
        time.sleep(randint(1,5)) # allow bids to have different registered times 
        #so to allow sorting out by time
        Bid.objects.create(**data)
        
def bid_records_same_price(number_of_records=2):
     logging.info(">>>>>>>>>>Generating User Data with same price")
     for i in range(number_of_records):
        data = {"userid":Users.objects.get(id=randint(1,len(Users.objects.all()))),
                "number_of_tokens":randint(1,treasury.token_max_bid),
                "bidding_price":40,
                }
        time.sleep(randint(1,5)) # allow bids to have different registered times 
        #so to allow sorting out by time
        Bid.objects.create(**data)

@background(schedule=timedelta(minutes=treasury.bid_window))
def token_assignment():
        
        logging.info(">>>>>>>>>>Executing Auction Logic on Bids")
        # give the max bid the number of tokens they bid for
        max_bid_price = Bid.objects.aggregate(Max('bidding_price'))['bidding_price__max']
        max_bid = Bid.objects.filter(bidding_price=max_bid_price)
        for bid in max_bid: # could be a single item or list of bids with max price
            bid.userid.update_token_balance(bid.number_of_tokens)
            bid.qualify_bid()
        # award tokens to the rest of the bids
        
        remaining_bids = Bid.objects.exclude(id__in=[bid.id for bid in max_bid]).order_by('timestamp', '-bidding_price')    
        for bid in remaining_bids:
            bid.userid.update_token_balance(bid.number_of_tokens)
            bid.qualify_bid()
                
                
        