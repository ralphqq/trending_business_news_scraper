# -*- coding: utf-8 -*-
# Google Trends (Business Stories) Spider

import datetime
import logging
import time

import scrapy
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import StaleElementReferenceException

from gtrends_scraper.items import GtrendsScraperItem, GtrendsItemLoader

STORY_XPATH = "//a[contains(@class, 'trending-story')]"
ARTICLE_XPATH = "//a[contains(@class, 'article-item')]"
TITLE_XPATH = ".//div[contains(@class, 'article-title')]"
MEDIA_XPATH = ".//div[starts-with(@class, 'article-media')]"
TIME_XPATH = ".//div[starts-with(@class, 'ng-binding')]"

INITIAL_WAIT = 15       # The Internet here is so painfully SLOW
INTERIM_WAIT = 3


class GoogleTrendsSpider(scrapy.Spider):
    name = 'gtrends'
    start_urls = ['https://www.google.com/trends/home/b/PH']
    
    def __init__(self):
        scrapy.Spider.__init__(self)
        self.driver = webdriver.PhantomJS()
        self.verificationErrors = []
    
    
    def __del__(self):
        self.driver.quit()
        print self.verificationErrors
        scrapy.Spider.__del__(self)
    
    
    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(INITIAL_WAIT)
        self.wait_for_js(By.XPATH, STORY_XPATH)
        
        for sel in self.driver.find_elements_by_xpath(STORY_XPATH):
            url = response.urljoin(sel.get_attribute('href'))
            request = scrapy.Request(url, callback=self.parse_story_page)
            request.meta['trending-story'] = sel.text
            
            yield request
    
    
    def parse_story_page(self, response):
        self.driver.get(response.url)
        time.sleep(INTERIM_WAIT)
        self.wait_for_js(By.XPATH, ARTICLE_XPATH)   # Just making sure
        
        story = response.meta['trending-story']
        t = datetime.datetime.now().strftime('%Y-%m-%d %H:%M:%S')
        
        for elem in self.driver.find_elements_by_xpath(ARTICLE_XPATH):
        
            try:
                title = elem.find_element_by_xpath(TITLE_XPATH).text
                publisher = elem.find_element_by_xpath(MEDIA_XPATH).text
                since_pub = elem.find_element_by_xpath(TIME_XPATH).text
                
                l = GtrendsItemLoader(GtrendsScraperItem())
                l.add_value('time_scraped', t)
                l.add_value('story', story)
                l.add_value('link', elem.get_attribute('href'))
                l.add_value('title', title)
                l.add_value('publisher', publisher)
                l.add_value('since_published', since_pub)
                
                yield l.load_item()
            
            except StaleElementReferenceException as e:
                logging.getLogger(__name__).warning(e)
                
            except Exception as err:
                logging.getLogger(__name__).error(err)
    
    
    def wait_for_js(self, find_by, expression,
                    wait_time=10, parent=None):
        base = self.driver if parent is None else parent
        
        return WebDriverWait(base, wait_time).until(
            EC.presence_of_element_located((find_by, expression)))
