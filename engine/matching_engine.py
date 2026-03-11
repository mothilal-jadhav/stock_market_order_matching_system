'''
This file contains the core trading logic
The order book only stores orders, but the matching engine decides when a trade should occur and how much quantity should execute.
The matching engine continuously checks the best buy order and best sell order. 
If the buy price is greater than or equal to the sell price, a trade can execute.
Most exchanges use the rule:
Buy price >= Sell price -> trade executes
This ensures price compatibility between buyer and seller

'''

from engine.order_book import orderBook
from engine.order import order, orderSide
from database.db import SessionLocal
from database.models import Trade
import threading


class MatchingEngine:

    def __init__(self):
        self.order_book = orderBook() #Creates a new order book to store incoming orders
        self.trade_history = [] #Stores executed trades
        self.lock = threading.Lock()



    def submit_order(self,order:order): #Entry point for all orders coming from API, simulator, external trader
        with self.lock:
            self.order_book.add_order(order)
            self.match_orders()

        self.match_orders() #After inserting the order, the engine attempts to match it immediately

    def match_orders(self):
        while self.order_book.has_orders():

            best_buy = self.order_book.get_best_buy()
            best_sell = self.order_book.get_best_sell()
            '''
            These represent the highest bid and lowest ask
            The heap ensures this operation runs in O(1) time

            '''

            if best_buy.price<best_sell.price:
                break
            '''
            If the highest buyer is willing to pay less than the lowest seller wants, a trade cannot occur
            The engine stops matching
            '''

            trade_quantity = min(best_buy.quantity, best_sell.quantity)
            trade_price = best_sell.price
            '''
            Most exchanges execute trades at the resting order price
            If the seller placed the earlier order, the buyer accepts the sellers price

            '''

            trade = {
                'buy_order_id':best_buy.order_id,
                'sell_order_id':best_sell.order_id,
                'price':trade_price,
                'quantity':trade_quantity
            }

            self.trade_history.append(trade) #Adds the trade to the trade history log, Later this can be written to a database

            db = SessionLocal()

            db_trade = Trade(
                buy_order_id=best_buy.order_id,
                sell_order_id=best_sell.order_id,
                price=trade_price,
                quantity=trade_quantity
            )

            db.add(db_trade)
            db.commit()
            db.close()


            best_buy.reduce_quantity(trade_quantity)
            best_sell.reduce_quantity(trade_quantity)


            if best_buy.quantity == 0:
                self.order_book.remove_best_buy() #If the buyer has no shares left to buy, the order must leave the order book

            if best_sell.quantity == 0:
                self.order_book.remove_best_sell()
