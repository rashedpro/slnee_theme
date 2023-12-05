from setuptools import setup, find_packages

with open("requirements.txt") as f:
	install_requires = f.read().strip().split("\n")

# get version from __version__ variable in slnee_theme/__init__.py
from slnee_theme import __version__ as version

setup(
	name="slnee_theme",
	version=version,
	description="Slnee Theme",
	author="Baha",
	author_email="baha@slnee.com",
	packages=find_packages(),
	zip_safe=False,
	include_package_data=True,
	install_requires=install_requires
)
