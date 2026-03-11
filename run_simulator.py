from engine.matching_engine import MatchingEngine
from Simulator.trade_simulation import TradeSimulator


def main():

    engine = MatchingEngine()

    simulator = TradeSimulator(engine)

    simulator.run_simulation(10000)

if __name__== "__main__":
    main()

    