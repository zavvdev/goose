from setuptools import find_packages, setup

def read_requirements():
  with open("requirements.txt", "r") as req:
    content = req.read()
    requirements = content.split("\n")
  return requirements

setup(
  name="goose",
  version="1.0",
  packages=find_packages(),
  include_package_data=True,
  install_requires=read_requirements(),
  entry_points="""
      [console_scripts]
      goose=goose.cli:cli
  """,
)
