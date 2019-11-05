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

    def init_db(self):
        with self.conn.cursor(cursor=DictCursor) as c:
            c.execute('drop table if exists dushu_book')
            sql = '''
            create table dushu_book(id integer PRIMARY key auto_increment,
                                b_name varchar(50),
                                b_author varchar(30),
                                b_price FLOAT,
                                b_publisher varchar(50),
                                b_publish_date date,
                                b_isbn varchar(20),
                                b_detail_url varchar(50))
            '''
            c.execute(sql)

    def process_item(self, item, spider):
        with self.conn.cursor(cursor=DictCursor) as c:
            sql = "insert into dushu_book(%s) values(%s)"
            cols = ", ".join('`{}`'.format('b_' + k) for k in item.keys())
            val_cols = ', '.join('%({})s'.format(k) for k in item.keys())
            res_sql = sql % (cols, val_cols)

            c.execute(res_sql, args=item)


            self.conn.commit()
        return item

    def close_spider(self,spider):
        self.conn.cursor().close()
        self.conn.close()