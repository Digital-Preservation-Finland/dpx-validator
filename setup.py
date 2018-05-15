from setuptools import setup, find_packages

setup(name="dpxv",
      version="0.1",
      packages=find_packages(),
      entry_points={'console_scripts':
          ["dpxv=dpxv.dpxv:main"]}
)
