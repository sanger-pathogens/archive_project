# archive_project
Tool to back up the data produced by the Pathogen Informatics sequencing pipelines to an S3 server

[![Build Status](https://travis-ci.com/sanger-pathogens/archive_project.svg?branch=master)](https://travis-ci.com/sanger-pathogens/archive_project)   
[![License: GPL v3](https://img.shields.io/badge/License-GPL%20v3-brightgreen.svg)](https://github.com/sanger-pathogens/archive_project/blob/master/LICENSE)   
[![codecov](https://codecov.io/gh/sanger-pathogens/archive_project/branch/master/graph/badge.svg)](https://codecov.io/gh/sanger-pathogens/archive_project) 

## Contents
  * [Introduction](#introduction)
  * [Installation](#installation)
    * [Required dependencies](#required-dependencies)
    * [From Source](#from-source)
  * [Usage](#usage)

## Introduction
This software backs up data produced by the Pathogen Informatics sequencing pipelines to an S3 server, thereby automatically creating missing buckets.
It can either take a study name or a file with a list of studies as input. The pipeline data created for the chosen study/studies is traced with  [pf](https://github.com/sanger-pathogens/Bio-Path-Find) and then uploaded/synchronized with the data on the S3 server.
NOTE: Temporary files and files that are easily reproducible (BAM, FASTQ) are ignored to speed up the process.

## Installation

### Required dependencies
  * Python 3.7
  * s3cmd
  * [pf](https://github.com/sanger-pathogens/Bio-Path-Find)

### From source
Download the latest release from this GitHub repository or clone it. Run the tests:
	
	python3 setup.py test

If the tests all pass, install: 
	
	python3 setup.py install 
	
## Usage
The installation will put a single script called archive_2S3 in your PATH. The usage is:

	archive_2S3 [options]

To list the available commands and brief descriptions, just run `archive_2S3 -h` or  `archive_2S3 --help`.
To display the version of the program, use `archive_2S3 --version`.
Full usage options:

```
  -h, --help            show this help message and exit
  --type TYPE, -t TYPE  ID type. Use "file" to read IDs from file [Required;
                        Possible values: file, studies] (default: None)
  --id ID, -i ID        study names or file containing list of studies,
                        seprated by a comma (default: None)
  --database DATABASE, -d DATABASE
                        database containing studies to be archived (default:
                        None)
  --bucket_name BUCKET_NAME, -b BUCKET_NAME
                        bucket to backup data to (default: None)
  --data_root DATA_ROOT, -r DATA_ROOT
                        root of data to be removed when uploading to s3.
                        Typically /lustre/scratch118/infgen/pathogen/pathpipe/
                        <database>/seq-pipelines/ (default: None)
  --failures FAILURES, -f FAILURES
                        output file to write any failed lanes to (default:
                        None)
  --version, -v         show program's version number and exit
```
