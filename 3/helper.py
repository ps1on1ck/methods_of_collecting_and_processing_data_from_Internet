from bs4 import BeautifulSoup as bs
import requests
import re


def get_site_results(link, params):
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) '
                      'Chrome/92.0.4515.159 Safari/537.36 '
    }

    return requests.get(link, params=params, headers=headers)


def hh_vacancy_parser(item):
    vacancy_data = {}

    salary = item.find('span', {'data-qa': 'vacancy-serp__vacancy-compensation'})
    if not salary:
        salary_min = None
        salary_max = None
    else:
        salary = salary.getText().replace(u"\u202f", "")
        salary = re.split(r'\s|-', salary)

        if salary[0] == 'до':
            salary_min = None
            salary_max = int(salary[1])
        elif salary[0] == 'от':
            salary_min = int(salary[1])
            salary_max = None
        elif salary[1] == '–':
            salary_min = int(salary[0])
            salary_max = int(salary[2])
        else:
            salary_min = int(salary[0])
            salary_max = int(salary[1])

    href_link = item.find('a', {'data-qa': 'vacancy-serp__vacancy-title'})['href']
    href_link = re.split(r'\?', href_link)

    vacancy_data['title'] = item.find('span', {'class': 'resume-search-item__name'}).getText()
    vacancy_data['salary_min'] = salary_min
    vacancy_data['salary_max'] = salary_max
    vacancy_data['vacancy_id'] = href_link[0].replace('https://hh.ru/vacancy/', '')
    vacancy_data['vacancy_link'] = href_link[0]
    vacancy_data['site'] = 'https://hh.ru'
    return vacancy_data


def hh_parser(vacancy_text):
    params = {
        'text': vacancy_text,
        'page': ''
    }
    link = 'https://hh.ru/search/vacancy'
    res = get_site_results(link, params)
    vacancies = []

    if res.ok:
        last_page = 1
        parsed = bs(res.text, 'html.parser')
        pager = parsed.find('div', {'data-qa': 'pager-block'})

        if pager:
            last_page = int(pager.find_all('a', {'data-qa': 'pager-page'})[-1].getText())

        for page in range(0, last_page):
            params['page'] = page
            site_res = get_site_results(link, params)
            site_info = bs(site_res.text, 'html.parser')
            vacancy_items = site_info.find('div', {'data-qa': 'vacancy-serp__results'}) \
                .find_all('div', {'class': 'vacancy-serp-item'})

            for item in vacancy_items:
                data_item = hh_vacancy_parser(item)
                vacancies.append(data_item)

    return vacancies
