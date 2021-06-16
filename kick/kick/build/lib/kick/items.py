import scrapy

class KickstarterItem(scrapy.Item):
	name = scrapy.Field()
	shortDesc = scrapy.Field()
	image = scrapy.Field()
	video = scrapy.Field()
	fundGoal = scrapy.Field()
	fundReached = scrapy.Field()
	fundPercent = scrapy.Field()
	backersCount = scrapy.Field()
	creatorName = scrapy.Field()
	creatorProfileUrl = scrapy.Field()
	creatorProfileImage = scrapy.Field()
	launchDate = scrapy.Field()
	category = scrapy.Field()
	subcategory = scrapy.Field()
	pageUrl = scrapy.Field()
	timestamp = scrapy.Field()