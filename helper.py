from concurrent.futures import ThreadPoolExecutor
from json import dump, load, loads
from os import listdir
from os.path import expanduser
from subprocess import check_output, run


def load_json(fp):
    with open(fp, "r") as f:
        return load(f)


def save_json(fp, obj):
    with open(fp, "w") as f:
        dump(obj, f)


def get_servers():
    return listdir(f"{expanduser('~')}/Documents/Servers")


def get_server_dir(server):
    return f"{expanduser('~')}/Documents/Servers/{server}"


def print_servers():
    print()
    servers = get_servers()
    for i, server in enumerate(servers):
        print(f"[{i + 1}] {server}")
    print()


def choose_server():
    servers = get_servers()
    if not servers:
        return None
    print_servers()
    choice = input("choose -> ")
    choice = int(choice)
    return servers[choice - 1]


def choose_version(available_versions):
    print("getting available versions...")
    versions = (
        get_available_versions() if available_versions is None else available_versions
    )
    if not versions:
        print("\nno version chosen\n")
        return None
    choice = input(f"choose version [{versions[0]}-{versions[-1]}] -> ")
    available_versions = versions
    return choice


# getting versions
def get_versions():
    run(
        [
            "curl",
            "https://launchermeta.mojang.com/mc/game/version_manifest_v2.json",
            "--output",
            "dog.json",
            "-s",
        ]
    )
    return load_json("dog.json")


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


def get_available_versions():
    versions = get_all_versions()
    with ThreadPoolExecutor(max_workers=20) as executor:
        results = list(executor.map(check_version_ok, versions))
    return [v for v, ok in zip(versions, results) if ok]


def check_version_ok(version):
    data = loads(
        check_output(
            [
                "curl",
                f"https://fill.papermc.io/v3/projects/paper/versions/{version}/builds",
                "-s",
            ]
        )
    )
    if isinstance(data, dict):
        return data.get("ok", True)
    return True


# server startup
def start_server(server):
    run(
        "./startup.sh",
        cwd=f"{expanduser('~')}/Documents/Servers/{server}/",
    )
