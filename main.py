import notif_util as nutil
import schedule
import time

def hourly_job():
    nutil.send_hourly_notification(2, True)
    print("Hourly job done.")

def daily_job():
    nutil.send_daily_notification(7)
    print("Daily jon done.")

def main():
    schedule.every().hour.at(":05").do(hourly_job)
    schedule.every().monday.at("08:00").do(daily_job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    main()

