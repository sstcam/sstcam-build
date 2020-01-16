import argparse
import subprocess
import os
import yaml
from shutil import copyfile,copytree

sub_projects = {'sstcam-base': 'https://github.com/sstcam/sstcam-base.git',
                'sstcam-template': 'https://github.com/sflis/sstcam-template.git',
                'sstcam-common': "https://github.com/sstcam/sstcam-common.git"}

dependencies = {'pybind11': "https://github.com/pybind/pybind11.git"}


def create_dir(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)
        print("Directory ", dir_name, " Created ")
    else:
        print("Directory ", dir_name, " already exists")


def main():

    parser = argparse.ArgumentParser(
        description="SST Camera build system",
        formatter_class=argparse.ArgumentDefaultsHelpFormatter,
    )
    parser.add_argument("init", help="Initialize the build")
    args = parser.parse_args()
    if args.init:
        currentDirectory = os.getcwd()
        root_path = currentDirectory
        with open(os.path.join(root_path, ".sstcam-buildconfig.yaml"), 'w') as f:
            f.write(" ")

        sstcam_build_system_dir = os.path.dirname(os.path.dirname(os.path.realpath(__file__)))
        template_dir = os.path.join(sstcam_build_system_dir,'root_template')
        create_dir(os.path.join(root_path, 'build'))
        for sp, git_url in sub_projects.items():
            print("Cloning project {}".format(sp))
            subprocess.run(['git', 'clone', git_url])
        copyfile(os.path.join(template_dir, 'CMakeLists.txt'),
                os.path.join(root_path, 'CMakeLists.txt'))
        copytree(os.path.join(template_dir,'python'),
                os.path.join(root_path,'python'))

        # deps_dir = os.path.join(root_path, 'deps')
        # create_dir(os.path.join(deps_dir, "build"))

        # for dp, git_url in dependencies.items():
        #     print("Cloning dependency {}".format(dp))
        #     subprocess.run(['git', 'clone', git_url], cwd=os.path.join(root_path, "deps"))
        #     print("Installing dependency {}".format(dp))
        #     subprocess.run(['cmake', '../{}'.format(dp), "-DCMAKE_INSTALL_PREFIX=$CONDA_PREFIX"],
        #                         cwd=os.path.join(deps_dir, "build"))
        #     subprocess.run(['make', "install"], cwd=os.path.join(deps_dir, "build"))


if __name__ == '__main__':
    main()

