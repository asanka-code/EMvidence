#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""The setup script."""

from setuptools import setup, find_packages

with open('README.rst') as readme_file:
    readme = readme_file.read()

with open('HISTORY.rst') as history_file:
    history = history_file.read()

requirements = ['pyside2', 'loguru', 'SigMF', 'fuzzywuzzy', 'attrs', 'reportlab', 'joblib', 'scikit-learn',
                'matplotlib', 'requests', 'pyzmq', 'execnet']

setup_requirements = []

test_requirements = []

setup(
    author="Main Author",
    author_email='miscdev@mailworks.org',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)',
        'Natural Language :: English',
        "Programming Language :: Python :: 2",
        'Programming Language :: Python :: 2.7',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
    ],
    description="GUI for RF Forensics Toolkit",
    install_requires=requirements,
    license="GNU General Public License v3",
    long_description=readme + '\n\n' + history,
    include_package_data=True,
    keywords='maingui',
    name='maingui',
    packages=find_packages(include=['maingui', 'maingui.WebStorage', 'maingui.RFSource',
                                    'maingui.RFSource.RadioInterface']),
    setup_requires=setup_requirements,
    entry_points={
        'console_scripts': [
            'rftoolkitgui = maingui:main',
        ],
    },
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/miscdev/maingui',
    version='0.1.0',
    zip_safe=False,
)
