from django.db import models
from exceptions import InsufficientFundsInTreasuryException
from django.conf import settings

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=50)
    registraion_date = models.DateTimeField(auto_now_add=True)
    token_balance = models.FloatField(default=0.0)
    
    def update_token_balance(self, amount):
        if settings.TREASURY_SUPPLY > amount: 
            # deduct tokens from treasury
            settings.TREASURY_SUPPLY -= amount
            self.token_balance += amount
            self.save()
                #grant tokens
        else: # rare case when the treasury cant satisfy an order
                raise InsufficientFundsInTreasuryException('Treasury is out of Funds')
        
    
class Bid(models.Model):
    userid = models.ForeignKey(Users, on_delete=models.PROTECT)
    number_of_tokens = models.IntegerField()
    bidding_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    succesful = models.BooleanField(default=False)
    
    def qualify_bid(self):
        self.succesful = True
        self.save()
    