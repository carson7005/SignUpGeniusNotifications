from util import notif_util as nutil
import time


def main():
    start = time.time()
    # nutil.send_hourly_notification(2, 1, include_when=True)
    nutil.send_weekly_notification()

    uptime = time.time() - start
    print(f"Uptime: {uptime}")


if __name__ == "__main__":
    main()
