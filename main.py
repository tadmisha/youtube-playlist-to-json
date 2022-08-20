from bs4 import BeautifulSoup as bs
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException as NSEE
import json
from time import sleep
from pprint import pprint as print

def get_info(url):
    try:
        browser = webdriver.Chrome(r'D:\Programming\Python\Projects\login\chromedriver.exe')
        browser.get(url)
        while True:
            try:
                browser.find_element(By.XPATH, '//div[@id="container"][@class="style-scope ytd-playlist-panel-video-renderer"]')
                break
            except NSEE: pass
        sleep(2)
        soup = bs(browser.page_source, 'html.parser')
        with open('index.html', 'w', encoding='utf-8') as file: file.write(browser.page_source)
    except Exception as ex:
        print(type(ex))
    finally:
        browser.close()
        browser.quit()

    info = [{'url': 'https://www.youtube.com'+el.find('a').get('href')[0:el.find('a').get('href').index('&')],
              'text': el.find('span', id='video-title').text.replace('\n', '').replace('  ', ''),
              'time': el.find('span', id='text').text.replace(' ','').replace('\n',''),
              'index': el.find('span', id='index').text.replace('▶','1'),
              'channel': el.find('span', id='byline').text}
            for el in soup.find_all(id="playlist-items")]

    return info

def info_to_json(info):
    with open("sample.json", "w", encoding='utf-8') as outfile:
        json.dump(info, outfile, indent=4)

def main():
    url = input('Youtube playlist url: ')
    info = get_info(url)
    info_to_json(info)
    print(info)

if __name__ == '__main__':
    main()
