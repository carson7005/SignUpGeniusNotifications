from util import signup_util as sutil, config_util, log_util as lutil
import datetime
import json
import os


def main():
    sg_token = config_util.get_config_item("signup_genius_token")

    now = datetime.datetime.now()
    current_time_name = f"{now.strftime('%m-%d-%Y_Signups_Store')}"
    log_file_name = current_time_name + "_Log.txt"

    lutil.log("Fetching all current signups for JSON store task", log_file_name)
    current_signups = sutil.get_current_signups(sg_token, log_file_path=log_file_name)

    signups_array_json = []

    for s in current_signups:
        signups_array_json.append(s.to_json())


    if not os.path.exists("logs/"): os.mkdir("logs/")

    with open(f"logs/{current_time_name}.json", "w") as json_out_file:
        json_out_file.write(json.dumps({"signups": signups_array_json}, indent=4))

    lutil.log("Finished JSON store task", log_file_name)


if __name__ == "__main__":
    main()
