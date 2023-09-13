from datetime import datetime
import os

def log(message):
    now = datetime.now()
    current_time = now.strftime("%m/%d/%Y %H:%M:%S")
    log_message = f"[{current_time}]: {message}"
    if not os.path.exists("logs/"):
        os.mkdir("logs/")

    with open("logs/latest.txt", "a") as log_file:
        log_file.write("\n" + log_message)

    print(log_message)


def handle_logger_close():
    now = datetime.now()
    current_date = now.strftime("%m_%d_%Y")
    if not os.path.exists("logs") or \
        not os.path.exists("logs/latest.txt"):
            return
    
    other_count = 0
    for log_file in os.listdir("logs"):
        if current_date in log_file: other_count += 1

    os.rename("logs/latest.txt", f"logs/{current_date}{'_' + str(other_count) if other_count > 0 else ''}.txt")

