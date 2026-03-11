'''
The random module generates realistic market behaviour. Real markets contain random price levels and order sizes. This module allows the simulator to mimic that


The time module measures how long the simulation takes. This is necessary for throughput analysis


The MatchingEngine is imported so the simulator can inject orders directly into the system


The Order and OrderSide classes are imported to create valid orders compatible with the engine
'''

import time
import random
from concurrent.futures import ThreadPoolExecutor

from engine.matching_engine import MatchingEngine
from engine.order import order, orderSide

'''
TraderSimulator class represents a simplified market environment, this object generates synthetic orders

The generate_random_order function creates one synthetic order 
It randomly decides whether the order is BUY or SELL
The price is sampled from a uniform range between 95 and 105
The quantity is randomly selected between 1 and 100

This randomness creates realistic market pressure where some orders match immediately and others remain pending
'''
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
    def submit_order(self):
        order = self.generate_random_order()
        self.engine.submit_order(order)

    def run_concurrent_simulation(self, num_orders=10000, num_threads=10):

        start = time.time()

        with ThreadPoolExecutor(max_workers=num_threads) as executor:
            for _ in range(num_orders):
                executor.submit(self.submit_order)

        end = time.time()

        duration = end - start

        print("Concurrent Simulation Complete")
        print("Orders processed:", num_orders)
        print("Threads used:", num_threads)
        print("Trades executed:", len(self.engine.trade_history))
        print("Time taken:", duration)
        print("Throughput:", num_orders / duration, "orders/sec")