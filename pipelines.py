# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import logging

class Learner1Pipeline(object):

        def __init__(self):
            self.file_prefix = 900
            self.file_extension = ".txt"
            self.file_path = "/harvest/"

        def _get_filename(self, item):
            file_name = self.file_path
            if item['language'] == 'kn':
                file_name += 'kannada/'
            else:
                file_name += 'english/'
            file_name += str(self.file_prefix) + self.file_extension

            self.file_prefix += 1
            return file_name

        def process_item(self, item, spider):
            logger = logging.getLogger()

            file_name = self._get_filename(item)

            logger.info("Writing to file: " + file_name)
            with open(file_name, "w") as f:
                f.write(item['url'])
                f.write("\n")
                f.write(item['content'].encode('utf8'))

            return item
