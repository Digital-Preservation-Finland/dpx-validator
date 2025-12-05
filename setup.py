from setuptools import setup, find_packages

setup(
    name="dpx-validator",
    setup_requires=["setuptools_scm"],
    use_scm_version={
        "write_to": "dpx_validator/_version.py"
    },
    packages=find_packages(exclude=['tests']),
    include_package_data=True,
    entry_points={
        'console_scripts': ["dpx-validator=dpx_validator.main:main"]
    }
)
