# -*- coding: utf-8 -*-
from distutils.core import setup
import setuptools

setup(
    name='python-munin',
    version='0.3.2',
    author='Mengchen LEE',
    classifiers = [
        'Development Status :: 4 - Beta',
        'Intended Audience :: Developers',
        'Intended Audience :: System Administrators',
        'Operating System :: OS Independent',
        'Programming Language :: Python',
        'Programming Language :: Python :: 2',
        'Programming Language :: Python :: 3',
        'Topic :: System :: Monitoring',
    ],
    description='Framework for writing munin plugins.',
    extras_require={
        'test': ['fixtures2'],
    },
    install_requires=[
        'inflection',
        'six',
    ],
    package_dir={'': 'src'},
    py_modules=['munin'],
    url='https://github.com/cooledcoffee/python-munin',
)
