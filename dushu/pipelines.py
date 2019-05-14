# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymysql
from pymysql.cursors import DictCursor

from dushu import settings


class DushuPipeline(object):
    def __init__(self):
        # **dict 将字典转成关键参数传值的格式，如key = value
        self.conn = pymysql.Connect(**settings.DB_CONFIG)
        self.init_db()
        self.batch_count = 0

    def init_db(self):
        with self.conn.cursor(cursor=DictCursor) as c:
            c.execute('drop table if exists dushu_book')
            sql = '''
            create table dushu_book(id integer PRIMARY key auto_increment,
                                name varchar(200),
                                author varchar(50),
                                price FLOAT,
                                publisher varchar(200),
                                publish_date DATE,
                                isbn varchar(30),
                                detail_url varchar(100))
            '''
            c.execute(sql)

    def process_item(self, item, spider):
        with self.conn.cursor(cursor=DictCursor) as c:
            sql = 'insert into dushu_book(name,author,price,publisher,publish_date,isbn,detail_url) values(%(name)s,%(author)s,%(price)s,%(publisher)s,%(publish_date)s,%(isbn)s,%(detail_url)s)'
            c.execute(sql,args=item)
        self.batch_count+=1
        if self.batch_count%100 == 0:
            self.conn.commit()
        return item
