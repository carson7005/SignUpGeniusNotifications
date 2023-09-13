from util import notif_util as nutil
import json


def main():
    config_file = open("config.json")
    data = json.load(config_file)
    token = data["signup_genius_token"]
    config_file.close()

    
    nutil.send_weekly_notification(token)

if __name__ == "__main__":
    main()
