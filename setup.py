from setuptools import setup
from setuptools.command.install import install
import os
import shutil
import warnings
import sys
import platform

# Download setuptools if it's not installed on target system
import ez_setup
ez_setup.use_setuptools()


# Utility function to read the README file.
# Used for the long_description.  It's nice, because now 1) we have a top level
# README file and 2) it's easier to type in the README file than to put a raw
# string in below ...
def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

requires = [
    "appdirs",
    "prettytable",
    "simpleyaml",
    "numpy",
    "matplotlib",
    "scipy",
    "pandas"
]

# install_requires should contain pygtk. However there's a problem,
# at least on linux:
# - pygtk can't be build from setuptools (only possible on Windows)
# - setuptools isn't smart enough to figure out that the module is already
#   there - i.e. it'll try to install it, remember it can't, and die.

if platform.system() == "Windows":
    # So if we're on windows, we can add it to the list.
    requires.append("pygtk")
else:
    # Otherwise the best we can do is tell the user to install pygtk
    # before trying again.
    try:
        import pygtk
    except ImportError:
        print "Superplot requires PyGTK, which is not available on this system " \
              "and cannot be automatically installed. Please install PyGTK " \
              "version 2.0 or greater using your OS package manager or via " \
              "www.pygtk.org"
        sys.exit(1)


class SuperplotInstall(install):
    """
    Subclass the setuptools install command so we can
    run post-install actions (e.g. placing the config file).
    """
    def run(self):
        """
        Post-install, this script will try to place the config and
        style files in an OS-appropriate user data directory.
        If this fails, setup will continue and the application
        will fall back on the files included in the install.
        """
        install.run(self)
        import appdirs

        # OS-specific user data directory for this app.
        # We will put the config file and style sheets here.
        user_dir = appdirs.user_data_dir("superplot", "")

        try:
            if not os.path.isdir(user_dir):
                os.mkdir(user_dir)
        except OSError as e:
            warnings.warn(
                "Could not create user data directory: {}".format(
                    e.strerror
                )
            )

        # Copy config.yml to user directory
        config_path = os.path.join(user_dir, "config.yml")

        # If the config file is already present,
        # *don't* overwrite it.
        if os.path.exists(config_path):
            warnings.warn(
                "Config file already present - not overwriting."
            )
        else:
            try:
                shutil.copy("superplot/config.yml", config_path)
            except shutil.Error as e:
                warnings.warn(
                    "Error copying config file to user directory: {}".format(
                        e.strerror
                    )
                )

        # Copy style sheets to user directory
        styles_dir = os.path.join(user_dir, "styles")

        try:
            shutil.copytree("superplot/plotlib/styles", styles_dir)
        except shutil.Error as e:
            warnings.warn(
                "Error copying style sheets to user directory: {}".format(
                    e.strerror
                )
            )

        print "Finished post-setup actions"

setup(
        cmdclass={'install': SuperplotInstall},

        setup_requires=["setuptools_git", "appdirs"],

        install_requires=requires,

        packages=[
            "superplot",
            "superplot.plotlib",
            "superplot.plotlib.styles",
            "superplot.statslib"
        ],
        include_package_data=True,

        name="superplot",
        version="2.0-dev",
        author="Andrew Fowlie, Michael Bardsley",
        author_email="mhbar3@student.monash.edu",
        license="GPL v2",
        url="https://github.com/michaelhb/superplot",

        description="Python GUI for plotting SuperPy/SuperBayes/MultiNest/BAYES-X results",
        long_description=read("README.rst"),

        entry_points={
            'gui_scripts': [
                'superplot_gui = superplot.super_gui:main',
                'superplot_summary = superplot.summary:main'
            ]
        }
)
