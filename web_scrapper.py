from random import randint
import time 
from time import sleep
from urllib.parse import urljoin
import requests
from bs4 import BeautifulSoup
from tqdm import tqdm
import csv
from concurrent import futures
start = time.time()

URL = "http://books.toscrape.com/"
URL2 = "https://www.w3schools.com/"
URL3 = "https://en.wikipedia.org/"
URL4 = 'https://www.bbc.com/'


MAX_WORKERS = 25

# Maximum timeout to download a page (in seconds)
MAX_TIMEOUT = 3

# Number of retries
NUM_RETRIES = 3
list_links = []


def download_page(url):
    retries = 0
    while retries < NUM_RETRIES:
        try:
            response = requests.get(url, timeout=MAX_TIMEOUT)
            response.raise_for_status()
            return response
        except (requests.exceptions.RequestException, requests.exceptions.HTTPError) as e:
            print(f"Error downloading page: {e}")
            retries += 1
    return None       

def scrap_data(link):

    with open("data3.csv", mode='a', newline='') as file:
        writer = csv.writer(file)
        # for link in tqdm(urls):
        r = download_page(link)
        soup = BeautifulSoup(r.text, 'html.parser')
        h1s = []
        h2s = []
        h3s = []
        for h1 in soup.find_all('h1'):
            h1s.append(h1.text.strip())

        for h2 in soup.find_all('h2'):
            h2s.append(h2.text.strip())

        for h3 in soup.find_all('h3'):
            h3s.append(h3.text.strip())

        sleep(randint(8,15))

        writer.writerow([link,soup.title.text,h1s,h2s,h3s,len(r.content),r.status_code,r.elapsed.total_seconds()])


def scrap_links(url, num_pages):

            response = download_page(url)
            soup = BeautifulSoup(response.text, 'html.parser')

            for link in soup.find_all('a', href = True):

                # if str(link['href']).startswith('#'):
                #     pass
        
                if str(link['href']).startswith(str(url)):
                    formatted_link = link['href']
                    if formatted_link not in list_links:
                        list_links.append(formatted_link)
                        print(formatted_link)
                        if (len(list_links)) >= num_pages:
                            return list_links
                        scrap_links(formatted_link, num_pages)

                # if str(link['href']).startswith('//en.wikipedia.org/wiki'):
                #     formatted_link = 'https:'+ link['href']
                #     if formatted_link not in list_links:
                #         list_links.append(formatted_link)
                #         print(formatted_link)
                #         if (len(list_links)) >= num_pages:
                #             return list_links
                        
                #         scrap_links(formatted_link, num_pages)
                        
                # formatting links starting /
                if str(link['href']).startswith('/'):
                    formatted_link = urljoin (URL4, link['href'][1:])
                    if formatted_link not in list_links:
                        list_links.append(formatted_link)
                        print(formatted_link)
                        if (len(list_links)) >= num_pages:
                            return list_links
                        
                        scrap_links(formatted_link, num_pages)
                # sleep(randint(8,15))
    
    
def scrap_data_con(link_list):
    workers = min(MAX_WORKERS, len(link_list))
    with futures.ThreadPoolExecutor(workers) as executor:
        res = executor.map(scrap_data, link_list)
    return res


l = scrap_links(URL4,11)

scrap_data_con(l)

end = time.time()
print(end - start)