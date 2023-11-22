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

## Best Flow with Crew.txt
```shell
$ poetry install
$ poetry shell
$ python -m src --images chapter_1/ --easy-ocr True --crew-list crew.txt
```
> **Note:** Validate the scores and you can pull the crew list from lotr.gg. The Crew List needs to be new line separated player_ids.
> This outputs ranking.csv and totals.csv. Totals is just to validate attempts made. Ranking.csv is the conversion of the actual.
> You can open ranking.csv and sort by line number. This will duplicate scores if they show up more than once. 

#### Example of crew.txt
```csv
player_id_1
player_id_2
player_id_3
```

> **Note:** Why is this needed? Js and some other characters are hard to read with the current font used haha. 
> I use fuzzy match to make sure I have the right player_ids with 85% match rate or above

```shell
$ python -m src --csv ranking.csv
```
> **Note:** This outputs attempts.csv - which is the pivot of ranking.csv without the rank and number of attempts and total. 

## Secondary Flow
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