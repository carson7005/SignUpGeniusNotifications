import signup_util as sutil
import canvas_util as cutil
import google_calendar_util as gcalutil
from datetime import date, timedelta
import log_util as lutil
import link_util


def get_notification_message(days_out=None,
                             days_from=0,
                             hours_out=None,
                             hours_from=0,
                             include_when=False):

    if not days_out and not hours_out:
        return None

    notif_message = ""
    signups_notify = get_signups_to_notify(days_out=days_out,
                                           days_from=days_from,
                                           hours_out=hours_out,
                                           hours_from=hours_from)
    for signup in signups_notify:
        roles = signup.get_roles(days_out=days_out,
                                 days_from=days_from,
                                 hours_out=hours_out,
                                 hours_from=hours_from)

        whole_count = 0
        signup_string = ""
        
        when_string = ""
        if include_when:
            if days_out:
                when_string = f" in the next {days_out} days{'s'[:days_out^1]}"
            elif hours_out:
                when_string = f" in the next {hours_out} hour{'s'[:hours_out^1]}"


        for r in roles:
            signup_string += "\n" + f"   {r.get_notification_role_string()}"
            whole_count += r.get_needed_count()

        signup_string += "\n" + f"   Link: <a href={signup.url}>{signup.url}</a>"
        
        update_string = ""
        if whole_count > 0:
            update_string = f"'{signup.title}' has {whole_count} volunteering" + \
                f" slot{'s'[:whole_count^1]} available{when_string}:"
        else:
            update_string = f"'{signup.title}' is full{f' and has roles happening{when_string}' if when_string else ''}:"

        signup_string = update_string + signup_string

        if notif_message: notif_message += "\n\n"

        notif_message += signup_string

    notif_message = notif_message.replace("\n", "<br>")

    return notif_message, len(signups_notify)


def get_signups_to_notify(days_out=None,
                          days_from=0,
                          hours_out=None,
                          hours_from=0,
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
                                 hours_from=hours_from)

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

