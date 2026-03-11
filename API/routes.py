from fastapi import FastAPI
from pydantic import BaseModel
from engine.order import order,orderSide

class OrderRequest(BaseModel):
    side: str
    price: float
    quantity: int


def create_routes(app: FastAPI, engine):

    @app.post("/order")
    def submit_order(order: OrderRequest):

        side = orderSide.BUY if order.side.upper() == "BUY" else orderSide.SELL

        new_order = order(
            side=side,
            price=order.price,
            quantity=order.quantity
        )

        engine.submit_order(new_order)

        return {"message": "order received", "order_id": new_order.order_id}


    @app.get("/trades")
    def get_trades():
        return engine.trade_history
    
    @app.get("/orderbook")
    def get_orderbook():

        buy_orders = [
            {"price": o[2].price, "qty": o[2].quantity}
            for o in engine.order_book.buy_orders
        ]

        sell_orders = [
            {"price": o[2].price, "qty": o[2].quantity}
            for o in engine.order_book.sell_orders
        ]

        return {
            "buy_orders": buy_orders,
            "sell_orders": sell_orders
        }