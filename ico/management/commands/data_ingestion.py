from django.core.management.base import BaseCommand
from ico.utils import *

def data_prep():
    generate_user_records()
    generate_bid_records()
    bid_records_same_price()
    token_assignment()
    
    
class Command(BaseCommand):

    def handle(self, *args, **options):
        data_prep()