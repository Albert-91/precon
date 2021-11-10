from setuptools import setup, find_packages
import sys
from precon import __version__ as version


if sys.platform == "linux":
    gpio_lib = "RPi.GPIO==0.7.0"
else:
    gpio_lib = "fake-rpi==0.7.1"

with open("README.md", "r", encoding="utf-8") as f:
    long_description = f.read()

setup(
    name="precon",
    version=version,
    description="Software for robot which is running on Raspberry PI ZERO",
    long_description=long_description,
    long_description_content_type="text/markdown",
    author="Albert Suraliński",
    author_email="albert.suralinski@gmail.com",
    url="https://github.com/Albert-91/precon",
    license="MIT",
    license_file="LICENSE",
    python_requires=">=3.8",
    package_dir={"": "src"},
    packages=find_packages(where="src"),
    install_requires=[
        gpio_lib,
        "click~=8.0.3"
    ],
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: POSIX :: Linux"
    ],
    entry_points={
        'console_scripts': [
            'precon-rc=precon.commands:remote_control',
            'precon-show-distance=precon.commands:show_distance',
        ],
    }
)
