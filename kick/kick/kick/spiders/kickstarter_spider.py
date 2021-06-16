import scrapy
import urlparse
import re
from kick.items import KickstarterItem

class KickstarterSpider(scrapy.Spider):
	name = "kickstarter"
	allowed_domains = ["kickstarter.com"]

	def start_requests(self):
		for i in xrange(1, 200):	
			yield self.make_requests_from_url("https://www.kickstarter.com/discover/categories/design?sort=most_funded&page=%d" % i)
			yield self.make_requests_from_url("https://www.kickstarter.com/discover/categories/technology?sort=most_funded&page=%d" % i)

	def parse(self, response):
		for href in response.xpath("//div[@class='project-thumbnail']/a/@href"):
			url = response.urljoin(href.extract())
			url = urlparse.urljoin(url, urlparse.urlparse(url).path)
			url = url + '/description'
			yield scrapy.Request(url, callback=self.parse_description_page)


	def parse_description_page(self, response):
		item = KickstarterItem()

		item["pageUrl"] = response.url		

		if (response.xpath("//data[@itemprop='Project[pledged]']/@data-value").extract()):
			item["fundGoal"] = response.xpath("//div[@id='pledged']/@data-goal").extract()[0]
			item["fundReached"] = response.xpath("//div[@id='pledged']/@data-pledged").extract()[0]
			fundPercent = response.xpath("//div[@id='pledged']/@data-percent-raised").extract()[0]
			item["fundPercent"] = float(fundPercent)
		else:
			fundGoalString = response.xpath("(//div[@class='NS_projects__description_section']//span[@class='money usd no-code']/text())[2]").extract()[0]
			item["fundGoal"] = float(re.sub('\$|,','',fundGoalString))
			fundReachedString = response.xpath("(//div[@class='NS_projects__description_section']//span[@class='money usd no-code']/text())[1]").extract()[0]
			item["fundReached"] = float(re.sub('\$|,','',fundReachedString))
			item["fundPercent"] = ( item["fundReached"] / item["fundGoal"] )



		if (response.xpath("(//section[@class='NS_projects__hero_funding']//div[@class='NS_projects__header center']/h2)[1]/a/text()")):
			item["name"] = response.xpath("(//section[@class='NS_projects__hero_funding']//div[@class='NS_projects__header center']/h2)[1]/a/text()").extract()[0]
		else:
			item["name"] = response.xpath("//div[@class='project-profile__content']/div[@class='NS_project_profile__title']/h2[@class='project-profile__title editable-field']/span[@class='relative']/a[@class='hero__link']/text()").extract()[0]
		
		if (response.xpath("//section[@class='NS_projects__hero_funding']/div[@class='container-flex px2']/div[@class='row'][2]/div[@class='col col-8 py4']/div[@class='mobile-hide']/p[@class='h3 mb3']/text()")):
			shortDesc = response.xpath("//section[@class='NS_projects__hero_funding']/div[@class='container-flex px2']/div[@class='row'][2]/div[@class='col col-8 py4']/div[@class='mobile-hide']/p[@class='h3 mb3']/text()").extract()[0]
		else:
			shortDesc = response.xpath("//div[@class='project-profile__text_container col-4']/div[@class='NS_project_profiles__blurb']/div[@class='project-profile__blurb editable-field']/span[@class='relative']/span[@class='content edit-profile-blurb js-edit-profile-blurb']/text()").extract()[0]
		item["shortDesc"] = shortDesc.strip()
		
		if (response.xpath("//div[@id='video_pitch']/@data-video-url")):
			item["video"] = response.xpath("//div[@id='video_pitch']/@data-video-url").extract()[0]
			image = response.xpath("//div[contains(@class,'video-player')]/@data-video").extract()[0]
			image = re.search('(?<=frame":")[^"]*', image)
			item["image"] = image.group(0)

		subcategory = response.xpath("(//div[@class='NS_projects__category_location']/a[@class='grey-dark mr3 nowrap'][2])[1]/text()").extract()[0]
		subcategory = subcategory.strip()
		item["subcategory"] = subcategory

		categoryUrl = response.xpath("(//div[@class='NS_projects__category_location']/a[@class='grey-dark mr3 nowrap'][2])[1]/@href").extract()[0]
		categoryUrl = re.sub('\/[a-z]+\/[a-z]+\/', '', categoryUrl)
		item["category"] = re.sub('\/.*', '', categoryUrl)

		if (response.xpath("//data[@itemprop='Project[backers_count]']/@data-value")):
			backersCount = response.xpath("//data[@itemprop='Project[backers_count]']/@data-value").extract()[0]
			item["backersCount"] = int(backersCount)
		else:
			backersCount = response.xpath("//div[@class='project-profile__text_container col-4']/div[@class='NS_projects__spotlight_stats']/b/text()").extract()
			backersCount[0] = re.sub('backers', '' ,backersCount[0])
			backersCount[0] = re.sub(',', '', backersCount[0])
			item["backersCount"] = int(backersCount[0])

		if (response.xpath("(//a[@data-modal-class='modal_project_by'])[1]/text()")):
			creatorName = response.xpath("(//a[@data-modal-class='modal_project_by'])[1]/text()").extract()[0]
			creatorProfileUrl = response.xpath("(//a[@data-modal-class='modal_project_by'])[1]/@href").extract()[0]
		else:
			creatorName = response.xpath("//div[@class='creator-name']/div[@class='mobile-hide']/a[@class='hero__link remote_modal_dialog js-update-text-color']/text()").extract()[0]
			creatorProfileUrl = response.xpath("//a[@class='hero__link remote_modal_dialog js-update-text-color']/@href").extract()[0]
		item["creatorName"] = creatorName.strip()
		creatorProfileUrl = urlparse.urljoin(response.url, creatorProfileUrl[0].strip())
		item["creatorProfileUrl"] = creatorProfileUrl
		
		item["creatorProfileImage"] = response.xpath("(//img[@class='avatar-small circle'])[1]/@src").extract()[0]
		
		updatesUrl = re.sub('\/description', '/updates', response.url)
		request = scrapy.Request(updatesUrl, callback=self.parse_updates_page)
		request.meta["item"] = item ## passing item in the meta dictionary

		yield request
		

	def parse_updates_page(self, response):
		item = response.meta["item"]
		item["launchDate"] = response.xpath("//div[contains(@class,'launched')]//@datetime").extract()[0]

		return item



