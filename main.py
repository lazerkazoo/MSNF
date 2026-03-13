from os.path import expanduser
from subprocess import run

from helper import get_available_versions, get_servers, start_server

available_versions = None
print("type 'help' for available operations")


def print_servers():
    print()
    servers = get_servers()
    for i, server in enumerate(servers):
        print(f"[{i + 1}] {server}")
    print()


def remove():
    servers = get_servers()
    print_servers()
    choice = input("server -> ")
    run(
        ["rm", "-rf", f"{expanduser('~')}/Documents/Servers/{servers[int(choice) - 1]}"]
    )


def start():
    servers = get_servers()
    print_servers()
    choice = input("server -> ")
    start_server(servers[int(choice) - 1])


def download():
    global available_versions
    if available_versions is None:
        print("getting available versions...")
        available_versions = get_available_versions()

    version = input(
        f"mc version [{available_versions[0]}-{available_versions[-1]}] -> "
    )
    name = input("server name -> ")
    run(["./download.sh", version, f"{expanduser('~')}/Documents/Servers/{name}"])


def main():
    options = {
        "help": lambda: print(
            "\nstart - start a server\nlist - list servers\nclear - clear the screen\ndownload/install - download and install a server.jar file\ndelete/remove - remove a server\nexit - exit the program\n"
        ),
        "delete": remove,
        "remove": remove,
        "start": start,
        "list": print_servers,
        "download": download,
        "install": download,
        "clear": lambda: run("clear"),
        "exit": exit,
    }
    operation = input("operation -> ")
    options[operation]()
    main()


if __name__ == "__main__":
    main()
