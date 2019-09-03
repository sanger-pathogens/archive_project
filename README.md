# archive_project
Backup the pipeline results to S3

[![Build Status](https://travis-ci.org/sanger-pathogens/seroba.svg?branch=master)](https://travis-ci.org/sanger-pathogens/seroba)   
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/sanger-pathogens/seroba/blob/master/LICENSE)   
[![install with bioconda](https://img.shields.io/badge/install%20with-bioconda-brightgreen.svg)](http://bioconda.github.io/recipes/seroba/README.html)  
[![Container ready](https://img.shields.io/badge/container-ready-brightgreen.svg)](https://quay.io/repository/biocontainers/seroba)  
[![Docker Build Status](https://img.shields.io/docker/build/sangerpathogens/seroba.svg)](https://hub.docker.com/r/sangerpathogens/seroba)  
[![Docker Pulls](https://img.shields.io/docker/pulls/sangerpathogens/seroba.svg)](https://hub.docker.com/r/sangerpathogens/seroba)  
[![codecov](https://codecov.io/gh/sanger-pathogens/mlst_check/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/mlst_check) 

## Contents (edit as fit)
  * [Introduction](#introduction)
  * [Installation](#installation)
    * [Required dependencies](#required-dependencies)
    * [Optional dependencies](#optional-dependencies)
    * [Linux specific instructions (Debian, Ubuntu, RedHat etc\.)](#linux-specific-instructions-debian-ubuntu-redhat-etc)
    * [Mac OS](#mac-os)
    * [Bioconda](#bioconda)
    * [Homebrew/Linuxbrew](#homebrewlinuxbrew)
    * [Docker](#docker)
    * [Virtual Machine](#virtual-machine)
    * [Galaxy](#galaxy)
    * [From Source](#from-source)
    * [Running the tests](#running-the-tests)
  * [Usage](#usage)
  * [License](#license)
  * [Feedback/Issues](#feedbackissues)
  * [Citation](#citation)
  * [Further Information](#further-information)

## Introduction
- A module which checks if a bucket for the database already exists on S3 and, if not, creates one 
- A module to find all of the studies for a given database 
- A module to find the paths to the data for each study 
- A module to filter out files that do not need to be archived 
- A module to do the actual backup 

## Installation
There are a number of ways to install <software name> and details are provided below. If you encounter an issue when installing <software name> please contact your local system administrator. If you encounter a bug please log it [here](link_to_github_issues_page) or email us at path-help@sanger.ac.uk <or appropriate tool email list e.g. iva@sanger.ac.uk>.

### Required dependencies
  * Python 3.6

### From source 

Download the latest release from this github repository or clone it. Run the tests:
	
	python3 setup.py test

If the tests all pass, install: 
	
	python3 setup.py install 
	
Alternatively, install directly from github using:

	pip3 install git+https://github.com/sanger-pathogens/archive_project.git #--user
	


## Usage
The installation will put a single script called archive_2S3 in your PATH. The usage is:

	archive_2S3 [options]

- To list the available commands and brief descriptions, just run 'archive_2S3 -h' or  'archive_2S3 -help'
- To display the version of the program, use 'archive_2S3 --version'



## License
<software name> is free software, licensed under [<license>](link_to_license_file_on_github).

## Feedback/Issues
Please report any issues to the [issues page](link_to_github_issues_page) or email path-help@sanger.ac.uk <or appropriate tool email list e.g. iva@sanger.ac.uk>.

