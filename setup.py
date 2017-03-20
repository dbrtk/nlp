

from os import path
from setuptools import find_packages, setup

HERE = path.abspath(path.dirname(__file__))


setup(
    name='nlp',
    # version='0.1',
    description='Natural language processing.',
    long_description='',

    url='http://dbrtk.net',

    author='Dominik Bartkowski',
    author_email='dominik@dbrtk.net',

    classifiers=[

        'Environment :: Console',

        'Framework :: Flake8',
        'Framework :: Flask',
        'Framework :: IDLE',
        'Framework :: IPython',
        'Framework :: Django',
        'Framework :: Django :: 1.10',

        'Intended Audience :: Developers',
        'Intended Audience :: Education',
        'Intended Audience :: Science/Research',

        'Natural Language :: English',

        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.0',
        'Programming Language :: Python :: 3.1',
        'Programming Language :: Python :: 3.2',
        'Programming Language :: Python :: 3.3',
        'Programming Language :: Python :: 3.4',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3 :: Only',

        'Operating System :: POSIX :: Linux',
        'Operating System :: Unix',
    ],

    keywords='natural language processing',

    packages=find_packages(include=['nlp']),

    install_requires=['numpy', 'scipy', 'Pillow']
)
