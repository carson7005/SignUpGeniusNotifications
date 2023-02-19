import signup_util as sutil
import canvas_util as cutil
import google_calendar_util as gcalutil
import argparse


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("signup_url")
    args = parser.parse_args()

    if not args.signup_url:
        print("No Sign Up URL given.")
        return
    else:
        print("Thinking...")

    signup = sutil.get_signup_data(args.signup_url, 5)
    print(signup.title)
    for r in signup.roles:
        print(r.get_role_string())


def test():
    #parser = argparse.ArgumentParser()
    #parser.add_argument("signup_url")
    #args = parser.parse_args()

    #s = sutil.get_signup_data(args.signup_url, 5)

    #print(s.title)

    events = gcalutil.get_nhs_events()
    for e in events:
        desc = gcalutil.get_raw_description(e).split(" ")
        for i in desc:
            url = sutil.fix_signupgenius_url(i)
            if url == None: continue
            
            signup = sutil.get_signup_data(url, 5)
            print("-----------------------------------------------")
            #for r in signup.roles:
            #    print(r.get_role_string())
            print(signup.description)
            break


if __name__ == "__main__":
    test()

