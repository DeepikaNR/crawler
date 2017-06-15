# -*- coding: utf-8 -*-
from __future__ import absolute_import
import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from bs4 import BeautifulSoup

from ..items import Learner1Item


class JedaSpider(CrawlSpider):

    name = "jeda"

    allowed_domains = []
    start_urls = [

        "https://en.wikipedia.org/wiki/Yash_(actor)",

        ]
    # This spider has one rule: extract all (unique and canonicalized) links,
    # follow them and parse them using the parse_items method
    rules = [
        Rule(
            LinkExtractor(
                canonicalize=True,
                unique=True

            ),
            follow=True,
            callback="parse_items"
        )
    ]

    def start_requests(self):
        for url in self.start_urls:
            yield scrapy.Request(url, callback=self.parse_items)

    def parse_items(self, response):    # htmlresponse? extract kannada?

        # Extract only kan or english web pages
        html_lang = response.xpath('//html/@lang').extract_first()
        # Caveat: TODO : a subsection can have info in other lang.
        # Then the lang attribute will be set around that content. This is not taken care here
        if html_lang is None or html_lang.startswith('en') or html_lang == 'kn':

            self.logger.info(
            'Jeda: success crawling -> {}'.format(response.url))
            content = self._get_plain_content(response.body)

            # Populating the item
            item = Learner1Item()
            item['url'] = response.url
            item['content'] = content
            item['language'] = html_lang
            yield item

            for link in LinkExtractor().extract_links(response):
                yield scrapy.Request(link.url, callback=self.parse_items)
        else:
            self.logger.debug("jeda: skipped extracting {}".format(response.url))

    def _get_plain_content(self, html):
        soup = BeautifulSoup(html)
        # kill all script and style elements
        for script in soup(["script", "style"]):
            script.extract()  # rip it out

        # get text
        text = soup.get_text()

        # break into lines and remove leading and trailing space on each
        lines = (line.strip() for line in text.splitlines())
        # break multi-headlines into a line each
        chunks = (phrase.strip() for line in lines for phrase in
                  line.split("  "))
        # drop blank lines
        text = '\n'.join(chunk for chunk in chunks if chunk)
        return text

"""
    def error_handler(self, failure):
        # log all failures
        self.logger.error(repr(failure))

for href in response.css("ul.directory.dir-col > li > a::attr('href')"):
            url = response.urljoin(href.extract())
            yield scrapy.Request(url, callback=self.parse_dir_contents)

https://en.wikipedia.org/wiki/Karnataka

"https://en.wikipedia.org/wiki/Ayurveda",
        "https://en.wikipedia.org/wiki/List_of_engineering_colleges_affiliated_to_Visvesvaraya_Technological_University",
        "http://swayampaaka.com/",
        "http://www.webindia123.com/personal/person.htm"

"""