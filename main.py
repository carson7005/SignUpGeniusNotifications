import signup_util as sutil
import canvas_util as cutil
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

    signup = sutil.get_signup_data(args.signup_url)
    print(signup.title)
    print(signup.roles)
    for r in signup.roles:
        print(r.status)


def test():
    parser = argparse.ArgumentParser()
    parser.add_argument("signup_url")
    args = parser.parse_args()

    tables = sutil.get_page_tables(args.signup_url, 5)
    for t in tables:
        t.info()
        t.to_csv("test/out.csv")
        print("\n")
        break

    print(len(tables))

    # a = cutil.send_announcement(6768,
    #                         "Python Test",
    #                         "This announcement was automatically sent using a Python script",
    #                         True)
    # print(a)


if __name__ == "__main__":
    test()

