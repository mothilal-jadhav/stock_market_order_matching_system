import time
from engine.matching_engine import MatchingEngine
from Simulator.trade_simulation import TradeSimulator

engine = MatchingEngine()
simulator = TradeSimulator(engine)

start = time.time()

simulator.run_simulation(50000)

end = time.time()
duration = end - start

print("Benchmark Results")
print("Time:", duration)
print("Orders/sec:", 50000/duration)
print("Trades:", len(engine.trade_history))