import time
from core.scanner import scan_market
from database.trades import save_signal

SCAN_INTERVAL = 20


def start_live_engine():

    print("AI Live Engine Started")

    while True:

        try:

            signals = scan_market()

            for signal in signals:

                save_signal(signal)

                print(
                    f"Signal {signal['symbol']} "
                    f"{signal['direction']} "
                    f"{signal['confidence']}%"
                )

        except Exception as e:

            print("Engine error:", e)

        time.sleep(SCAN_INTERVAL)
