from subprocess import run

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


def update_plugins():
    server = choose_server()
    for i in get_plugins(server):
        update_plugin(server, i)


def install_plugin():
    server = choose_server()
    hits = search_plugins(input("search for -> "), get_server_version(server))["hits"]
    download_plugin(choose(hits, False)["slug"], server)


def main():
    options = {
        "help": lambda: print(open("help.txt").read()),
        "start": start_server,
        "install": download_server,
        "update": lambda: download_server(choose_server()),
        "list": lambda: print_list(get_servers()),
        "remove": lambda: run(["rm", "-rf", get_server_dir()]),
        "clear": lambda: run("clear"),
        "exit": exit,
        "plugin help": lambda: print(open("help-plugin.txt").read()),
        "plugin install": install_plugin,
        "plugin update": update_plugins,
        "plugin list": lambda: print_list(get_plugins()),
        "plugin remove": remove_plugin,
    }
    operation = input("> ")
    options[operation]()
    main()


if __name__ == "__main__":
    print("type 'help' for available operations")
    main()
