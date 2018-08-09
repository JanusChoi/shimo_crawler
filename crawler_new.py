### Code refer : http://edmundmartin.com/selenium-based-crawler-in-python/
import time
import logging
import csv
from selenium import webdriver
from urllib.parse import urldefrag, urljoin
from collections import deque
from bs4 import BeautifulSoup
import base64

def encode(key, clear):
    enc = []
    for i in range(len(clear)):
        key_c = key[i % len(key)]
        enc_c = chr((ord(clear[i]) + ord(key_c)) % 256)
        enc.append(enc_c)
    return base64.urlsafe_b64encode("".join(enc).encode()).decode()

def decode(key, enc):
    dec = []
    enc = base64.urlsafe_b64decode(enc).decode()
    for i in range(len(enc)):
        key_c = key[i % len(key)]
        dec_c = chr((256 + ord(enc[i]) - ord(key_c)) % 256)
        dec.append(dec_c)
    return "".join(dec)

def read_config(config_file):
    pars={}
    exclude_link=[]
    with open(config_file, "r", encoding='utf-8') as pf:
        for str in pf:
            if str == '\n':
                continue
            if ":" in str:
                key = str.split(":",1)[0]
                value = str.split(":",1)[1]
                pars[key]=value.rstrip('\n')
            else:
                exclude_link.append(str.rstrip('\n'))
    pf.close()
    return pars, exclude_link

class SeleniumCrawler(object):

    def __init__(self, driver_type, base_url, exclusion_list, output_file='example.txt', config_file='config.ini', start_url=None):

        assert isinstance(exclusion_list, list), 'Exclusion list - needs to be a list'

        #self.browser = webdriver.Chrome('E:\Webdrivers\chromedriver')  #Add path to your Chromedriver
        #self.browser = webdriver.Firefox('E:\Webdrivers')  #Add path to your webdriver
        if driver_type == '1':
            #self.browser = webdriver.Chrome('E:\Webdrivers\chromedriver')
            self.browser = webdriver.Chrome()
        elif driver_type == '2':
            self.browser = webdriver.Firefox()
        else:
            self.browser = None

        self.base = base_url

        self.start = start_url if start_url else base_url  #If no start URL is passed use the base_url

        self.exclusions = exclusion_list  #List of URL patterns we want to exclude

        self.crawled_urls = []  #List to keep track of URLs we have already visited

        self.url_queue = deque([self.start])  #Add the start URL to our list of URLs to crawl

        self.output_file = output_file

        self.config_file = config_file

    def log_in(self, login_url, name, passwd):
        self.browser.get(login_url)
        time.sleep(5)
        email = self.browser.find_element_by_name('email')
        email.send_keys(name)
        password = self.browser.find_element_by_name('password')
        password.send_keys(passwd)
        self.browser.find_element_by_id('bd-login-submit').click()
        time.sleep(5)




    def get_page(self, url): ## not used in this script
        self.browser.get(url)
        time.sleep(5)
        return self.browser.page_source

    def get_soup(self, html): ## get html into soup
        if html is not None:
            soup = BeautifulSoup(html, 'lxml')
            return soup
        else:
            return


    def get_data(self, soup): ## write info into list

        file_idx_L1 = []

        flink = self.base + soup['href']
        raw_name = soup.find("div", class_="file-name")
        if raw_name is not None:
            fname = raw_name.get_text()
            file_idx_L1.append([[fname],[flink]])
            #debug# print(f"get_data: Writing: {fname} {flink}")
        return file_idx_L1

    def csv_output(self, url, title): ## write list into csv file

        with open(self.output_file, 'a', encoding='utf-8') as outputfile:

            writer = csv.writer(outputfile)
            writer.writerow([url, title])

    def txt_output(self, out_list, n): ## write list into txt file

        fh = open(self.output_file, "a", encoding='utf-8')
        for i in range(0,len(out_list)):
            fh.write(n * "    " + f"{out_list[i][0][0]} {out_list[i][1][0]}\n")

        fh.close()

    def get_links(self, soup, n):

        result_L1 = []
        #debug# print("get_links: inside now")
        for raw_link in soup.find_all('a', href=True): #All links which have a href element
            link = raw_link['href'] #The actually href element of the link
            #debug# print(f"get_links: link is {link}")
            result_L1 = self.get_data(raw_link)
            self.txt_output(result_L1, n)
            if result_L1 == []: #Skip link with no contents
                continue
            if any(e in link for e in self.exclusions): #Check if the link matches our exclusion list
                #debug# print(f"get_links: skipping exclusions {link}")
                continue #If it does we do not proceed with the link
            if 'folder' not in link: #Skip opening documents
                #debug# print(f"get_links: skipping not folder {link}")
                continue
            url = urljoin(self.base, urldefrag(link)[0]) #Resolve relative links using base and urldefrag
            #debug# print(f"get_links: url(0) is {url}")
            if url not in self.url_queue and url not in self.crawled_urls: #Check if link is in queue or already crawled
                if url.startswith(self.base): #If the URL belongs to the same domain
                    self.url_queue.append(url) #Add the URL to our queue
                    #debug# print(f"get_links: url is {url}")
                    #debug# print(f"get_links: url queue is {self.url_queue}")
                    html = self.get_page(url)
                    soup = self.get_soup(html)
                    self.get_links(soup, n+1)

    def run_crawler(self):
        #while len(self.url_queue): #If we have URLs to crawl - we crawl
            #debug# print(f"run_crawler: url queue is {self.url_queue}")

            current_url = self.url_queue.popleft() #We grab a URL from the left of the list
            self.crawled_urls.append(current_url) #We then add this URL to our crawled list

            #debug# print(f"run_crawler: url is {current_url}")

            self.browser.get(current_url)
            time.sleep(5)
            html = self.browser.page_source

            if self.browser.current_url != current_url: #If the end URL is different from requested URL - add URL to crawled list
                self.crawled_urls.append(current_url)
            soup = self.get_soup(html)

            if soup is not None:  #If we have soup - parse and write to our csv file
                #debug# print("run_crawler: start get_links")
                self.get_links(soup, 0)
                #debug# print(f"run_crawler: url queue is {self.url_queue}")
