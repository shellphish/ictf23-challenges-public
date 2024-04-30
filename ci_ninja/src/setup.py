import os

from setuptools import setup, find_packages

# assert 'VIRTUAL_ENV' in os.environ, "Cannot install outside of a Python virtualenv"

setup(
    name='ci_ninja',
    version='0.1.0',
    packages=find_packages(),
    install_requires=[
        'openai==0.28.0',
        'tiktoken'
    ],
    python_requires='>=3.8',
)