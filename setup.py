import setuptools
import os

with open("README.md", "r") as fh:
    long_description = fh.read()

DIR = os.path.dirname(os.path.abspath(__file__))
INSTALL_PACKAGES = open(os.path.join(DIR, "requirements.txt")).read().splitlines()

print(INSTALL_PACKAGES)

setuptools.setup(
    name="figlet-to-pygamelib",
    version="0.1.0",
    author="Arnaud Dupuis",
    author_email="8bitscoding@gmail.com",
    description="A small script to automatically convert Figlet fonts to the "
    "Pygamelib's sprite format.",
    long_description=long_description,
    long_description_content_type="text/markdown",
    install_requires=INSTALL_PACKAGES,
    url="https://www.pygamelib.org",
    packages=setuptools.find_packages(),
    scripts=["figlet-to-pygamelib.py"],
    keywords=["development", "console", "terminal", "font"],
    classifiers=[
        "Programming Language :: Python :: 3",
        "Programming Language :: Python :: 3.6",
        "Programming Language :: Python :: 3.7",
        "Programming Language :: Python :: 3.8",
        "Programming Language :: Python :: 3.9",
        "Programming Language :: Python :: 3.10",
        "Development Status :: 4 - Beta",
        "Environment :: Console",
        "Topic :: Terminals",
        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
        "Operating System :: OS Independent",
    ],
    project_urls={
        "Documentation": "https://github.com/pygamelib/figlet-to-pygamelibl",
        "Source": "https://github.com/pygamelib/figlet-to-pygamelib",
        "Tracker": "https://github.com/pygamelib/figlet-to-pygamelib/issues",
    },
    python_requires=">=3.6",
)
