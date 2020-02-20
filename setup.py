import os
import sys
from setuptools import find_packages, setup
import versioneer

commands = versioneer.get_cmdclass().copy()

PY2 = sys.version_info.major == 2
PY3 = sys.version_info.major == 3

pkgname = "imageio_wrappers"


def package_files(directories):
    if isinstance(directories, str):
        directories = [directories]
    paths = []
    for directory in directories:
        for (path, directories, filenames) in os.walk(directory):
            for filename in filenames:
                paths.append(os.path.join("..", path, filename))
    return paths


packages = find_packages()

setup(
    name=pkgname,
    version=versioneer.get_version(),
    script_name="setup.py",
    zip_safe=False,
    packages=packages,
    install_requires=["typing"],
    extras_require={},
    cmdclass=commands,
)
