'''
The random module generates realistic market behaviour. Real markets contain random price levels and order sizes. This module allows the simulator to mimic that


The time module measures how long the simulation takes. This is necessary for throughput analysis
'''

import time
import random

from engine.matching_engine import MatchingEngine
from engine.order import order, orderSide

class TradeSimulator:
    def __init__(self, engine: MatchingEngine):
        self.engine = engine

    def generate_random_order(self):

        side = random.choice([orderSide.BUY, orderSide.SELL])

        price = round(random.uniform(95, 105), 2)

        quantity = random.randint(1, 100)

        return order(
            side=side,
            price=price,
            quantity=quantity
        )
    
    def run_simulation(self, num_orders=1000):

        start_time = time.time()

        for _ in range(num_orders):

            order = self.generate_random_order()

            self.engine.submit_order(order)

        end_time = time.time()

        duration = end_time - start_time

        print("Simulation complete")
        print("Orders processed:", num_orders)
        print("Trades executed:", len(self.engine.trade_history))
        print("Time taken:", duration, "seconds")