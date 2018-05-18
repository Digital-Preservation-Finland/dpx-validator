from setuptools import setup, find_packages

setup(name="dpx-validator",
      version="0.1",
      packages=find_packages(exclude=['tests']),
      entry_points={'console_scripts':
          ["dpxv=dpx_validator.dpxv:main"]}
)
