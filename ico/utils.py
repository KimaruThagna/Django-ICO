from random import randint
from faker import Faker
from models import Users, Bid
from django.conf import settings

faker = Faker()

def generate_user_records(number_of_records=10):
    for i in range(number_of_records):
        data = {"name":faker.name()}
        Users.objects.create(**data)
        
        
        
def generate_bid_records(number_of_records=100):
     for i in range(number_of_records):
        data = {"userid":randint(1,len(Users.objects.all())),
                "number_of_tokens":randint(1,settings.TOKEN_MAX_PER_BID),
                "bid_price":randint(10,settings.TOKEN_MAX_PRICE),
                }
        Bid.objects.create(**data)
        
def bid_records_same_price(number_of_records=10):
     for i in range(number_of_records):
        data = {"userid":randint(1,len(Users.objects.all())),
                "number_of_tokens":randint(1,settings.TOKEN_MAX_PER_BID),
                "bid_price":40,
                }
        Bid.objects.create(**data)
