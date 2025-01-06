import datetime
import time

while True:
    hour = datetime.datetime.now().strftime("%H:%M:%S")
    print(f"\r", hour, end="")
    time.sleep(1)