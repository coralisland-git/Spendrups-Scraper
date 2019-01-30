# from __future__ import unicode_literals
import scrapy

import json

import os

import scrapy

from scrapy.spiders import Spider

from scrapy.http import FormRequest

from scrapy.http import Request

from chainxy.items import ChainItem

from scrapy import signals

from scrapy.xlib.pydispatch import dispatcher

from selenium import webdriver

from lxml import etree

from lxml import html

import time

import pdb


class Spendrups(scrapy.Spider):

	name = 'spendrups'

	domain = 'https://www.spendrups.se'

	history = []

	output = []

	def __init__(self):

		pass
	
	def start_requests(self):

		url = "https://www.spendrups.se/api/products?grid=small&sortfield=name"

		yield scrapy.Request(url, callback=self.parse) 

	def parse(self, response):

		product_list = json.loads(response.body)['items']

		for product in product_list:

			item = ChainItem()

			item['Alcohol'] = self.validate(product['alcohol'])

			item['Article_Number'] = self.validate(product['article'])

			item['Brand'] = self.validate(product['brand'])

			item['Category'] = self.validate(product['category'])

			item['Origin'] = self.validate(product['country'])

			item['Name'] = self.validate(product['name'])

			item['Packaging'] = self.validate(product['packaging'])

			item['Price'] = self.validate(product['price'])

			item['Volume'] = self.validate(product['volume'])

			url = self.domain + self.validate(product['href'])

			yield scrapy.Request(url, callback=self.parse_detail, meta={ 'item' : item })

	def parse_detail(self, response):

		item = response.meta['item']

		data = response.xpath('//div[@class="product-page-body page-body"]//p')

		for pro in data:

			try:

				prop = self.eliminate_space(pro.xpath('.//text()').extract())

				if 'Typ'.lower() in prop[0].lower():

					item['Type'] = prop[1]

				if 'Producent'.lower() in prop[0].lower():

					item['Manufacturer'] = prop[1]

				if 'Nyhet'.lower() in prop[0].lower():

					item['New_Year'] = prop[1]

				if 'Region'.lower() in prop[0].lower():

					item['Region'] = prop[1]

				if 'Distrikt'.lower() in prop[0].lower():

					item['District'] = prop[1]

				if 'Druvor'.lower() in prop[0].lower():

					item['Grapes'] = prop[1]

			except:

				pass

		yield item

	def validate(self, item):

		try:

			return item.replace('\n', '').replace('\t','').replace('\r', '').strip()

		except:

			pass


	def eliminate_space(self, items):

	    tmp = []

	    for item in items:

	        if self.validate(item) != '':

	            tmp.append(self.validate(item))

	    return tmp