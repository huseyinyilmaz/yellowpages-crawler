Sample crawler for yellow pages
===============================

Sample crawler for yellow pages.


::

   $ scrapy crawl listings -o business.json -a search=cupcakes -a geo='Tucson, AZ'
   ...
   ...
   $ cat business.json
   [
   {"phone": null, "name": "Shari's Berries", "address_text": "Serving the Tucson area."},
   {"phone": null, "name": "Village Bakehouse", "address": {"region": "AZ", "zipcode": "85704", "street_address": "7882 N Oracle Rd", "locality": "Tucson,\u00a0"}},
   {"phone": null, "name": "Beyond Bread", "address": {"region": "AZ", "zipcode": "85712", "street_address": "6260 E Speedway Blvd", "locality": "Tucson,\u00a0"}},
   ...
   ...
   ]$
