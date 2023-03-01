import notif_util as nutil
import schedule
import time
import log_util as lutil

def hourly_job():
    nutil.send_hourly_notification(2, 1,include_when=True)
    lutil.log("Hourly job done.")

def daily_job():
    nutil.send_daily_notification(7)
    lutil.log("Daily jon done.")

def main():
    lutil.log("Starting script...")

    schedule.every().hour.at(":05").do(hourly_job)
    schedule.every().sunday.at("12:00").do(daily_job)

    while True:
        schedule.run_pending()
        time.sleep(60)

    lutil.handle_logger_close()


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        lutil.handle_logger_close()

