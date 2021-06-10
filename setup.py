from setuptools import setup, find_packages
import codecs
from os import path
this_directory = path.abspath(path.dirname(__file__))
VERSION = '0.1.6'
DESCRIPTION = 'Python Wrapper for Newweb Nepse'
with open(path.join(this_directory, 'README.md'), encoding='utf-8') as f:
    LONG_DESCRIPTION = f.read()

# Setting up
setup(
    name="nepse",
    version=VERSION,
    author="FRAPPÉ (FRAPPÉ#4101)",
    description=DESCRIPTION,
    long_description_content_type="text/markdown",
    long_description=LONG_DESCRIPTION,
    packages=find_packages(),
    url='https://github.com/pyFrappe/nepse',  
    install_requires=['requests','matplotlib','pandas'],
    keywords=['python', 'nepse', 'stock', 'nepal stock', 'nepal stock prices', 'nepse pythonb']
)

