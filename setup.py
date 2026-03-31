import re
from os.path import join, dirname

from setuptools import setup, find_packages


# reading package version (same way the sqlalchemy does)
with open(join(dirname(__file__), 'boilerplate/manifest.py')) as v_file:
    package_version = re.compile('.*__version__ = \'(.*?)\'', re.S).\
        match(v_file.read()).group(1)


dependencies = [
    'yhttp >= 7.14, < 8',
    'yhttp-auth >= 7.0.1, < 8',
    'yhttp-i18n >= 1.6.0, < 2',
    'yhttp-mako >= 1.2.0, < 2',
    'yhttp-media >= 1, < 2',
    'yhttp-dbmanager >= 6.0.2, < 7',
    'yhttp-sqlalchemy >= 4.2.1, < 5',
    'babel >= 2.18, < 3',
    'httpx',
    'redis',
]


setup(
    name='yhttp-ssr-boilerplate',
    version=package_version,
    install_requires=dependencies,
    author='Vahid Mardani',
    author_email='vahid.mardani@gmail.com',
    maintainer='Vahid Mardani',
    maintainer_email='vahid.mardani@gmail.com',
    packages=find_packages(
        where='.',
        include=['boilerplate'],
        exclude=['tests']
    ),
    entry_points={
        'console_scripts': [
            'boilerplate = boilerplate:app.climain'
        ]
    },
)
