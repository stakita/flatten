from setuptools import setup

setup(
    name = 'flatten_json',
    author = 'Simon Takita',
    url = 'https://github.com/stakita/flatten_json',
    version = '0.1',
    packages = ['flatten_json'],
    entry_points = {
        'console_scripts': ['flatten_json = flatten_json:main']
    }
)