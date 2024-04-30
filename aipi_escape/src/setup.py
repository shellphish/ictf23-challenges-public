import os

from setuptools import setup, find_packages

#assert 'VIRTUAL_ENV' in os.environ, "Cannot install outside of a Python virtualenv"

setup(
    name='aipi_escape',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'ipython==8.12.2',
        'tiktoken==0.4.0',
        'openai==0.28.0'
    ],
    python_requires='>=3.8',
)