# CWC 2019 Ball-By-Ball Dataset
Ball-by-ball data set generated out of the commentary data scraped for every match of the ICC Cricket World Cup 2019 from the ICC website

### Requirements
- Python version: 3.7.4
- Python modules: pandas, selenium, pynput, requests, time, bs4, collections
- Executables: chormedriver (either in the same folder as the code or set in PATH)

### Process followed
The file to be run is ```script.py```.
It uses Beautiful Soup, Requests and Selenium with Chrome webdriver to scrape text commentary from [the official ICC site for the CWC 2019](https://www.cricketworldcup.com/).
The following data is fetched from the commentary:
- Ball and over number
- Runs scored or wicket in that ball
- Text commentary for the ball as available

### Further work to be done
- Find another way to scroll down the commentary other than the current pynput to make the web scraping look more cleaner and implementation of headless chrome
- Cleaning of the dataset formed and fetching features from commentary
- Following features need to be or can be fetched: batsman, bowler, speed of the ball, type of ball, length of the ball, type of dismissal
- Analyzing and understanding the data and providing visualization and easy way of fetching data using filters
- Generate a shiny dahsboard for certain features in R for better visualization of the data

All data is available as published in [the official ICC site for the CWC 2019](https://www.cricketworldcup.com/).
No part of this project will be used for commercial purposes by me and will solely be used for academic purposes.
