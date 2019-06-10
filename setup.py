from setuptools import setup, find_packages

from version import get_version

setup(
    name="dpx-validator",
    version=get_version(),
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': ["dpxv=dpx_validator.dpxv:main"]
    }
)
