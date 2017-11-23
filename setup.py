import os
from functools import partial
from setuptools import setup

from quicktick import __version__

project_dir = os.path.abspath(os.path.dirname(__file__))
project_file = partial(os.path.join, project_dir)

with open(project_file("README.rst"), "rt") as f:
    long_description = f.read()

with open(project_file("requirements.txt"), "rt") as f:
    requirements = map(
        lambda req: req.split("==")[0],
        f.readlines())

setup(
    name="quicktick",
    version=__version__,

    description="Simple cryptocurrency ticker",
    long_description=long_description,

    url="https://github.com/Xophmeister/quicktick",

    author="Christopher Harrison",
    license="GPLv3",

    classifiers=[
        "Development Status :: 4 - Beta",
        "Intended Audience :: End Users/Desktop",
        "Intended Audience :: Financial and Insurance Industry",
        "License :: OSI Approved :: GNU General Public License v3 or later (GPLv3+)",
        "Operating System :: POSIX",
        "Programming Language :: Python :: 3.6"],

    keywords="cryptocurrency ticker",

    packages=["quicktick"],
    python_requires=">=3.6",
    install_requires=requirements,

    data_files=[(os.path.expanduser("~"), [".quicktick"])],

    entry_points={"console_scripts": ["quicktick=quicktick.main:run"]}
)
