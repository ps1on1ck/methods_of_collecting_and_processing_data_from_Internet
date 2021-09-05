import scrapy
from scrapy.http import HtmlResponse
from jobparser.items import JobparserItem


class SuperjobSpider(scrapy.Spider):
    name = 'superjob'
    allowed_domains = ['superjob.ru']
    start_urls = ['https://www.superjob.ru/vacancy/search/?keywords=Python&noGeo=1']

    def parse(self, response: HtmlResponse):
        urls = response.xpath("//a[contains(@class,'icMQ_ _6AfZ9')]/@href").getall()
        next_page = response.xpath("//a[contains(@class,'f-test-link-Dalshe')]/@href").get()
        if next_page:
            yield response.follow(next_page, callback=self.parse)
        for url in urls:
            yield response.follow(url, callback=self.vacancy_parse)

    def vacancy_parse(self, response: HtmlResponse):
        vac_name = response.xpath("//h1/text()").get()
        vac_salary_pred = response.css("span[class='_1h3Zg _2Wp8I _2rfUm _2hCDz'] ::text").getall()
        vac_salary = ' '.join(vac_salary_pred)
        vac_url = response.url
        item = JobparserItem(name=vac_name, salary=vac_salary, url=vac_url)
        yield item