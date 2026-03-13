from os.path import expanduser
from subprocess import run

from helper import (
    choose_server,
    choose_version,
    print_servers,
    start_server,
)

available_versions = None
print("type 'help' for available operations")


def remove():
    choice = choose_server()
    run(["rm", "-rf", f"{expanduser('~')}/Documents/Servers/{choice}"])


def start():
    choice = choose_server()
    start_server(choice)


def update():
    server = choose_server()
    version = choose_version(available_versions)
    if version is None:
        return
    run(
        [
            "./download.sh",
            version,
            f"{expanduser('~')}/Documents/Servers/{server}",
        ]
    )


def download():
    name = input("server name -> ")
    version = choose_version(available_versions)
    if version is None:
        return
    run(["./download.sh", version, f"{expanduser('~')}/Documents/Servers/{name}"])


def main():
    options = {
        "help": lambda: print(
            "\nstart - start a server\nlist - list servers\nclear - clear the screen\ndownload/install - download and install a server.jar file\nupdate - update a server\ndelete/remove - remove a server\nexit - exit the program\n"
        ),
        "delete": remove,
        "remove": remove,
        "start": start,
        "list": print_servers,
        "download": download,
        "install": download,
        "update": update,
        "clear": lambda: run("clear"),
        "exit": exit,
    }
    operation = input("operation -> ")
    options[operation]()
    main()


if __name__ == "__main__":
    main()
