# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: https://docs.scrapy.org/en/latest/topics/item-pipeline.html


# useful for handling different item types with a single interface
from itemadapter import ItemAdapter
from pymongo import MongoClient
import re

class JobparserPipeline:
    def __init__(self):
        client = MongoClient('localhost', 27017)
        self.mongobase = client.vacancies_spider

    def process_item(self, item, spider):
        item['salary_min'], item['salary_max'], item['salary_cur'] = self.process_salary(item['salary'])
        item['domain'] = spider.allowed_domains[0]
        del item['salary']
        collection = self.mongobase[spider.name]
        collection.insert_one(item)
        return item

    def process_salary(self, salary):
        if not salary or salary == 'з/п не указана' or salary == 'По договорённости':
            salary_min = None
            salary_max = None
            salary_cur = None
        else:
            salary = salary.replace(u"\xa0", "").replace("руб.", "").replace("  ", " ")
            salary = re.split(r'\s|-', salary)

            if salary[0] == 'до':
                salary_min = None
                salary_max = int(salary[1])
                salary_cur = int(salary[1])
            elif len(salary) > 2 and salary[2] == 'до':
                salary_min = int(salary[1])
                salary_max = int(salary[3])
                salary_cur = int(salary[3])
            elif salary[0] == 'от':
                salary_min = int(salary[1])
                salary_cur = int(salary[1])
                salary_max = None
            elif salary[1] == '–' or salary[1] == "—":
                salary_min = int(salary[0])
                salary_max = int(salary[2])
                salary_cur = int(salary[2])
            else:
                salary_min = int(salary[0])
                if salary[1] != '':
                    salary_max = int(salary[1])
                    salary_cur = int(salary[1])
                else:
                    salary_max = None
                    salary_cur = None

        return salary_min, salary_max, salary_cur
