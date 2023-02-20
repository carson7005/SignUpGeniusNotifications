import signup_util as sutil
import canvas_util as cutil
import google_calendar_util as gcalutil
import notif_util as nutil
import argparse
from datetime import date, timedelta


def main():
    nutil.send_weekly_notification()


if __name__ == "__main__":
    main()

