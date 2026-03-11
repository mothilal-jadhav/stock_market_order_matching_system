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
          |  order.py
          |  order_book.py
          |  matching_engine.py
          |
        api/
          |   routes.py
          |   main.py
          |
        simulator/
          |  trader_simulation.py
          |
        database/
          |  models.py
          |
        benchmark/
          |  load_test.py
          |
        README.md
        Dockerfile
        requirements.txt



ENGINE LAYER
This is the **core trading system**. It contains the logic that actually runs the exchange.

order.py
This file defines the **Order object**, which is the fundamental unit in trading.

An order represents a trader’s instruction to buy or sell a security. Every order contains fields such as:

* order_id
* order_type (buy/sell)
* price
* quantity
* timestamp

The matching engine and order book operate only on these objects. Without a standardized order structure, the system cannot process trades consistently.

Typical contents:

* Order class definition
* validation rules
* utility functions (e.g., serialization)

Purpose:
Standardize the structure of incoming trade orders.

order_book.py

The order book represents the **market state**.

It stores all active orders that have not yet been executed.

In real exchanges such as the NSE India, the order book is the core structure that determines price discovery.

This file typically contains:

* buy order heap (max heap)
* sell order heap (min heap)
* functions to add/remove orders
* functions to retrieve best bid and ask

Responsibilities:

* maintain pending orders
* maintain price priority
* maintain time priority

Without this file the exchange cannot determine which orders should execute first.


matching_engine.py

This file contains the **trade execution logic**.

The matching engine continuously checks whether a buy order and a sell order can be matched.

Example condition:


buy_price >= sell_price


When a match occurs, this file executes the trade and updates the order book.

Responsibilities:

* trade execution
* partial fills
* order removal
* trade logging

This file represents the **heart of the exchange**.

If order_book stores market data, the matching engine decides **when trades occur**.


API LAYER

The library used will be FastAPI. It is widely used for backend services because it is simple and fast

The API layer allows external users/trading bots to interact with the exchange.

routes.py

This file defines the HTTP endpoints.

Typical endpoints:

POST /order
Submit buy or sell order.

GET /orderbook
Return current market depth.

GET /trades
Return executed trades.

Responsibilities:

* receive requests
* validate inputs
* pass orders to matching engine
* return results to clients

Without this layer the engine would only run locally and would not accept external orders.


main.py

This is the **application entry point**.

It starts the web server and loads the API.

Typical responsibilities:

* initialize FastAPI application
* register routes
* configure middleware
* start server

Example command that uses this file:


uvicorn main:app

Without this file the API cannot start.

current architecture:

    Client
    |
    FastAPI
    |
    MatchingEngine
    |
    OrderBook
    |
    Trade Execution


SIMULATION LAYER

trader_simulation.py

A real exchange processes thousands of traders simultaneously.

Since you will not have real traders using your system, this file **simulates market activity**.

Typical functionality:

* generate random buy/sell orders
* simulate market volatility
* send orders to API


Purpose:

* test system behavior
* simulate heavy trading activity
* generate performance data

**Results** after creating some basic pipeline of 

run_simulation.py
        |
TraderSimulator
        |
MatchingEngine
        |
OrderBook
        |
Trade execution


Simulation complete
Orders processed: 10000
Trades executed: 7642
Time taken: 0.04636192321777344 seconds


DATABASE LAYER

models.py

This file defines the **database schema**.

Executed trades and order history must be stored.

Typical tables:

orders
trades

Example fields:

order_id
price
quantity
timestamp
status



Purpose:

* persist historical trades
* store audit logs
* allow analytics queries

Real exchanges store massive trade histories.


PERFORMANCE LAYER

load_test.py

This file performs **stress testing**.

It measures how the system behaves under heavy load.

Example tests:

* orders per second
* latency per trade
* throughput under concurrency


Purpose:

* prove system scalability
* measure performance bottlenecks
* produce benchmark charts for GitHub


PROJECT METADATA FILES

README.md

This file explains the project.

Contents usually include:

* system architecture
* design decisions
* setup instructions
* performance metrics


Dockerfile

This file packages the entire system into a container.

It ensures the project runs the same way on any machine.

Example usage:

docker build 
docker run


Purpose:

* environment reproducibility
* deployment
* simplified setup

Most production backend systems are containerized.


requirements.txt

This file lists all Python dependencies.

Example:

fastapi
uvicorn
redis
sqlalchemy
pandas


Purpose:

Allows others to install dependencies with one command.

