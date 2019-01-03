"""Based on: https://github.com/pypa/sampleproject."""

from setuptools import find_packages, setup
from os import path

# Get the long description from the README file
with open(path.join(path.abspath(path.dirname(__file__)), 'README.rst')) as f:
    long_description = f.read()

setup(
    name='labelling_web_app',

    # Versions should comply with PEP440.  For a discussion on single-sourcing
    # the version across setup.py and the project code, see
    # https://packaging.python.org/en/latest/single_source_version.html
    version='0.0.1',

    description='Web app to label objects in images',
    long_description=long_description,

    url='https://github.com/ThundeRatz/labelling-web-app',

    author='Tiago Koji Castro Shibata',
    author_email='tiago.shibata@thunderatz.org',

    license='MIT',

    classifiers=[
        'Development Status :: 4 - Beta',

        'Intended Audience :: Developers',
        'Topic :: Multimedia :: Graphics',

        'License :: OSI Approved :: MIT License',

        'Programming Language :: Python :: 3',
    ],

    keywords='label detection',

    packages=find_packages(),

    # For an analysis of "install_requires" vs pip's requirements files see:
    # https://packaging.python.org/en/latest/requirements.html
    install_requires=['flask', 'gevent', 'gunicorn', 'psycopg2', 'requests'],

    # If there are data files included in your packages that need to be
    # installed, specify them here.
    package_data={
        'labelling_web_app': [
            'static/*', 'templates/*.html'
        ]
    },

    # Although 'package_data' is the preferred approach, in some case you may
    # need to place data files outside of your packages. See:
    # http://docs.python.org/3.4/distutils/setupscript.html#installing-additional-files # noqa
    # In this case, 'data_file' will be installed into '<sys.prefix>/my_data'
    data_files=[],

    # To provide executable scripts, use entry points in preference to the
    # "scripts" keyword. Entry points provide cross-platform support and allow
    # pip to create the appropriate form of executable for the target platform.
    entry_points={},
)
