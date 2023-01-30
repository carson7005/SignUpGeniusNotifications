import signup_util as sutil
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


if __name__ == "__main__":
    main()

