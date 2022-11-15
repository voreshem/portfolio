import os
from multiprocessing import Pool
import requests
from bs4 import BeautifulSoup

url = "https://cdn.star.nesdis.noaa.gov/GOES16/ABI/SECTOR/taw/GEOCOLOR/"
r = requests.get(url)

soup = BeautifulSoup(r.content, 'html5lib')
links = soup.findAll('a')

highres_list = [link['href'] for link in links if link['href'].endswith('GOES16-ABI-taw-GEOCOLOR-7200x4320.jpg')]
highres_links = [url + link for link in highres_list]

def download(link):
    file = link.split('/')[-1]
    os.system(f'echo "Downloading: {file}"')    
    with open(file, 'wb') as f:
        r = requests.get(link)
        image = r.content
        f.write(image)

if __name__ == '__main__':
    
    cpus = os.cpu_count()
    
    with Pool(processes=cpus) as p:
        p.map(download, highres_links)
