import time
from random import randint
from faker import Faker
from models import Users, Bid
from django.conf import settings
from django.db.models import Max

faker = Faker()



def generate_user_records(number_of_records=10):
    for i in range(number_of_records):
        data = {"name":faker.name()}
        Users.objects.create(**data)
        
        
        
def generate_bid_records(number_of_records=50):
     for i in range(number_of_records):
        data = {"userid":randint(1,len(Users.objects.all())),
                "number_of_tokens":randint(1,settings.TOKEN_MAX_PER_BID),
                "bid_price":randint(10,settings.TOKEN_MAX_PRICE),
                }
        time.sleep(randint(1,10)) # allow bids to have different registered times 
        #so to allow sorting out by time
        Bid.objects.create(**data)
        
def bid_records_same_price(number_of_records=10):
     for i in range(number_of_records):
        data = {"userid":randint(1,len(Users.objects.all())),
                "number_of_tokens":randint(1,settings.TOKEN_MAX_PER_BID),
                "bid_price":40,
                }
        time.sleep(randint(1,10)) # allow bids to have different registered times 
        #so to allow sorting out by time
        Bid.objects.create(**data)

def token_assignment():
        # give the max bid the number of tokens they bid for
        max_bid_price = Bid.objects.aggregate(Max('bidding_price'))['bidding_price__max']
        max_bid = Bid.objects.filter(bidding_price=max_bid_price)
        for bid in max_bid: # could be a single item or list of bids with max price
            bid.userid.update_token_balance(bid.number_of_tokens)
            bid.qualify_bid()
        # award tokens to the rest of the bids
        
        remaining_bids = Bid.objects.objects.exclude(id__in=[bid.id for bid in max_bid]).order_by('timestamp', '-bidding_price')
        while settings.TREASURY_SUPPLY > 0 : # go on as long as supply exists
            for bid in remaining_bids:
                bid.userid.update_token_balance(bid.number_of_tokens)
                bid.qualify_bid()
                
                
        