from util import notif_util as nutil
import time


def main():
    start = time.time()
    # nutil.send_weekly_notification()
    nutil.send_notification(days_out=1, include_full=False, include_when=True)

    uptime = time.time() - start
    print(f"Uptime: {uptime}")


if __name__ == "__main__":
    main()
