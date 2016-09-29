# -*- coding: utf-8 -*-
import logging
import scrapy
from urllib import urlencode
import urlparse

from yellowpages.items import Address
from yellowpages.items import Business

logger = logging.getLogger(__name__)


class ListingsSpider(scrapy.Spider):
    name = "listings"
    allowed_domains = ["yellowpages.com"]

    BASE_URL = urlparse.urlparse('http://www.yellowpages.com/search')

    # crawler argument default values.
    search = 'cupcakes'
    geo = 'Tucson, AZ'

    @staticmethod
    def _ip(query, el_type, prop):
        """filter by given query itemprop and """
        return query.xpath('.//{el}[@itemprop="{prop}"]'.format(
            el=el_type,
            prop=prop,
        ))

    @staticmethod
    def _text(query):
        return query.xpath('text()').extract_first()

    def start_requests(self):
        """Generate starting url for search and geo parameters.

        Those parameters can also be changed by commandline. So we need to
        calculate them on runtime.
        """
        query = {'search_terms': self.search,
                 'geo_location_terms': self.geo}
        parse_result = urlparse.ParseResult(
            scheme=self.BASE_URL.scheme,
            netloc=self.BASE_URL.netloc,
            path=self.BASE_URL.path,
            params=self.BASE_URL.params,
            query=urlencode(query),
            fragment=self.BASE_URL.fragment)

        return [scrapy.Request(parse_result.geturl(), self.parse)]

    def parse(self, response):
        # query for list of businessed
        q = '//div[@class="v-card"][@itemtype="http://schema.org/LocalBusiness"]'  # noqa
        for card in response.xpath(q):
            name = self._text(self._ip(card, 'a', 'name'))
            phone = self._text(self._ip(card, 'a', 'telephone'))

            business = Business(name=name, phone=phone)

            address_p = self._ip(card, 'p', 'address')
            # try to parse itemprops from address
            street_address = self._text(
                self._ip(address_p, 'span', 'streetAddress'))
            locality = self._text(
                self._ip(address_p, 'span', 'addressLocality'))
            region = self._text(
                self._ip(address_p, 'span', 'addressRegion'))
            zipcode = self._text(
                self._ip(address_p, 'span', 'postalCode'))

            if filter(None, [street_address, locality, region, zipcode]):
                # If address is structured create address item
                business['address'] = Address(
                    street_address=street_address,
                    locality=locality,
                    region=region,
                    zipcode=zipcode)
            else:
                # Add ress is plain text add it as address_text
                business['address_text'] = self._text(address_p)

            yield business

            next_url = response.xpath(
                '//a[contains(@class,"next")][contains(text(), "Next")]/@href').extract_first()  # noqa
            if next_url:
                next_page = response.urljoin(next_url)
                yield scrapy.Request(next_page, self.parse)
