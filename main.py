import notif_util as nutil
import schedule
import time


def main():
    schedule.every().hour.do(
            nutil.send_hourly_notification(2, True))
    schedule.every().monday.at("8:00").do(
            nutil.send_daily_notification(7))

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()

