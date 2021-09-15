from setuptools import setup, find_packages

setup(
    name='precon',
    version='0.1',
    description='Software for robot which is running on Raspberry PI ZERO',
    author='Albert Suraliński',
    author_email='albert.suralinski@gmail.com',
    packages=find_packages("src", exclude=["tests", ".gitignore", "README.md", "pytest.ini"]),
    package_dir={"": "src"},
    install_requires=['RPi.GPIO=<0.7.0'],
)
