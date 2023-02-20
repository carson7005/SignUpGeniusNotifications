import notif_util as nutil


def main():
    #nutil.send_weekly_notification()
    nutil.send_hourly_notification(2, True)


if __name__ == "__main__":
    main()

