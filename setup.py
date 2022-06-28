from setuptools import setup

setup(
    name = 'flatten_json',
    author = 'Simon Takita',
    url = 'https://github.com/stakita/flatten_json',
    version = '0.1',
    packages = ['flatten'],
    entry_points = {
        'console_scripts': ['flatten = flatten:main']
    }
)
