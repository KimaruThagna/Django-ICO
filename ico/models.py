from django.db import models

# Create your models here.
class Users(models.Model):
    name = models.CharField(max_length=50)
    registraion_date = models.DateTimeField(auto_now_add=True)
    token_balance = models.FloatField(default=0.0)
    
    def update_balance(self, amount):
        self.token_balance += amount
        self.save()
    
class Bid(models.Model):
    userid = models.ForeignKey(Users, on_delete=models.PROTECT)
    number_of_tokens = models.IntegerField()
    bidding_price = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)
    succesful = models.BooleanField(default=False)
    
    def qualify_bid(self):
        self.succesful = True
        self.save()
    