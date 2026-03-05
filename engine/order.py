from dataclasses import dataclass, field
from enum import Enum
import time
import uuid


class orderSide(Enum):
    BUY = 'BUY'
    SELL = 'SELL'

class orderStatus(Enum):
    OPEN = 'OPEN'
    PARTIAL = 'PARTIAL'
    FILLED = 'FILLED'
    CANCELLED = 'CANCELLED'

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

