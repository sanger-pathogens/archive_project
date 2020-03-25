import os
import shutil
import sys
import glob
from setuptools import setup, find_packages

def read(fname):
    return open(os.path.join(os.path.dirname(__file__), fname)).read()

version = '0.0.1'.strip()

setup(
    name='archive_project',
    version=version,
    description='Archive nfs that isn\'t backed up or easily reproducible',
	long_description=read('README.md'),
    packages = find_packages(),
    author='Kathryn Murie',
    author_email='path-help@sanger.ac.uk',
    url='https://github.com/sanger-pathogens/archive_project/',
    scripts=glob.glob('scripts/*'),
    test_suite='nose.collector',
    tests_require=['nose >= 1.3'],
    install_requires=[
         'biopython >= 1.68',
         'testfixtures >= 6.14.0',
	 'boto3 >= 1.0.0', 
         #'pyfastaq >= 3.12.0'
       ],
    license='GPLv3',
    classifiers=[
        'Development Status :: 4 - Beta',
        'Intended Audience  :: Science/Research',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Programming Language :: Python :: 3 :: Only',
        'License :: OSI Approved :: GNU General Public License v3 (GPLv3)'
    ],
)


