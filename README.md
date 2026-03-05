# Objective

To stimulate how exchanges such as NSE of india match buy and sell orders in real time

when trader places orders the exchange must continous and maintain an order book

buy orders and sell orders arrive asynchronously, so a matching system decides wheather a trade should execute immediately or remain pending

it works on a simple rule that is 

            if buy_price >= best selling price; then buy order
            if sell_price <= best buy price; then sell order

the matching order must process thousands of orders per secind while maintaining fairness and low latency.



# System Architecture

                        client (Trader)
                           |
                        REST API (Fast API)
                           |
                    Matching Engine
                           |
                        Order Book
                        /    |   \
                    Buy Heap |  Sell Heap
                             |
                        Trade Logger
                             |
                        Database

Core Modules will be:

    Order Gateway       : Recieves order through an API
    Matching Engine     : Matches incoming Orders
    Order Book          : maintains Buy and Sell orders
    Trade Logger        : Stores Executed Orders
    Persistance layer   : sttores ordered trades


# Key Data Strucutres

Engine Relies on Two priority Queues

1. Max Heap for buying orders
2. Min Heap for selling orders

Heaps will store Tuples: 

1. Buy heap -> (-price, timestamp, order) {-ve price converts python min_heap into max_heap}
2. sell heap -> (price, timestamp, order)

order objects will be like :- 

        class order:
            def __init__(self,order_id,side,price,quality,timestamp):
                self.order_id = order_id
                self.side = side
                self.price = price
                self.quantity = quantity
                self.timestamp = timestamp

# matching algorithm

every time a new order arrives engine checks if a match exists

Pseudo code for matching system:

        while buy_heap aand sell_heap:
            best_buy = highest buy price
            best_sell = lowest sell price

            if best_buy.price >= best_sell.price:
                execute trade
            else:
                break

trading_quantity = min(buy_order.qty, sell_order.qty)

After execution:
-> reduce remaining quantity
-> remove order if quantity becomes zero
-> push partially filled order back to heap

Example Python Skeleton
Basic matching engine structure:

    import heapq
    import time

    buy_heap = []
    sell_heap = []

    def add_buy(order):
        heapq.heappush(buy_heap, (-order.price, order.timestamp, order))

    def add_sell(order):
        heapq.heappush(sell_heap, (order.price, order.timestamp, order))

    def match_orders():

        while buy_heap and sell_heap:

            buy = buy_heap[0][2]
            sell = sell_heap[0][2]

            if buy.price >= sell.price:

                trade_qty = min(buy.quantity, sell.quantity)

                print("Trade executed:", trade_qty, "shares at", sell.price)

                buy.quantity -= trade_qty
                sell.quantity -= trade_qty

                if buy.quantity == 0:
                    heapq.heappop(buy_heap)

                if sell.quantity == 0:
                    heapq.heappop(sell_heap)

            else:
                break

till here a very basic order matching has been done

now adding extra features will turn it into some advanced version and close to NSE style order matching which works on large datasets and asynchrnous orders.

to counter these many orders we can have CONCURRENCY SIMULATION to simulate many trades

our metric to test wheather the project performance is good will be based on latency so lets set the metric as avg matching latency and orders processed per second

all the trades that are haooening have to be stored somewhere hence lets use MySQL database for it

and test the latency by stress testing large bust of orders


lets build this project in a clean layout of 

stock-exchange-engine

engine/
    order.py
    order_book.py
    matching_engine.py

api/
    routes.py
    main.py

simulator/
    trader_simulation.py

database/
    models.py

benchmark/
    load_test.py

README.md
Dockerfile
requirements.txt