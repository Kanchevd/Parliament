import scrapy


class MP(scrapy.Item):
    name = scrapy.Field() 
    dob = scrapy.Field() #Date of Birth
    pob = scrapy.Field() #Place of Birth
    job = scrapy.Field() #Profession
    lang = scrapy.Field() #All spoken languages
    pp = scrapy.Field() #Political Party
    email = scrapy.Field() 