import time
from selenium import webdriver
from selenium.webdriver.firefox.options import Options
from bs4 import BeautifulSoup
from threading import Thread
from multiprocessing import cpu_count
from tqdm import tqdm
import json

# Основная ссылка на Google Play
HOST = 'https://play.google.com'


def get_full_html(url, params=None):
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='driver/geckodriver', options=options)
    driver.get(url)
    while True:
        cur_height = driver.execute_script("return document.body.scrollHeight")
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight)")
        time.sleep(1)
        height_after_load = driver.execute_script("return document.body.scrollHeight")
        if cur_height == height_after_load:
            break
    html = driver.page_source
    driver.quit()
    return html


def get_primary_info(html):
    soup = BeautifulSoup(html, 'html.parser')
    items = soup.find_all('div', class_='vU6FJ p63iDd')
    apps = {}

    for i, item in enumerate(items, 1):
        average_rating = item.find('div', class_='pf5lIe')
        if average_rating is not None:
            average_rating = average_rating.find_next('div').get('aria-label').split()[1]
        apps[i] = {
            'name': item.find('div', class_='WsMG1c nnK0zc').get_text(strip=True),
            'author': item.find('div',  class_='KoLSrc').get_text(strip=True),
            'average_rating': average_rating,
            'link': HOST + item.find('div', class_='b8cIId ReQCgd Q9MA7b').find_next('a').get('href'),
        }
    return apps


def get_full_info(apps, id, keyword):

    link = apps[id]['link']
    options = Options()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    options.add_argument('--headless')
    driver = webdriver.Firefox(executable_path='driver/geckodriver', options=options)
    driver.get(link)
    html = driver.page_source
    driver.quit()
    soup = BeautifulSoup(html, 'html.parser')
    app = soup.find('main', class_='LXrl4c')
    apps[id]['description'] = app.find('div', class_='DWPxHb').find_next('div').get_text()
    if apps[id]['description'].lower().find(keyword) == -1 \
            and apps[id]['name'].lower().find(keyword) == -1:
        apps.pop(id)
        return
    apps[id]['category'] = app.find('a', class_='hrTbp R8zArc').get_text()
    apps[id]['number_of_ratings'] = app.find('span', class_='AYi5wd TBRnV').find_next('span').get_text()
    apps[id]['last_update'] = app.find('span', class_='htlgb').get_text()


def parse(url, keyword):
    html = get_full_html(url)
    apps = get_primary_info(html)
    threads = [Thread(target=get_full_info, args=(apps, id, keyword)) for id in apps.keys()]
    iteration_count = cpu_count()-1
    count_per_iteration = len(threads) / float(iteration_count)
    for iter_num in tqdm(range(0, iteration_count),
                         desc=f'Processing pages with {int(count_per_iteration)} threads'):
        start = int(count_per_iteration * iter_num)
        end = int(count_per_iteration * (iter_num + 1))
        for t in threads[start:end]:
            t.daemon = True
            t.start()
            t.join()
    return apps


if __name__ == '__main__':
    keyword = "сбербанк"
    url = HOST + f'/store/search?q={keyword}&c=apps'
    apps = parse(url, keyword)
    with open(f'data/{keyword}.json', 'w') as file:
        json.dump(apps, file)