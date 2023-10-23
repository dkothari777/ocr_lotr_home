# Lord of the Rings: Optical Character Recognition for Raid Battles

## Pre-Requisites

* Google Tesseract OCR in Path
* Python 3.11
* Poetry

### Mac Pre-Requisites Installation

```shell
$ brew install tesseract 
$ brew install poetry
$ brew install pyenv
$ pyenv install 3.11.5
$ pyenv global 3.11.5
```
> Requrires [Homebrew](https://brew.sh/)

## Run-It

```shell
$ poetry install
$ poetry shell
$ python -m src [directory of images | zipfile]
```

This will do one chapter at a time. This will generate two files rankings.csv and totals.csv. 
Rankings.csv is what it captured and totals.csv is the total number of battles and points players have scored for that round. 


## Issues
* 1 is difficult to read for tesseract especially if it is not around other numbers. So it will output -1. Commonly shown for difficulty. 
* -1 means it couldn't read it correctly. 