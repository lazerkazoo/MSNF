from subprocess import run

from helper import (
    choose_server,
    download_server,
    get_server_dir,
    print_servers,
    start_server,
)


def main():
    options = {
        "help": lambda: print(open("help.txt").read()),
        "start": start_server,
        "download": download_server,
        "install": download_server,
        "update": lambda: download_server(choose_server()),
        "list": print_servers,
        "delete": lambda: run(["rm", "-rf", get_server_dir()]),
        "remove": lambda: run(["rm", "-rf", get_server_dir()]),
        "clear": lambda: run("clear"),
        "exit": exit,
    }
    operation = input("> ")
    options[operation]()
    main()


if __name__ == "__main__":
    available_versions = None
    print("type 'help' for available operations")
    main()
