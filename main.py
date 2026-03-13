from subprocess import run

from helper import (
    choose_server,
    choose_version,
    download_server,
    get_server_dir,
    print_servers,
    start_server,
)

available_versions = None
print("type 'help' for available operations")


def remove():
    choice = choose_server()
    run(["rm", "-rf", get_server_dir(choice)])


def start():
    choice = choose_server()
    start_server(choice)


def download(updating=False):
    name = choose_server() if updating else input("server name -> ")
    download_server(name)


def main():
    options = {
        "help": lambda: print(
            """
    start - start a server
    download/install - download and install a server.jar file
    update - update a server
    list - list servers
    delete/remove - remove a server
    clear - clear the screen
    exit - exit the program
            """
        ),
        "start": start,
        "download": download,
        "install": download,
        "update": lambda: download(True),
        "list": print_servers,
        "delete": remove,
        "remove": remove,
        "clear": lambda: run("clear"),
        "exit": exit,
    }
    operation = input("operation -> ")
    options[operation]()
    main()


if __name__ == "__main__":
    main()
