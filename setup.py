from setuptools import setup, find_packages

def read_requirements(file):
    with open(file) as f:
        return f.read().splitlines()

VERSION = "0.0.1"
DESCRIPTION = "BB_data"
LONG_DESCRIPTION = "BB_data"
REQUIREMENTS = read_requirements("requirements.txt")

# Setting up
setup(
    name="BB_data",
    version=VERSION,
    author="Daniel Halls",
    author_email="daniel.j.halls@kcl.ac.uk>",
    description=DESCRIPTION,
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    install_requires=REQUIREMENTS,
    classifiers= [
            "Development Status :: Alpha",
            "Intended Audience :: BB data analysis ream",
            "Programming Language :: Python :: 3",
            "Operating System :: OS Independent"
            ])
