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