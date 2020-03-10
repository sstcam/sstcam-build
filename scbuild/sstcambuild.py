import argparse
import subprocess
import os
import yaml
from shutil import copyfile, copytree
import jinja2


sub_projects = {
    "sstcam-common": "github.com/sstcam/sstcam-common.git",
    "sstcam-control": "github.com/sstcam/sstcam-control.git",
}
mode = {"https": "https://", "ssh": "ssh://git@"}

build_types = {"lite": ["sstcam-common"], "full": ["sstcam-common", "sstcam-control"]}

conda_dep ={"full":["zeromq","cppzmq"],"lite":[]}

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
    subprocess.run(
        ["rsync", "-ai", "--exclude", "__pycache__", src, '--include="/*"', dest]
    )


def get_sstcambuild_dir():
    return os.path.dirname(os.path.realpath(__file__))


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

    sel_mode = "https"
    if args.ssh:
        sel_mode = "ssh"

    build_descr["git_mode"] = sel_mode
    build_descr["build_type"] = args.build_type

    with open(build_descr_file, "w") as f:
        yaml.dump(build_descr, f)

    sel_proj = {k: sub_projects[k] for k in build_types[args.build_type]}
    clone_repos(sel_proj, sel_mode)

    create_dir(os.path.join(root_path, "build"))

    template_dir = os.path.join(get_sstcambuild_dir(), "root_template")

    update_files(template_dir + "/", root_path)
    if args.conda:
        conda_setup(build_descr["build_type"])

bash_script_template ="""{{prepare}}
{%- for dep in deps %}
conda-build {{conda_build}}/{{dep}}
conda install -c $CONDA_PREFIX/conda-bld/ {{dep}} -y
{%- endfor %}
"""

def conda_setup(build_type):

    conda_env_file = os.path.join(get_sstcambuild_dir(), "conda_build", "enviroment.yml")
    conda_build = os.path.join(get_sstcambuild_dir(), "conda_build")
    prepare = f"conda env update --file {conda_env_file} \nconda install conda-build -y"
    t = jinja2.Template(bash_script_template)
    script = t.render(prepare=prepare,
                      conda_build=conda_build,
                      deps=conda_dep[build_type])
    with open("/tmp/sstcam_build.sh", "w") as f:
        f.write(script)
    subprocess.run(["bash", "/tmp/sstcam_build.sh"])

def devup(args):

    current_dir = os.getcwd()
    build_descr_file = os.path.join(current_dir, ".sstcam-buildconfig.yaml")
    if not os.path.exists(build_descr_file):
        while current_dir != "":
            current_dir = os.path.dirname(current_dir)
            build_descr_file = os.path.join(current_dir, ".sstcam-buildconfig.yaml")
            if os.path.exists(build_descr_file):
                os.chdir(current_dir)
                break
        else:
            print("This is not an sstcam project directory. Aborting update...")
            exit()
    build_descr = yaml.load(open(build_descr_file,'r'),Loader=yaml.SafeLoader)
    # conda_setup(build_descr['build_type'])
    print("Updating build...")
    template_dir = os.path.join(get_sstcambuild_dir(), "root_template")

    update_files(template_dir + "/", current_dir)
    if args.conda:
        conda_setup(build_descr['build_type'])


def main():

    parser = argparse.ArgumentParser(
        description="SST Camera build system",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    subparsers = parser.add_subparsers()
    init_parser = subparsers.add_parser("init", help="Initialize the build")
    init_parser.set_defaults(func=init)
    init_parser.add_argument(
        "-s",
        "--ssh",
        dest="ssh",
        action="store_true",
        help="Use ssh key authorization with Github",
    )
    init_parser.add_argument(
        "build_type",
        nargs="?",
        default="full",
        choices=["full", "lite"],
        help="Selects the type of build. The `full` is used for the camera system, for analysis `lite` is used.",
    )
    init_parser.add_argument(
        "-f", "--force", dest="force", action="store_true", help="Force command"
    )

    init_parser.add_argument(
        "-c", "--conda", dest="conda", action="store_true",
        help="Additional dependencies are installed and build in a conda env. Assumption: init is executed in a conda enviroment"
    )
    devup_parser = subparsers.add_parser(
        "devup",
        help="For development of the build system,"
        " updates the build after changing the build system app.",
    )
    devup_parser.add_argument(
        "-c", "--conda", dest="conda", action="store_true",
        help="Additional dependencies are installed and build in a conda env. Assumption: init is executed in a conda enviroment"
    )
    devup_parser.set_defaults(func=devup)

    args = parser.parse_args()
    args.func(args)


if __name__ == "__main__":
    main()
