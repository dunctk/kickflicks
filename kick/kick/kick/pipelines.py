# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
from scrapy.exceptions import DropItem

class KickPipeline(object):
    def process_item(self, item, spider):
        return item


class FundpercentPipeline(object):

	def process_item(self, item, spider):

		fund_percent_filter = float(4)

		if item["fundPercent"]:
			if (float(item["fundPercent"]) >= fund_percent_filter):
				return item
			else:
				raise DropItem("Funded percent too low")
		else:
			raise DropItem("Missing funded percent")


class VideoexistsPipeline(object):

	def process_item(self, item, spider):
		
		if "video" in item:
			return item
		else:
			raise DropItem("Missing video in %s" % item)


