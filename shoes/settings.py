from shutil import which

BOT_NAME = "shoes"

SPIDER_MODULES = ["shoes.spiders"]
NEWSPIDER_MODULE = "shoes.spiders"

# SELENIUM_DRIVER_NAME = 'chrome'
# SELENIUM_DRIVER_EXECUTABLE_PATH = which('C:/Users/User/Desktop/scrapy-re/shoes/')

SELENIUM_DRIVER_ARGUMENTS = \
    [
        '--headless=new', '--no-sandbox', '--disable-gpu', '--disable-dev-shm-usage',
        '--incognito', '--disable-extensions', '--disable-popup-blocking', '--disable-infobars',
    ]

DOWNLOADER_MIDDLEWARES = {
    'scrapy_selenium.SeleniumMiddleware': 800,
    'scrapy.downloadermiddlewares.retry.RetryMiddleware': 550,
}

DOWNLOAD_DELAY = 5  # Wait 5 seconds between requests
RANDOMIZE_DOWNLOAD_DELAY = True
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 3
AUTOTHROTTLE_MAX_DELAY = 10

ROTATING_PROXY_LIST = [
    "http://196.192.76.185:3128",
    "http://168.138.55.69:3128",
    "http://103.152.238.115:1080",
    "http://117.54.114.10:80",
    "http://157.66.16.52:8080",
]

ROBOTSTXT_OBEY = False

TWISTED_REACTOR = "twisted.internet.asyncioreactor.AsyncioSelectorReactor"
FEED_EXPORT_ENCODING = "utf-8"
