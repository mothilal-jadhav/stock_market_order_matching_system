'''
This file contains the core trading logic
The order book only stores orders, but the matching engine decides when a trade should occur and how much quantity should execute.
The matching engine continuously checks the best buy order and best sell order. 
If the buy price is greater than or equal to the sell price, a trade can execute.
Most exchanges use the rule:
Buy price >= Sell price -> trade executes
This ensures price compatibility between buyer and seller

'''