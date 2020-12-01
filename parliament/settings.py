BOT_NAME = 'parliament'

SPIDER_MODULES = ['parliament.spiders']
NEWSPIDER_MODULE = 'parliament.spiders'

# Obey robots.txt rules
ROBOTSTXT_OBEY = True
DOWNLOAD_DELAY = 10 #to prevent ban

LOG_LEVEL = 'WARNING'

ITEM_PIPELINES = {
    'parliament.pipelines.UnwrapPipeline': 100,
    'parliament.pipelines.ParsePipeline': 200,
    'parliament.pipelines.PrintPipeline': 800,
    'parliament.pipelines.DatabasePipeline': 900,
}

DOWNLOADER_MIDDLEWARES = {
    'rotating_proxies.middlewares.RotatingProxyMiddleware': 610,
    'rotating_proxies.middlewares.BanDetectionMiddleware': 620,
}

ROTATING_PROXY_LIST = [
    '163.172.47.182:3128',
    '163.172.47.182:3128',
]

COOKIES_ENABLED = False