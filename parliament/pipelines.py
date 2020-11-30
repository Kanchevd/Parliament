# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
import sqlite3

class UnwrapPipeline:
    def process_item(self, item, spider):
        #ItemLoader gets all items as lists; set the property to the first value to remove them from the lists

        item['name'] = item.get('name')[0].strip()
        item['dob'] = item.get('dob')[0].strip()
        item['pob'] = item.get('pob')[0].strip()
        item['job'] = item.get('job')[0].strip()
        item['lang'] = item.get('lang')[0].strip()
        item['pp'] = item.get('pp')[0].strip()
        item['email'] = item.get('email')[0].strip()

        return item

class PrintPipeline:
    def process_item(self, item, spider):
        #Prints all items; For testing purposes
        print(item.get('name'))
        print(item.get('dob'))
        print(item.get('pob'))
        print(item.get('job'))
        print(item.get('lang'))
        print(item.get('pp'))
        print(item.get('email'))
       
        return item

class ParsePipeline:
    def process_item(self, item, spider):
        item['dob'] = item.get('dob').replace('/','')

        return item

class DatabasePipeline:

    #Database setup
    conn = sqlite3.connect('parliament.db')
    c = conn.cursor()

    def open_spider(self, spider):
        self.c.execute(""" CREATE TABLE IF NOT EXISTS mps (name text, dob text, pob real, job integer, lang text, pp integer, email text) """)

    def process_item(self, item, spider):
        #Insert values
        self.c.execute("INSERT INTO mps (name,dob,pob,job,lang,pp,email) VALUES (?,?,?,?,?,?,?)",(item.get('name'),item.get('dob'),item.get('pob'), item.get('job'), item.get('lang'), item.get('pp'),item.get('email')))
        self.conn.commit()
        return item

    def close_spider(self, spider):
        #Save and close database
        self.conn.close()