# coding=utf-8
# @author=cer

from setuptools import setup, find_packages
from datetime import date
import os

# --- Define project dependent variable ---
# Your package name
NAME = "paper_manager"
# Your GitHub user name
GITHUB_USERNAME = "applenob"  # your GitHub account name

# --- Automatically generate setup parameters ---
try:
    SHORT_DESCRIPTION = __import__(NAME).__short_description__  # GitHub Short Description
except:
    print("'__short_description__' not found in '%s.__init__.py'!" % NAME)
    SHORT_DESCRIPTION = "No short description!"

try:
    LONG_DESCRIPTION = open("README.rst", "rb").read().decode("utf-8")
except:
    LONG_DESCRIPTION = "No long description!"

VERSION = __import__(NAME).__version__
AUTHOR = "Kevin Chan"
AUTHOR_EMAIL = "applecer@pku.edu.cn"
MAINTAINER = "Kevin Chan"
MAINTAINER_EMAIL = "applecer@pku.edu.cn"

# Include all sub packages in package directory
PACKAGES = [NAME] + ["%s.%s" % (NAME, i) for i in find_packages(NAME)]
# Include everything in package directory
INCLUDE_PACKAGE_DATA = True
PACKAGE_DATA = {
    "": ["*.*"],
}

# The project directory name is the GitHub repository name
repository_name = os.path.basename(os.getcwd())
# Project Url
URL = "https://github.com/{0}/{1}".format(GITHUB_USERNAME, repository_name)
# Use todays date as GitHub release tag
github_release_tag = str(date.today())
# Source code download url
DOWNLOAD_URL = "https://github.com/{0}/{1}/tarball/{2}".format(
    GITHUB_USERNAME, repository_name, github_release_tag)

try:
    LICENSE = __import__(NAME).__license__
except:
    print("'__license__' not found in '%s.__init__.py'!" % NAME)
    LICENSE = ""

PLATFORMS = ["Windows", "MacOS", "Unix"]
CLASSIFIERS = [
    "Development Status :: 4 - Beta",
    "Intended Audience :: Education",
    "License :: OSI Approved :: MIT License",
    "Natural Language :: English",
    "Operating System :: Microsoft :: Windows",
    "Operating System :: MacOS",
    "Operating System :: Unix",
    "Programming Language :: Python :: 2.7",
    "Programming Language :: Python :: 3",
    "Programming Language :: Python :: 3.3",
    "Programming Language :: Python :: 3.4",
    "Programming Language :: Python :: 3.5",
    "Programming Language :: Python :: 3.6",
]

try:
    f = open("requirements.txt", "rb")
    REQUIRES = [i.strip() for i in f.read().decode("utf-8").split("\n")]
except:
    print("'requirements.txt' not found!")
    REQUIRES = list()

setup(
    name=NAME,
    description=SHORT_DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    version=VERSION,
    author=AUTHOR,
    author_email=AUTHOR_EMAIL,
    maintainer=MAINTAINER,
    maintainer_email=MAINTAINER_EMAIL,
    packages=PACKAGES,
    include_package_data=INCLUDE_PACKAGE_DATA,
    package_data=PACKAGE_DATA,
    url=URL,
    download_url=DOWNLOAD_URL,
    classifiers=CLASSIFIERS,
    platforms=PLATFORMS,
    license=LICENSE,
    install_requires=REQUIRES,
    entry_points={
        'console_scripts': ['paper_manager=paper_manager.main:main'],
    }
)