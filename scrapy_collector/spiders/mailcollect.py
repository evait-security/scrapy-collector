import re, sys

import scrapy


class MailcollectSpider(scrapy.Spider):
    """Tries to collect email addresses from a given domain

    Will follow internal links, including subdomains.
    Does not filter collected mail addresses from other domains,
    all found addresses are included in the results.

    Optionally outputs the followed URLs."""

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
        "LOG_LEVEL": "WARN",
        "ROBOTSTXT_OBEY": False,
        "USER_AGENT": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/42.0.2311.135 Safari/537.36 Edge/12.246",
    }

    emails = []  # to remember the mail adresse we've already yielded
    show_paths = "false"  # command line flag

    def start_requests(self):
        try:
            url = f"https://{getattr(self, 'target')}"
        except AttributeError:
            print(
                f'\n\nNo target given.\nRecommended usage: scrapy runspider {__file__} -O outfile.json -a target="example.com" -a [show-paths=true]\n\nExiting...\n'
            )
            return

        try:
            self.show_paths = getattr(self, "show-paths")
        except AttributeError:
            pass

        yield scrapy.Request(url=url, callback=self.parse)

    def parse(self, response):
        # if we don't see an HTML body, leave
        try:
            response.css("body").get()
        except scrapy.exceptions.NotSupported:
            return

        print(f"Crawling {response.url} ...")

        # include visited paths in output file?
        if self.show_paths == "true":
            yield {
                "type": "visited",
                "href": response.url,
            }

        # regex taken from https://emailregex.com/
        # will NOT find things like abc (at) xyz.com etc,
        # only clean mail addresses
        mails = re.findall(
            r"([a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+)",
            response.css("body").get(),
        )

        # process captured mail addresses
        for mail in mails:
            if mail not in self.emails:
                self.emails.append(mail)
                yield {
                    "type": "email",
                    "address": mail,
                }

        # follow links
        page_links = response.css("a")

        for link in page_links:
            href = link.css("a::attr(href)").get()
            if not href:
                continue

            target = getattr(self, "target")
            # only follow internal links
            if target in href or href.startswith("/"):
                try:
                    yield response.follow(link, self.parse)
                except ValueError:
                    # we found a non-http(s) link
                    continue
