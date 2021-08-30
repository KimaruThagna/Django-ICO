from django.db import models
from ico.exceptions import InsufficientFundsInTreasuryException
from django.conf import settings

# Create your models here.


class TreasuryConfig(models.Model):
    bid_window = models.IntegerField(default=3)
    token_max_price = models.IntegerField(default=100)
    token_max_bid = models.IntegerField(default=1)
    treasury_supply = models.IntegerField(default=1000)
    @property
    def token_max_bid(self):
        return 0.01*self.treasury_supply
    
class Users(models.Model):
    name = models.CharField(max_length=50)
    registration_date = models.DateTimeField(auto_now_add=True)
    token_balance = models.FloatField(default=0.0)
    
    def __str__(self):
        return self.name
    
    def update_token_balance(self, amount):
        treasury = TreasuryConfig.objects.get(id=settings.TREASURY_CONFIG)
        if treasury.treasury_supply > amount: 
            # deduct tokens from treasury
            treasury.treasury_supply -= amount
            treasury.save()
            self.token_balance += amount #grant tokens
            self.save()
                
        else: # rare case when the treasury cant satisfy an order
            raise InsufficientFundsInTreasuryException('Treasury is out of Funds')
        
    
class Bid(models.Model):
    userid = models.ForeignKey(Users, on_delete=models.PROTECT)
    number_of_tokens = models.IntegerField()
    bidding_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    successful = models.BooleanField(default=False)
    
    def qualify_bid(self):
        self.successful = True
        self.save()
    