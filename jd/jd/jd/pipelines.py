# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://doc.scrapy.org/en/latest/topics/item-pipeline.html
import csv
import pymysql

class JdPipeline(object):
    def __init__(self):
        self.file = open('data.csv', 'w', encoding='utf-8')
        self.conf = {
                'host': 'localhost',
                'user': 'root',
                'password': 'root',
                'db': 'jd',
                'port': 3306,
                'charset' : "utf8"
            }
        self.conn = pymysql.connect(**self.conf)
        self.row=0

    def process_item(self, item, spider):
        if self.row==0:
            self.file.write(','.join(item.keys())+'\n')
        self.file.write(','.join(item.values()))
        self.file.write("\n")

        cur = self.conn.cursor()
        sql_insert = 'insert into commodity(category, name, price, remark_count, descript, merchant, second_hand) values("{category}", "{name}", {price}, "{remark_count}+", "{descript}", "{merchant}", "{second_hand}")'.format(
            category = item['category'],
            name = item['name'],
            price = item['price'],
            remark_count = item['remark_count'],
            descript = item['descript'],
            merchant = item['merchant'],
            second_hand = item['second_hand']
        )
        try:
            cur.execute(sql_insert)
            self.conn.commit()     # 提交
        except Exception as e:
            # 错误回滚
            print("存储失败: ", sql_insert)
            self.conn.rollback()

        self.row+=1
        return item

    def close_spider(self, spider):
        self.file.close()
        self.conn.close()
        print("sum %d data" % self.row)

