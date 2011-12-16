#/usr/bin/env python

from numpy.distutils.misc_util import Configuration
from numpy.distutils.core import setup

DESCRIPTION = "Performance benchmarking and monitoring tool"
LONG_DESCRIPTION = """
Performance benchmarking and monitoring tool
"""

REQUIRES = ['sqlalchemy', 'pandas']
DISTNAME = 'gitbench'
LICENSE = 'BSD'
AUTHOR = "Wes McKinney"
AUTHOR_EMAIL = "wesmckinn@gmail.com"
URL = "https://github.com/wesm/gitbench"
CLASSIFIERS = [
    'Development Status :: 2 - Pre-Alpha',
    'Environment :: Console',
    'Operating System :: OS Independent',
    'Intended Audience :: Science/Research',
    'Programming Language :: Python',
    'Topic :: Scientific/Engineering',
]

MAJOR = 0
MINOR = 1
ISRELEASED = False
VERSION = '%d.%d' % (MAJOR, MINOR)

FULLVERSION = VERSION
if not ISRELEASED:
    FULLVERSION += '.beta'

def configuration(parent_package='', top_path=None):
    config = Configuration(None, parent_package, top_path,
                           version=FULLVERSION)
    config.set_options(ignore_setup_xxx_py=True,
                       assume_default_configuration=True,
                       delegate_options_to_subpackages=True,
                       quiet=True)

    config.add_subpackage('gitbench')
    config.add_data_dir('gitbench/tests')
    return config

if __name__ == '__main__':
    setup(name=DISTNAME,
          author=AUTHOR,
          author_email=AUTHOR_EMAIL,
          description=DESCRIPTION,
          license=LICENSE,
          url=URL,
          long_description=LONG_DESCRIPTION,
          classifiers=CLASSIFIERS,
          platforms='any',
          configuration=configuration)
