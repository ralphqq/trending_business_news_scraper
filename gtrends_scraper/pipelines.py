# -*- coding: utf-8 -*-

import logging
import sqlite3


class GtrendsScraperPipeline(object):
    def process_item(self, item, spider):
        return item


class SQLiteItemPipeline(object):
    filename = 'scraped_data.db'

    def __init__(self):
        self.db = None
        self.cursor = None
    
    
    def open_spider(self, spider):
        self.db = sqlite3.connect(self.filename)
        self.cursor = self.db.cursor()
        self._create_table()
    
    
    def close_spider(self, spider):
        self.db.close()
    
    
    def process_item(self, item, spider):
        
        if self._is_duplicate(item):
            pass
        
        else:
            
            try:
                self.cursor.execute(
                    """
                    INSERT INTO trending_articles(
                        time_scraped, title, publisher,
                        story, since_published, link
                    )
                    VALUES(?, ?, ?, ?, ?, ?)
                    """, 
                    (item['time_scraped'], item['title'],
                     item['publisher'], item['story'],
                     item['since_published'], item['link'])
                )
                self.db.commit()
            
            except Exception as err:
                logging.getLogger(__name__).error(err)
        
        return item
    
    
    def _create_table(self):
        self.cursor.execute(
            """
            CREATE TABLE IF NOT EXISTS trending_articles(
                id INTEGER PRIMARY KEY, time_scraped TEXT, title TEXT,
                publisher TEXT, since_published TEXT, story TEXT,
                link TEXT, status TEXT DEFAULT 'active'
            )
            """
        )
        self.db.commit()
    
    
    def _is_duplicate(self, item):
        self.cursor.execute("""SELECT link FROM trending_articles
                               WHERE link = ?""", (item['link'], ))
        
        return True if self.cursor.fetchone() else False
