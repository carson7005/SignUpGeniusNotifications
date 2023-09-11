from util import notif_util as nutil, \
    log_util as lutil
import schedule
import time
import traceback

def hourly_job():
    nutil.send_notification(hours_out=2, hours_from=1, include_full=False, include_when=True)
    lutil.log("Hourly job done.")

def daily_job():
    nutil.send_notification(days_out=1, include_full=False, include_when=True)
    lutil.log("Daily job done.")

def weekly_job():
    nutil.send_weekly_notification()
    lutil.log("Weekly job done.")


def main():
    lutil.log("Starting script...")

    schedule.every().hour.at(":15").do(hourly_job)

    daily_time = "07:00"
    schedule.every().sunday.at(daily_time).do(daily_job)
    schedule.every().tuesday.at(daily_time).do(daily_job)
    schedule.every().wednesday.at(daily_time).do(daily_job)
    schedule.every().thursday.at(daily_time).do(daily_job)
    schedule.every().friday.at(daily_time).do(daily_job)
    schedule.every().saturday.at(daily_time).do(daily_job)

    schedule.every().monday.at(daily_time).do(weekly_job)

    while True:
        schedule.run_pending()
        time.sleep(60)


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        traceback.print_exc()
        
    lutil.handle_logger_close()

