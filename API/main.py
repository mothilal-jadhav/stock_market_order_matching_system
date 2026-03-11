from fastapi import FastAPI
from engine.matching_engine import MatchingEngine
from api.routes import create_routes


app = FastAPI()
engine = MatchingEngine()

create_routes (app,engine)

