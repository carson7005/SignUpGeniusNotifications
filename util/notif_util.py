from util import signup_util as sutil, \
    canvas_util as cutil, \
    google_calendar_util as gcalutil, \
    log_util as lutil, \
    link_util
from datetime import date, timedelta


def get_notification_message(days_out=None,
                             days_from=0,
                             hours_out=None,
                             hours_from=0,
                             include_full=True,
                             include_when=False):

    if not days_out and not hours_out:
        return None

    notif_message = ""
    signups_notify = get_signups_to_notify(days_out=days_out,
                                           days_from=days_from,
                                           hours_out=hours_out,
                                           hours_from=hours_from,
                                           include_full=include_full)
    for signup in signups_notify:
        notif_message += signup.get_signup_message()

    notif_message = notif_message.replace("\n", "<br>")

    return notif_message, len(signups_notify)


def get_signups_to_notify(days_out=None,
                          days_from=0,
                          hours_out=None,
                          hours_from=0,
                          include_full=True,
                          retries=5):
    if not days_out and not hours_out:
        return None

    signups = []
    links = link_util.get_current_links()
    for l in links:
        signup = sutil.get_signup_data(l, retries)
        roles = signup.get_roles(days_out=days_out,
                                 days_from=days_from,
                                 hours_out=hours_out,
                                 hours_from=hours_from,
                                 include_full=include_full)

        if not roles: continue

        signups.append(signup)

    return signups


def send_daily_notification(days_out, days_from=0, include_when=False):
    notif_message, signup_count = get_notification_message(days_out=days_out,
                                                           days_from=days_from,
                                                           include_when=include_when)

    if signup_count == 0:
        lutil.log(f"No signups for daily update ({days_out} days), skipping.")
        return

    current_date_str = date.today().strftime("%m/%d/%Y")
    notif_title = f"Daily Update for SignUps ({current_date_str})"
    notif_message = notif_title + "<br><br>" + notif_message
    default_course = cutil.get_notification_course_id()
    cutil.send_announcement(default_course, notif_title, notif_message)


def send_weekly_notification(days_out=7, days_from=0, include_when=False):
    notif_message, signup_count = get_notification_message(days_out=days_out,
                                                           days_from=days_from,
                                                           include_when=include_when)

    if signup_count == 0:
        lutil.log(f"No signups for weekly update ({days_out} days), skipping.")
        return

    current_date_str = date.today().strftime("%m/%d/%Y")
    notif_title = f"Weekly Update for SignUps ({current_date_str})"
    notif_message = notif_title + "<br><br>" + notif_message
    default_course = cutil.get_notification_course_id()
    cutil.send_announcement(default_course, notif_title, notif_message)


def send_hourly_notification(hours_out, hours_from=0,include_when=False):
    notif_message, signup_count = get_notification_message(hours_out=hours_out,
                                                                  hours_from=hours_from,
                                                                  include_when=include_when)

    if signup_count == 0:
        lutil.log(f"No signups for hourly update ({hours_out} hours), skipping.")
        return

    current_date_str = date.today().strftime("%m/%d/%Y")
    notif_title = f"Hourly Update for SignUps ({current_date_str})"
    notif_message = notif_title + "<br><br>" + notif_message
    default_course = cutil.get_notification_course_id()
    cutil.send_announcement(default_course, notif_title, notif_message)

