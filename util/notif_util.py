from util import signup_util as sutil, \
    canvas_util as cutil, \
    log_util as lutil
from datetime import date, timedelta


def get_notification_message(signup_genius_token,
                             days_out=None,
                             days_from=0,
                             hours_out=None,
                             hours_from=0,
                             include_full=True,
                             include_when=False):

    if not days_out and not hours_out:
        return None

    notif_message = ""
    signups_notify = get_signups_to_notify(signup_genius_token,
                                           days_out=days_out,
                                           days_from=days_from,
                                           hours_out=hours_out,
                                           hours_from=hours_from,
                                           include_full=include_full)
    for signup in signups_notify:
        notif_message += signup.get_signup_message(days_out=days_out,
                                                   days_from=days_from,
                                                   hours_out=hours_out,
                                                   hours_from=hours_from,
                                                   include_full=include_full,
                                                   include_time_detail=include_when)

    contact_email = "joshua.fernandez@dexterschools.org"
    notif_message += "\n<hr>\n" + "Is there anything incorrect with this " + \
        "notification? If so, please contact Josh Fernandez (" + \
        f"<a href='mailto:{contact_email}'>{contact_email}</a>)" + "\n"
    
    notif_message = notif_message.replace("\n", "<br>")

    return notif_message, len(signups_notify)


def get_signups_to_notify(signup_genius_token,
                          days_out=None,
                          days_from=0,
                          hours_out=None,
                          hours_from=0,
                          include_full=True):
    if not days_out and not hours_out:
        return None

    signups = []
    for signup in sutil.get_current_signups(signup_genius_token):
        roles = signup.get_roles(days_out=days_out,
                                 days_from=days_from,
                                 hours_out=hours_out,
                                 hours_from=hours_from,
                                 include_full=include_full)

        if not roles: continue

        signups.append(signup)

    return signups


def send_notification(days_out=None,
                      days_from=0,
                      hours_out=None,
                      hours_from=0,
                      include_full=True,
                      include_when=False,
                      override_title=None):
    if not days_out and not hours_out:
        lutil.log("No ending time given, skipping notification.")
        return

    notif_message, signup_count = get_notification_message(days_out=days_out,
                                                           days_from=days_from,
                                                           hours_out=hours_out,
                                                           hours_from=hours_from,
                                                           include_full=include_full,
                                                           include_when=include_when)

    notif_status = "Daily", f"{days_out} days"
    if hours_out:
        notif_status = "Hourly", f"{hours_out} hours"

    if signup_count == 0:
        lutil.log(f"No signups for {notif_status[0]} Update " + \
                f"({notif_status[1]}), skipping.")
        return

    current_date_str = date.today().strftime("%m/%d/%Y")
    notif_title = f"{override_title if override_title else notif_status[0]}" + \
            f" Update for SignUps ({current_date_str})"
    notif_message = notif_title + "<br>" + notif_message
    default_course = cutil.get_notification_course_id()
    cutil.send_announcement(default_course, notif_title, notif_message)

    lutil.log(f"{notif_status[0]} Update ({notif_status[1]}) sent.")



def send_weekly_notification():
    send_notification(days_out=7, override_title="Weekly")


