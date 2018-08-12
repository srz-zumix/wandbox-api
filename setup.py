import os
from setuptools import setup

f = open(os.path.join(os.path.dirname(__file__), 'README.md'))
readme = f.read()
f.close()

VERSION = "0.3.7"

setup(
	name = "wandbox-api"
	, version = VERSION
	, author = "Takazumi Shirayanagi"
	, author_email = "zumix.cpp@gmail.com"
	, url = "https://github.com/srz-zumix/wandbox-api/"
	, description = "A Python binding to the Wandbox API."
	, license = "MIT"
	, platforms = ["any"]
	, keywords = "API, Wandbox"
	, packages = ['wandbox']
	, long_description = readme
	, classifiers = [
		"Development Status :: 3 - Alpha"
		, "Topic :: Utilities"
		, "License :: OSI Approved :: MIT License"
	]
	, install_requires=['requests']
)
	