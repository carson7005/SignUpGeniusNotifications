from util import link_util


def main():
    link_util.file_check()
    link_util.update_current_links(5)
    print(link_util.get_current_links())


if __name__ == "__main__":
    main()

