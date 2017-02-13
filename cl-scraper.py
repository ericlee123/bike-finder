import json
import os
import re
import sys
import time
from urllib.request import urlopen, urlretrieve

image_folder_path = "images/cl"

def scrape_bikes(city):
    base_url = "https://" + city + ".craigslist.org"
    first_page = base_url + "/search/bia"

    if not os.path.isdir(image_folder_path + "/" + city):
        os.makedirs(image_folder_path + "/" + city)

    html = urlopen(first_page).read()
    # regex = "https://" + city + "\.craigslist\.org(/([a-z])*)*/bik/[0-9]{10}.html"
    regex = r"(?:/[a-z]{3})*/bik/[0-9]{10}.html" # some suffixes have 3 char prefix in the beginning
    matches = re.findall(regex, html.decode('utf-8'))
    bike_pages = set()

    for m in matches:
        bike_pages.add(m)

    for bp in bike_pages:
        html = urlopen(base_url + bp).read()
        image_urls = re.findall("var imgList = (.*?);", html.decode('utf-8'))
        if image_urls:
            img_list = json.loads(image_urls[0])

            # get bike num and make folder
            num_regex = r"[0-9]{10}"
            num = re.search(num_regex, bp);
            bike_num = num.group(0)
            bike_folder = image_folder_path + "/" + city + "/" + bike_num
            if not os.path.isdir(bike_folder):
                os.makedirs(bike_folder)
                i = 0
                for img in img_list :
                    urlretrieve(img["url"], image_folder_path + "/" + city + "/" + bike_num + "/" + str(i) + ".jpg")
                    i = i + 1
        time.sleep(10)

# set up folders
if not os.path.isdir(image_folder_path):
    os.makedirs(image_folder_path)
    print("made folder for craigslist images")

cities = open('cities.txt', 'r')
for line in cities:
    print("scraping " + line[:-1] + "...", end="")
    sys.stdout.flush()
    scrape_bikes(line[:-1])
    print("done")
