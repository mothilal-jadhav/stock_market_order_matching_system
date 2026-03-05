'''
This maintains the market state

It stores all active buy and sell orders and ensures they follow price time priority, which is the rule used by most electronic exchanges such as the NSE of India

The objective is simple: always know the best buy price (bid) and best sell price (ask) efficiently. The correct data structure for this is a heap (priority queue)
Buy orders must prioritize highest price first, so they use a max heap
Sell orders must prioritize lowest price first, so they use a min heap
Python only provides a min-heap, so we simulate a max-heap by storing negative prices

'''
import heapq
from typing import List,Tuple
from engine.order import order, orderSide #This ensures that every entry in the order book follows the standardized order structure defined earlier

class orderBook: #represents the entire market order book for a single asset

    def __init__(self):
        self.buy_orders : List[Tuple[float,float,order]] = [] #stores buy orders
        self.sell_orders: List[Tuple[float, float, order]] = [] #stores sell orders

    def add_order(self, order:order):

        if order.side == orderSide.BUY:
            heapq.heappush(self.buy_orders,(-order.price,order.timestamp,order))

        if order.side == orderSide.SELL:
            heapq.heappush(self.sell_orders,(order.price,order.timestamp,order))

    def get_best_buy(self): #returns the highest bid order without removing it
        if not self.buy_orders:
            return None
        
        return self.buy_orders[0][2]
    
    def get_best_sell(self): #method returns the lowest ask order
        if not self.sell_orders:
            return None
        
        return self.sell_orders[0][2]
    
    def remove_best_buy(self):
        if self.buy_orders:
            heapq.heappop(self.buy_orders)

    def remove_best_sell(self):
        if self.sell_orders:
            heapq.heappop(self.sell_orders)

    #remove the top order from the heaps, These are necessary when an order is completely filled

    def has_orders(self): #checks whether both buy and sell sides contain orders, If either side is empty then matching cannot occur
        return len(self.buy_orders)>0 and len(self.sell_orders)>0
    
