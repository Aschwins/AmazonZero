import os
from setuptools import setup, find_packages

deploy_packages = [
    "numpy",
    "scipy",
    "pandas",
    "scikit-learn",
    "click",
    "matplotlib"]
    
dev_packages = [
    "jupyterlab"
    ]


setup(
    name='amazonzero',
    version="1.0.0",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    install_requires=deploy_packages,
    description='',
    extras_require={
        'dev': dev_packages
    },
    entry_points = {"console_scripts": ["package-name = amazonzero.cli:main"]},
    author='Aschwin Schilperoort',
    long_description_content_type='text/markdown',
)
