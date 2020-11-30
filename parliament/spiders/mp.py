import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from parliament.items import MP
from scrapy.loader import ItemLoader

class MpSpider(CrawlSpider):
    name = 'mp'
    allowed_domains = ['parliament.bg']
    start_urls = ['http://parliament.bg/en/mp']
    
    rules = (
        Rule(LinkExtractor(restrict_text = 'Profile'), callback='parse'),
    )

    def parse(self, response):
        mp = ItemLoader(item=MP(), response=response)
        print(response.url)
        name = response.xpath("//div[@class='MProwD']/descendant-or-self::*/text()").getall()
        name = ' '.join(name)
        mp_list = response.xpath("(//ul[@class='frontList'])[1]/li/text()").getall()
        email = response.xpath("(//ul[@class='frontList'])[1]/li[contains(text(), 'E-mail')]/a/text()").get()

        #defaults if none found
        dob = pob = job = lang = pp = 'Not found'
        for entry in mp_list:
            if entry.startswith('Date of birth'):
                dob = entry[16:27]
                pob = entry[27:]
            elif entry.startswith('Profession:'):
                job = entry[11:-1]
            elif entry.startswith('Languages:'):
                lang = entry[10:-1]
            elif entry.startswith('Political force: '):
                pp = entry[16:-7]

        mp.add_value('name', name)
        mp.add_value('dob', dob)
        mp.add_value('pob', pob)
        mp.add_value('job', job)
        mp.add_value('lang', lang)
        mp.add_value('pp', pp)
        mp.add_value('email', email)

        return mp.load_item()