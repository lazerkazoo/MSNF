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
args = []


def update_plugins():
    global args
    for i in get_plugins(server):
        update_plugin(server, i)


def install_plugin():
    global args
    if len(args) >= 1:
        search = args[0]
    else:
        search = input("search for -> ")
    hits = search_plugins(search, get_server_version(server))["hits"]
    download_plugin(choose(hits, False)["slug"], server)


def main():
    global args
    options = {
        "help": lambda: print(open("help.txt").read()),
        "start": lambda: start_server(server),
        "select": lambda: execv(executable, ["python"] + argv + ["no"]),
        "install": lambda: download_server(args=args),
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
    for o in options:
        if not operation.startswith(o):
            continue
        args = operation.split(o)[-1]
        args = args.split(" ")
        for a in args:
            if a in ["", " "]:
                args.remove(a)

        operation = o
        break
    options[operation]()
    main()


if __name__ == "__main__":
    if "no" not in argv:
        print("type 'help' for available operations")
    main()
