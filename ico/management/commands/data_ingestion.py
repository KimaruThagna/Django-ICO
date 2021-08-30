from django.core.management.base import BaseCommand
from ico.utils import *

def data_prep():
    print("commencing")
    generate_user_records()
    generate_bid_records()
    bid_records_same_price()
    print("calling task")
    token_assignment() # will be a scheduled task
    
    
class Command(BaseCommand):

    def handle(self, *args, **options):
        data_prep()