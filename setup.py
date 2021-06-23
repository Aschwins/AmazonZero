from setuptools import setup, find_packages

setup(
    name='amazonzero',
    version="1.0.0",
    packages=find_packages(where='src'),
    package_dir={"": "src"},
    description='',
    author='Aschwin Schilperoort',
    long_description_content_type='text/markdown',
)
