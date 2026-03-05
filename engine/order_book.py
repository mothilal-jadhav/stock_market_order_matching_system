'''
This maintains the market state

It stores all active buy and sell orders and ensures they follow price time priority, which is the rule used by most electronic exchanges such as the NSE of India

The objective is simple: always know the best buy price (bid) and best sell price (ask) efficiently. The correct data structure for this is a heap (priority queue)
Buy orders must prioritize highest price first, so they use a max heap
Sell orders must prioritize lowest price first, so they use a min heap
Python only provides a min-heap, so we simulate a max-heap by storing negative prices

'''
