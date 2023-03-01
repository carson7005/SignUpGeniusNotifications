from datetime import datetime

def log(message):
    now = datetime.now()
    current_time = now.strftime("%H:%M:%S")
    print(f"[{current_time}]: {message}")

