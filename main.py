from os import execv
from subprocess import run
from sys import argv, executable

from helper import (
    choose,
    choose_server,
    download_plugin,
    download_server,
    get_plugins,
    get_server_dir,
    get_server_version,
    get_servers,
    print_list,
    remove_plugin,
    search_plugins,
    start_server,
    update_plugin,
)

server = choose_server()


def update_plugins():
    for i in get_plugins(server):
        update_plugin(server, i)


def install_plugin():
    hits = search_plugins(input("search for -> "), get_server_version(server))["hits"]
    download_plugin(choose(hits, False)["slug"], server)


def main():
    options = {
        "help": lambda: print(open("help.txt").read()),
        "start": lambda: start_server(server),
        "install": download_server,
        "restart": lambda: [run("clear"), execv(executable, ["python"] + argv)],
        "update": lambda: download_server(server),
        "list": lambda: print_list(get_servers()),
        "remove": lambda: run(["rm", "-rf", get_server_dir()]),
        "clear": lambda: run("clear"),
        "exit": exit,
        "plugin help": lambda: print(open("help-plugin.txt").read()),
        "plugin install": install_plugin,
        "plugin update": update_plugins,
        "plugin list": lambda: print_list(get_plugins(server)),
        "plugin remove": lambda: remove_plugin(server),
    }
    operation = input("> ")
    options[operation]()
    main()


if __name__ == "__main__":
    print("type 'help' for available operations")
    main()
