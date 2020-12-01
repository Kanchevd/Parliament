import scrapy
from scrapy.linkextractors import LinkExtractor
from scrapy.spiders import CrawlSpider, Rule
from parliament.items import MP
from scrapy.loader import ItemLoader
from scrapy.exceptions import CloseSpider

class MpSpider(CrawlSpider):
    name = 'mp'
    allowed_domains = ['parliament.bg']
    start_urls = ['http://parliament.bg/en/mp']
    
    rules = (
        Rule(LinkExtractor(restrict_text = 'Profile'), callback='parse'),
    )

    def parse(self, response):
        mp = ItemLoader(item=MP(), response=response)

        dob = pob = job = lang = pp = 'Not found' #defaults if none found
        

        #name always exists on valid page, no need for default
        name = response.xpath("//div[@class='MProwD']/descendant-or-self::*/text()").getall() #split into different tags

        if not name: #if it goes to a page but can't find a name, spider is sent to captcha, close
            raise CloseSpider('Closing spider, IP blocked')
        name = ' '.join(name) #join them to a string

        #list with all information on it
        mp_list = response.xpath("(//ul[@class='frontList'])[1]/li/text()").getall()

        #there is always an email as well
        email = response.xpath("(//ul[@class='frontList'])[1]/li[contains(text(), 'E-mail')]/a/text()").get()

        
        for entry in mp_list:
            if entry.startswith('Date of birth'):
                start = len('Date of birth : ') #start after this string
                size = len('04/08/1974') #size of string we want to get
                dob = entry[start:start+size+1]
                pob = entry[start+size+1:] #Place of birth is right after date of birth

            elif entry.startswith('Profession:'):
                start = len('Profession:')
                job = entry[start:-1] #remove ';' at the end

            elif entry.startswith('Languages:'):
                start = len('Languages:')
                lang = entry[start:-1] #remove ';' at the end

            elif entry.startswith('Political force:'):
                start = len('Political force:')
                percent = len('23.74%;') #size of string we want gone from the end
                pp = entry[16:-percent]

        #Load everything into the item
        mp.add_value('name', name)
        mp.add_value('dob', dob)
        mp.add_value('pob', pob)
        mp.add_value('job', job)
        mp.add_value('lang', lang)
        mp.add_value('pp', pp)
        mp.add_value('email', email)

        return mp.load_item()