from concurrent.futures import ThreadPoolExecutor
from json import dump, load, loads
from os import listdir
from os.path import expanduser
from subprocess import check_output, run


# QOL
def load_json(fp):
    with open(fp, "r") as f:
        return load(f)


def save_json(fp, obj):
    with open(fp, "w") as f:
        dump(obj, f)


def print_list(lst):
    if len(lst) == 0:
        print("no items found")
        return
    print()
    for i, item in enumerate(lst):
        if isinstance(item, dict) and item.get("title"):
            item = item["title"]
        print(f"[{i + 1}] {item}")
    print()


def choose(options, auto=True):
    if len(options) == 1 and auto:
        print(f"chose {options[0]} [no other options]")
        return options[0]

    print_list(options)
    choice = int(input("choose -> "))
    return options[choice - 1]


# Version retrieval
def get_versions():
    run(
        [
            "curl",
            "-s",
            "-o",
            "/tmp/idk.json",
            "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json",
        ]
    )
    return load_json("/tmp/idk.json")


def get_latest_version():
    js = get_versions()
    return js["latest"]["release"]


def get_all_versions():
    js = get_versions()
    versions: list = []
    for i in js["versions"]:
        if i["type"] == "release":
            versions.append(i["id"])
    versions.reverse()
    return versions


def check_version_ok(version):
    data = loads(
        check_output(
            [
                "curl",
                "-s",
                f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds",
            ]
        )
    )
    if isinstance(data, dict):
        return data.get("ok", True)
    return True


def get_available_versions():
    versions = get_all_versions()
    with ThreadPoolExecutor(max_workers=30) as executor:
        results = list(executor.map(check_version_ok, versions))
    return [v for v, ok in zip(versions, results) if ok]


def choose_version():
    print("getting available versions...")
    versions = get_available_versions()
    return input(f"choose version [{versions[0]}-{versions[-1]}] -> ")


# Server discovery
def get_servers():
    return listdir(f"{expanduser('~')}/Documents/Servers")


def get_server_dir(server=None):
    if server is None:
        server = choose_server()
    return f"{expanduser('~')}/Documents/Servers/{server}"


def get_server_version(server=None):
    if server is None:
        server = choose_server()
    return load_json(f"{get_server_dir(server)}/version.json")["version"]


def choose_server():
    return choose(get_servers())


# Server management
def download_server(server=None, version=None):
    if server is None:
        server = input("server name -> ")
    if version is None:
        version = choose_version()
    run(["./download.sh", version, get_server_dir(server)])


def start_server(server=None):
    if server is None:
        server = choose_server()
    run(
        "./startup.sh",
        cwd=f"{expanduser('~')}/Documents/Servers/{server}/",
    )


# Plugin managerment
def get_plugins(server=None):
    if server is None:
        server = choose_server()
    plugins_dir = f"{get_server_dir(server)}/plugins/"
    return listdir(plugins_dir)


def choose_plugin(server=None):
    if server is None:
        server = choose_server()
    return choose(get_plugins(server))


def remove_plugin(server=None, plugin=None):
    if server is None:
        server = choose_server()
    if plugin is None:
        plugin = choose_plugin(server)
    run(["rm", f"{get_server_dir(server)}/plugins/{plugin}"])


def search_plugins(query, mc):
    for n, i in enumerate(query):
        if i == " ":
            query = query[:n:]
    return loads(
        check_output(
            [
                "curl",
                "-s",
                f"https://api.modrinth.com/v2/search?query={query}&limit=5&facets=%5B%5B%22project_type%3Aplugin%22%5D%2C%5B%22categories%3Apaper%22%5D%2C%5B%22versions%3A{mc}%22%5D%5D",
            ]
        )
    )


def search_versions(slug):
    return loads(
        check_output(
            [
                "curl",
                "-s",
                f"https://api.modrinth.com/v2/project/{slug}/version?include_changelog=false",
            ]
        )
    )


def remove_unwanted_versions(versions, mc):
    for v in versions:
        if mc not in v["game_versions"] or "paper" not in v["loaders"]:
            versions.remove(v)


def download_plugin(slug, server):
    versions = search_versions(slug)
    remove_unwanted_versions(versions, get_server_version(server))

    newest = versions[0]["files"][0]
    url = newest["url"]
    run(["curl", "-o", f"{get_server_dir(server)}/plugins/{slug}.jar", url])


def update_plugin(server, plugin):
    download_plugin(plugin.split(".")[0], server)
