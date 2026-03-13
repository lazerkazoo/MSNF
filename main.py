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
    remove_unwanted_versions,
    search_plugins,
    search_versions,
    start_server,
)


def install_plugin():
    server = choose_server()
    version = get_server_version(server)
    query = input("search for -> ")

    hits = search_plugins(query, version)["hits"]
    project_data = choose(hits)
    versions = search_versions(project_data)
    remove_unwanted_versions(versions, version)

    download_plugin(
        versions,
        project_data["slug"],
        server,
    )


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
        "plugin list": lambda: print_list(get_plugins()),
        "plugin remove": remove_plugin,
    }
    operation = input("> ")
    options[operation]()
    main()


if __name__ == "__main__":
    print("type 'help' for available operations")
    main()
