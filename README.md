# Telegram Media Scraper via Python

Tele-Scrapper is a python program designed to scrap media content like images and video from telegram posts using HTTP requests and HTML parsing. It is idle for downloading content from Telegram without using Telegram API.

# Installation
This program was built using python 3.10.10 64bit
Python and the following dependencies are required to run the program

 - beautifulsoup4==4.11.1
 - html2text==2020.1.16
 - Requests==2.28.2

## Windows
Run the Install.bat to install python and required dependencies

## Other
Open a terminal and use the command to install dependencies:
```
pip install -r requirements.txt
```

# Usage

## Windows

Run the "Run.bat" file for the url scrapper
Run the "Run batch.bat" file for the batch scrapper, first edit the python file and edit the username in __init__ function

## Other
Open a terminal and run `python scrap.py` for the url scrapper

Open a terminal and run `python loop.py` for the batch scrapper, first edit the python file and edit the username in __init__ function

***Enter the telegram link and folder name (default: content) to use scrap.py***

***Enter the telegram id and folder name (default: content) to use loop.py***

# **NOTE: The loop.py is created for downloading from bulk posts in a channel, see inside to change the username of the channel**

# License
This project was originally created by stellio as [Telegrap-Post-Scrapper](https://https://github.com/Steelio/Telegram-Post-Scraper)

Later recreated by @SamratBarai
