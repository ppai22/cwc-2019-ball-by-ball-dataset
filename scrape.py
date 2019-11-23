import time
import pandas as pd
from collections import OrderedDict
from bs4 import BeautifulSoup
from selenium import webdriver
import requests
from pynput.mouse import Controller


def fetch_urls():
    """Method that fetches the URLs for all the matches of CWC 2019"""
    # Initialization of return variable
    url_list = list()
    # Link where fixtures are listed
    url = 'https://www.cricketworldcup.com/fixtures'
    # Fetch page source using requests
    page_source = requests.get(url).text
    # Fetching the HTML content
    soup = BeautifulSoup(page_source, 'lxml')
    # Finding the container with the list of matches
    container = soup.find('div', class_='match-list__wrapper js-matchlist')
    # Looping over all the matches
    for match in container.find_all('div', class_='match-block__body col-12'):
        # Appending the fetched URL
        url_list.append(match.a['href'])
    # Sorting of URLs from first to last match
    url_list.sort()
    # Returning the list
    return url_list


def launch_driver():
    """Method that launches Chrome webdriver for Selenium"""
    driver = webdriver.Chrome()
    return driver


def terminate_driver(driver):
    """Method that terminates the launched web driver"""
    driver.close()


def scroll_down():
    """Method that simulates mouse scroll"""
    # Initializing controller
    mouse = Controller()
    # Go to location
    mouse.position = (250, 750)
    # Scroll by 3000 px
    mouse.scroll(0, -3000)


def fetch_content_from_match(driver, url):
    """Method that fetches content for every match"""
    # Fetch the site using Selenium
    driver.get('https://www.cricketworldcup.com' + url)
    # Wait for two seconds
    time.sleep(2)
    # Go to 'Ball By Ball' tab
    driver.find_element_by_xpath('/html/body/main/div[2]/div[1]/header/nav/ul/li[2]/span').click()
    # Wait for two seconds
    time.sleep(2)
    # Scroll down and click on 'Show More'
    driver.find_element_by_css_selector('body > main > div.match-centre-page__section.match-centre-page__section--left.js-mc-section-left > div.commentary.js-ct.tab-content.js-tab-content.t-cwc > div > div.commentary__bbb.js-bbb-container > footer > button').click()
    # Fetch current time
    time_start = time.time()
    while True:
        try:
            # Added time-out if loading web page took more than 45 seconds
            if time.time() - time_start > 45:
                break
            # Break the loop as soon as bottom of page is reached
            driver.find_element_by_css_selector('#chunk1 > li:nth-child(48) > div > div')
            break
        except:
            # Scroll down until bottom of page is reached in try part
            scroll_down()
    # Fetch HTML content
    page_source = driver.page_source
    # Parse the HTML using bs4
    soup = BeautifulSoup(page_source, 'lxml')
    # Left section of the page containing the ball-by-ball commentary
    section = soup.find('div', class_='match-centre-page__section match-centre-page__section--left js-mc-section-left')
    # Finding the commentary pane
    commentary_pane = section.find('div', class_='commentary__content js-body-content')
    # Finding containers
    container = commentary_pane.find('div', class_='commentary__bbb js-bbb-container')
    inner_container = container.find('div', 'js-chunks-container')
    # Finding each over
    ul = inner_container.findChildren()
    # Initializing variables to store the fetched data
    runs = list()
    balls = list()
    statements = list()
    # Parsing through each over
    for item in ul:
        # Finding each ball bowled
        li = item.find_all('li', class_='commentary__item')
        # Parsing each ball
        for i in li:
            # Finding the content for each ball
            commentary_block = i.find('div', class_='commentary-block')
            # Finding the runs scored in the ball
            for run in commentary_block.find_all('div', class_='commentary-block__ball'):
                runs.append(run.text.strip())
            # Finding the ball number in < OVER.BALL > format
            for ball in commentary_block.find_all('div', class_='commentary-block__over'):
                balls.append(ball.text.strip())
            # Finding the commentary statement for the ball
            for statement in commentary_block.find_all('div', class_='commentary-block__text'):
                # Added handling the case of super over in the final
                if 'Super Over' not in statement.p.text.strip():
                    statements.append(statement.p.text.strip())
    teams, time_start = [statements[-1]], [statements[-2]]
    # Terminating the driver
    terminate_driver(driver)
    # Initialize an ordered dict
    data_dict = OrderedDict()
    data_dict['Ball'] = [ball for ball in balls]
    data_dict['Runs'] = [run for run in runs]
    data_dict['Commentary'] = [statement for statement in statements[:-2]]
    # Return dict
    return data_dict


def write_to_csv(data_dict, file_name):
    """Method that writes content to a CSV file"""
    # Create a Pandas data frame
    df = pd.DataFrame(data_dict)
    # Write the data to a CSV file
    df.to_csv(file_name, index=False)


if __name__ == '__main__':
    # Fetch URLs
    urls = [fetch_urls()[-1]]
    # Fetch content for each match
    for url in urls:
        # Launch driver
        driver = launch_driver()
        try:
            # Fetch content
            data_dict = fetch_content_from_match(driver, url)
            # File to be written
            file = './Commentary Dump/' + url.split('.')[0].split('/')[-1] + '.csv'
            # Write to CSV file
            write_to_csv(data_dict, file)
        except:
            print(url)
            # Terminate driver
            terminate_driver(driver)
