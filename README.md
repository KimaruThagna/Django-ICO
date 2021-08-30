# ICO in Django
The project demonstrates an ICO by triggering bids via a dummy operator. Once the bid window closes, the `token_assignment()`, a scheduled background task that runs after the `bid_window`,  executes the auction logic which is as follows
## Auction Logic: Approach and Compromises
To simulate an actual bidding process, I have incorporated randomized `time.sleep()` to allow bid data to be added at different times with pauses in between records. This allows me to later on sort the bids by the time they were placed. The pauses are from 1 to 10 seconds for simulation purposes. In a real world situation, this would not be the case. The pauses therefore means that the bidding process will take some time before the application is fully functional and data is available.

The `TreasuryConfig` model holds configuration data such as bidding window, maximum token supply and tokens per bid. This method allows code flexibility where one can add other configurations and reference them instead. The current configuration is referenced in the `settings.py` file.

Bidding window is set in minutes for practicality. In an ideal situation, the window would be set to days or months into the future. Before every bid is commited to the database, it is checked against the bid window by use of `pre_save()` Django signals. Only bids submitted before the end of the biding window will be considered

The maximum number of tokens a user can place in a bid is 1% of the total treasury supply it also allows the maximization of the possibility of all bids being fulfilled. This prevents very large bids that might _hoard_ and not allow other bid participants to participate

Precedence is given to the highest bidder. They are given the total number of tokens they requested.

* In the problem statement, only the max bidder and the price groups were recognized. All the other bidders were not catered for. To remedy this, assumptions and compromises were made as follows.

All the rest of the bids are fulfilled in a first come first serve basis. The earliest bid with the best price gets fulfilled in full. This better mimics a real world auction and allows for succuessful/unsuccesful bids and succesful/unsucessful users who did not receive any tokens, which is expected/anticipated according to the problem statement.

## Possible alternative
All the rest of the bids are fulfilled in a round robin fashion, assigning 1 token in each round until either the `treasury_supply` is depleted or all bids are fulfilled. The bids are ordered in order of the timestamp where the earliest bid is given preference. A first come first serve basis. A sample is demonstrated below

``` python

        remaining_bids = Bid.objects.objects.exclude(id__in=[bid.id for bid in max_bid]).orderby('timestamp')
        bid_fulfilled = []
        while settings.TREASURY_SUPPLY > 0 or len(bid_fulfilled) < len(remaining_bids): # go on as long as supply exists or bidders are yet to be satisfied
            for bid in remaining_bids:
                if bid.userid.token_balance < bid.number_of_tokens: # as long as user's bid request is not fulfilled
                    bid.userid.update_token_balance(1)
                else: #bid has been fulfilled
                    bid_fulfilled.append(True)
        
```

 This approach closely mimics the problem statement in the document but without the price groups. The compromise made was the simplicity of a round robin solution in favor of the computational expense (execution time and memory)that would be incurred in:
1. Identifying price groups and collecting them as a list(final data structure) of lists(price groups) of dictionaries(bid records)
2. sorting price groups(lists of dictionaries) by date and sorting the list of lists of dictionaries by price. ie, the higher price group comes first.
3. Looping through price groups, assigning tokens, checking for number of tokens requested and `popping` the bid record if token request is fulfilled until the treasury is depleted or all bids are fulfilled.

This approach however does not guarantee the existence of unsuccessful bids or users, which is anticipated(expected in a real auction), because each bid is fulfilled in a round robin fashion. The only way it can occur is if the max bidder is awarded a large amount of tokens and the remaining bids are a huge number such that the last bidders may not get a single token due to insufficient treasury funds.

# Running the Project
1. Install dependencies py running the command `pip3 install -r requirements.txt`
2. Run the data ingestion management command `python3 manage.py data_ingestion`
3. Run the task processing command `python manage.py process_tasks`
4. On a separate terminal, Run the server `python3 manage.py runserver` and navigate to http://127.0.0.1:8000 for bids and http://127.0.0.1:8000/users/ for user data. To see results, refresh after 4 minutes since the auction logic is executed after the bid window closes.