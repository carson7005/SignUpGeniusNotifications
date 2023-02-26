import notif_util as nutil
import time


def main():
    start = time.time()
    nutil.send_daily_notification(7)

    uptime = time.time() - start
    print(f"Uptime: {uptime})


if __name__ == "__main__":
    main()
