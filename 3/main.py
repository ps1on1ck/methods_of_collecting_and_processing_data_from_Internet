from m_client import MClient
from pprint import pprint
import json
from helper import hh_parser

mClient = MClient('127.0.0.1', 27017, 'vacancies', 'hh')
vacancy = 'Python'
hh_data = hh_parser(vacancy)

if len(hh_data) < 1:
    with open('hh_data_new.json', 'r', encoding='utf-8') as a:
        hh_data = json.load(a)


result_insert_many = mClient.insert_many(hh_data)
pprint(result_insert_many)

mClient.find_and_print_by_salary(250000)

new_items = [
    {
        'salary_max': 450001,
        'salary_min': 300001,
        'site': 'https://hh.ru',
        'title': 'Senior Python developer',
        'vacancy_id': '471',
        'vacancy_link': 'https://hh.ru/vacancy/471'
    }, {
        'salary_max': 450000,
        'salary_min': 300000,
        'site': 'https://hh.ru',
        'title': 'Senior Python/Flask developer',
        'vacancy_id': '47188144',
        'vacancy_link': 'https://hh.ru/vacancy/47188144'
    }
]
mClient.insert_many_if_not_exist(new_items)
