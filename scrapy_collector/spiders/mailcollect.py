import re

import scrapy

### TODO: this is currently hardcoded to only work for vereinigte-hagel.net
### next step is to generalize it to work for any domain


class MailcollectSpider(scrapy.Spider):
    name = "mailcollect"
    allowed_domains = []

    custom_settings = {
        "CONCURRENT_REQUESTS": 2,
        "CONCURRENT_REQUESTS_PER_DOMAIN": 2,
        "DEPTH_LIMIT": 2,
        "DEPTH_STATS_VERBOSE": True,
        "DOWNLOAD_DELAY": 2,
        "DOWNLOAD_MAXSIZE": 33554432,  # 32 MB
        "DOWNLOAD_WARNSIZE": 8388608,  # 8 MB
        "LOG_LEVEL": "INFO",
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    }

    paths = []
    emails = []

    def start_requests(self):
        urls = [
            "https://www.vereinigte-hagel.net/",
        ]
        for url in urls:
            yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        mails = re.findall(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
            response.css("body").get(),
        )

        for mail in mails:
            if mail not in self.emails:
                self.emails.append(mail)
                yield {
                    "type": "email",
                    "address": mail,
                }

        page_links = response.css("a")

        for anchor in page_links:
            href = anchor.css("a::attr(href)").get()
            if "vereinigte-hagel.net" in href:
                if href not in self.paths:
                    self.paths.append(href)
                    yield {
                        "type": "path",
                        "href": href,
                        "text": anchor.css("a::text").get(),
                    }
                yield response.follow(anchor, self.parse)
