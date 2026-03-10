from threading import Thread
from core.live_engine import start_engine

def run():

    start_engine()

Thread(target=run).start()
