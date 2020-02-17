import argparse
import subprocess
import os
import yaml
from shutil import copyfile, copytree

sub_projects = {
    "sstcam-base": "github.com/sstcam/sstcam-base.git",
    "sstcam-template": "github.com/sflis/sstcam-template.git",
    "sstcam-common": "github.com/sstcam/sstcam-common.git",
}
mode = {"https": "https://", "ssh": "ssh://git@"}
dependencies = {"pybind11": "https://github.com/pybind/pybind11.git"}


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print("Directory ", dir_name, " Created ")
    else:
        print("Directory ", dir_name, " already exists")


def clone_repos(sub_projects, sel_mode):
    for sp, git_url in sub_projects.items():
        print("Cloning project {}".format(sp))
        subprocess.run(["git", "clone", f"{mode[sel_mode]}{git_url}"])


def update_files(src, dest):
    subprocess.run(["rsync", "-ai", src, '--include="/*"', dest])


def get_sstcambuild_dir():
    return os.path.dirname(os.path.dirname(os.path.realpath(__file__)))


def init(args):
    currentDirectory = os.getcwd()
    root_path = currentDirectory
    build_descr_file = os.path.join(root_path, ".sstcam-buildconfig.yaml")
    if os.path.exists(build_descr_file) and not args.force:
        print(
            "This build is already initialized! To update use the update command instead"
        )
        exit()
    build_descr = {}

    sel_mode = "https"  # mode[]
    if args.ssh:
        sel_mode = "ssh"  # mode["ssh"]
    build_descr["git_mode"] = sel_mode

    with open(build_descr_file, "w") as f:
        yaml.dump(build_descr, f)

    clone_repos(sub_projects, sel_mode)

    create_dir(os.path.join(root_path, "build"))

    template_dir = os.path.join(get_sstcambuild_dir(), "root_template")

    update_files(template_dir + "/", root_path)


def devup(args):
    current_dir = os.getcwd()
    build_descr_file = os.path.join(current_dir, ".sstcam-buildconfig.yaml")
    if not os.path.exists(build_descr_file):
        while current_dir != "/":
            current_dir = os.path.dirname(current_dir)
            build_descr_file = os.path.join(current_dir, ".sstcam-buildconfig.yaml")
            if os.path.exists(build_descr_file):
                os.chdir(current_dir)
                break
        else:
            print("This is not an sstcam project directory. Aborting update...")
            exit()

    print("Updating build...")
    template_dir = os.path.join(get_sstcambuild_dir(), "root_template")

    update_files(template_dir + "/", current_dir)


def main():

    parser = argparse.ArgumentParser(
        description="SST Camera build system",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers()
    init_parser = subparsers.add_parser("init", help="Initialize the build")
    init_parser.set_defaults(func=init)
    init_parser.add_argument(
        "-s, --ssh",
        dest="ssh",
        action="store_true",
        help="Use ssh key authorization with Github",
    )
    init_parser.add_argument(
        "-f, --force", dest="force", action="store_true", help="Force command"
    )

    devup_parser = subparsers.add_parser(
        "devup",
        help="For development of the build system,"
        " updates the build after changing the build system app.",
    )
    devup_parser.set_defaults(func=devup)
    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
