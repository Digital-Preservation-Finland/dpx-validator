from setuptools import setup, find_packages

setup(name="dpxv",
      version="0.1",
      packages=find_packages(),
      entry_points={'console_scripts':
          ["dpxv=dpx_validator.dpxv:main"]}
)
