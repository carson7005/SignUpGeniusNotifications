import notif_util as nutil
import schedule
import time
import log_util as lutil
import link_util
import traceback

def hourly_job():
    nutil.send_hourly_notification(2, 1,include_when=True)
    lutil.log("Hourly job done.")

def daily_job():
    nutil.send_daily_notification(7)
    lutil.log("Daily job done.")

def weekly_job():
    nutil.send_weekly_notification()
    lutil.log("Weekly job done.")

def link_update_job():
    link_util.update_current_links(5)
    lutil.log("Link Update job done.")

def main():
    lutil.log("Starting script...")

    schedule.every().hour.at(":15").do(hourly_job)
    schedule.every().sunday.at("12:10").do(weekly_job)
    schedule.every().day.at("00:00").do(link_update_job)
    schedule.every().day.at("12:00").do(link_update_job)

    while True:
        schedule.run_pending()
        time.sleep(60)

    lutil.handle_logger_close()


if __name__ == "__main__":
    try:
        main()
    except BaseException as e:
        lutil.handle_logger_close()
        traceback.print_exc()

