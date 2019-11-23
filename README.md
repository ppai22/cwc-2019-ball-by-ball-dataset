# cwc-2019-ball-by-ball-dataset
Ball-by-ball data set generated out of the commentary data scraped for every match of the ICC Cricket World Cup 2019 from the ICC website

### Requirements
- Python version: 3.7.4
- Python modules: pandas, selenium, pynput, requests, time, bs4, collections
- Executables: chormedriver (either in the same folder or set in PATH)

### Process followed
The file to be run is ```script.py```.
It uses Beautiful Soup, Requests and Selenium with Chrome webdriver to scrape text commentary from [the official ICC site for the CWC 2019](https://www.cricketworldcup.com/).
The following data is fetched from the commentary:
- Ball and over number
- Runs scored or wicket in that ball
- Text commentary for the ball as available

### Further work to be done
- Cleaning of the dataset formed and fetching features from commentary
- Following features need to be or can be fetched: batsman, bowler, speed of the ball, type of ball, length of the ball, type of dismissal
- Analyzing and understanding the data and providing visualization and easy way of fetching data using filters

All data is available as published in [the official ICC site for the CWC 2019](https://www.cricketworldcup.com/).
No part of this project will be used for commercial purposes by me and will solely be used for academic purposes.
