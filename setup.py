#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['Click>=6.0', 'flake8-pytest-mark>=1.0.0,<2.0.0', 'flake8', 'flake8-json', 'six']
packages = ['magic_marker']
entry_points = {
    'console_scripts': [
        'magic-marker=magic_marker.cli:main',
    ],
}

setup(
    name='magic-marker',
    version='1.0.0',
    author="rcbops",
    author_email='rpc-automation@rackspace.com',
    maintainer='rcbops',
    maintainer_email='rpc-automation@rackspace.com',
    license="Apache Software License 2.0",
    url='https://github.com/rcbops/magic-marker',
    keywords='magic_marker',
    description="Automatically mark pytest tests with a UUID",
    long_description=readme + '\n\n' + history,
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: Apache Software License',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Operating System :: OS Independent',
    ],
    install_requires=requirements,
    packages=packages,
    include_package_data=True,
    zip_safe=False,
    entry_points=entry_points,
)
