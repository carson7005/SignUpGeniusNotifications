from util import notif_util as nutil, \
    log_util as lutil
import schedule
import time
import traceback
import json

def hourly_job():
    nutil.send_notification(get_config_item("signup_genius_token"),
                            hours_out=2,
                            hours_from=1,
                            include_full=False,
                            include_when=True)
    lutil.log("Hourly job done.")

def daily_job():
    nutil.send_notification(get_config_item("signup_genius_token"),
                            days_out=1,
                            include_full=False,
                            include_when=True)
    lutil.log("Daily job done.")

def weekly_job():
    nutil.send_weekly_notification(get_config_item("signup_genius_token"))
    lutil.log("Weekly job done.")

def get_config_item(key):
    config_file = open("config.json")
    data = json.load(config_file)
    config_file.close()

    return data[key]

def main():
    lutil.log("Starting script...")

    daily_time = get_config_item("daily_time")
    hourly_minute = get_config_item("hourly_minute")

    schedule.every().hour.at(hourly_minute).do(hourly_job)

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
        lutil.log("Exception Thrown:")
        traceback.print_exc()
        
    lutil.handle_logger_close()


    
