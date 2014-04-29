# -*- coding: utf-8 -*-
from distutils.core import setup

setup(
    name='python-munin',
    version='0.1.1',
    author='Mengchen LEE',
    author_email='CooledCoffee@gmail.com',
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
        'test': ['fixtures'],
    },
    install_requires=[
        'inflection',
    ],
    packages=[
        'munin',
    ],
    url='https://github.com/CooledCoffee/python-munin/',
)
