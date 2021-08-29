# ICO in Django
The project demonstrates an ICO by triggering bids via a dummy operator. Once the bid window closes, the `token_assignment()` executes the auction logic which is as follows
## Auction Logic: Approach and Compromises
The maximum number of tokens a user can place in a bid is 1% of the total treasury supply. This prevents very large bids that might _hoard_ and not allow other bid participants to participate

Precedence is given to the highest bidder. They are given the total number of tokens they requested.

* In the problem statement, only the max bidder and the price groups were recognized. All the other bidders were not catered for. To remedy this, assumptions and compromises were made as follows.

All the rest of the bids are fulfilled in a first come first serve basis. The earliest bid with the best price gets fulfilled in full. This better mimics a real world auction and allows for succuessful/unsuccesful bids and succesful/unsucessful users who did not receive any tokens, which is expected/anticipated.

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

 This approach closely mimics the problem statement in the document but without the price groups. The compromise made was the simplicity of a round robin solution in favor of the computational expense (execution and memory)that would be incurred in:
1. Identifying price groups and collecting them as a list of lists of dictionaries
2. sorting price groups(lists of dictionaries) by date and sorting the list of lists of dictionaries by price. ie, the higher price group comes first.
3. Looping through price groups, assigning tokens, checking for number of tokens requested and `popping` the bid record if token request is fulfilled until the treasury is depleted or all bids are fulfilled.

This approach however does not guarantee the existence of unsuccessful bids or users, which is anticipated(expected in a real auction), because each bid is fulfilled in a round robin fashion. The only way it can occur is if the max bidder is awarded a large amount of tokens and the remaining bids are a huge number such that the last bidders may not get a single token due to insufficient treasury funds.
