from dataclasses import dataclass, field 
'''
-> dataclass automatically generates boilerplate code such as __init__, __repr__ and equality comparisions otherwise we haev to manually write these methods
-> field allows configuration of how a variable behaves inside the dataclass, such as automatically generating values
'''

from enum import Enum
'''
-> Enum restricts variables to predefined constant values
-> Instead of allowing random strings like "buy" "BUY" "Buy" "purchase", the system forces the order side to be one of two valid values
-> This prevents invalid states inside the system
'''

import time
'''
Orders need timestamps because most exchanges follow the price time priority rule

When two orders have the same price, the order that arrived earlier must execute first. The timestamp enables that comparison
'''


import uuid
'''
every order must have unique identifires, hence uuid module generates globbaly unique id so that every order can be tracked reliably across the system. in real world every order has a unique refernce number
'''



class orderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

'''
Defines the direction of the order.
BUY - Trader wants to purchase shares.
SELL - Trader wants to sell shares.
Using an enum guarantees that the system only accepts these two states.

'''

class orderStatus(Enum):
    OPEN = 'OPEN'
    PARTIAL = 'PARTIAL'
    FILLED = 'FILLED'
    CANCELLED = 'CANCELLED'

'''
Tracks the lifecycle of an order
OPEN - Order is waiting in the order book

PARTIAL - Some quantity was executed but the order still has remaining shares

FILLED - The order has been completely executed

CANCELLED - The trader removed the order before execution

This is important for logging and trade history
'''

@dataclass
class order:
    side:orderSide
    price:float
    quantity:int
    order_id: str = field(default_factory=lambda: str(uuid.uuid4()))
    timestamp: float = field(default_factory=time.time)
    status: orderStatus = orderStatus.OPEN

    def __post_init__(self):
        if self.price <= 0:
            raise ValueError("Price must be positive")
        
        if self.quantity <= 0:
            raise ValueError('Quantity must be positive')
        

    def reduce_quantity(self,qty):
        if qty > self.quantity:
            raise ValueError('trade quantity exceeds order quantity')
        
        self.quantity -= qty

        if self.quantity == 0:
            self.status = orderStatus.FILLED

        else:
            self.status = orderStatus.PARTIAL

