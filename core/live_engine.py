import time
from core.scanner import scan_market
from database.trades import save_signal
from config.settings import SCAN_INTERVAL
from ml.learning import train_model

def start_engine():

    print("AI Engine iniciado")

    while True:

        signals=scan_market()

        for s in signals:

            save_signal(s)

        train_model()

        time.sleep(SCAN_INTERVAL)
