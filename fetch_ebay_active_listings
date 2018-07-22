from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError
from pymongo import MongoClient
import time
import json
import sys, traceback

active_product_ids = []
active_product_titles = []
active_product_prices = []
active_product_cat_names = []
active_product_cat_ids = []
active_product_img_thumb = []
active_product_img_url = []
active_product_lst_type = []
active_product_watchers = []
active_product_con = []
active_product_loc = []
active_product_start = []

pages = []
page_num = []
page_entries = []
total_pages = []
total_entries = []

class SearchRequest(object):

    def __init__(self, api_key, cat_id):
        self.api_key, self.cat_id = api_key, cat_id
        self.search_body_pages = {
            'categoryId': cat_id,
            'itemFilter': [
                {'name': 'Condition', 'value': 'New'},  # can be used, etc as well
                {'name': 'LocatedIn', 'value': 'US'},  # US only sellers -- can also limit by feedback score, business type, top-rated status, charity, etc.
                {'name': 'MinPrice', 'value': '00000001', 'paramName': 'Currency', 'paramValue': 'USD'},
                {'name': 'MaxPrice', 'value': '99999999', 'paramName': 'Currency', 'paramValue': 'USD'},
                {'name': 'ListingType', 'value': ['FixedPrice', 'StoreInventory', 'AuctionWithBIN']}, # pre-filter to only actionable items (non-bids, etc.)
            ],
            'paginationInput': {
                'entriesPerPage': '100', # always 100 (maximum) &
                'pageNumber': '1' # always 1, as we want to pull the maximum number of pages given a maximum of 100 results per page
            },
            'sortOrder': 'PricePlusShippingLowest' # can filter this to multiple different options as well (Best Offer, Most Watched, etc.)
        }

    def get_pages(self):
        """() -> dict

        Connects to the API,
        Executes a query to find items by their category and takes in predefined parameters search_body_pages,
        Returns the data in dictionary form,
        Returns an integer with the total number of pages.
        """
        try:
            api = Connection(siteid='EBAY-US', appid=self.api_key, config_file=None)
            api.execute('findItemsByCategory', self.search_body_pages)
            self.data = api.response.dict()
            return self.data
        except ConnectionError as e:
            print('Temp connection error placeholder')
            print(e)
            tb = sys.exc_info()[-1]
            print(traceback.extract_tb(tb, limit=1)[-1][1])

    def fetch_active_data(self, data):
        """() -> dict

        Connects to the API,
        Iterates over each page in the previously established range of 1 -> the total number of pages,
        Establish search_body_data parameters,
        Execute a query to find items by their category and takes in predefined parameters search_body_data,
        Return the data in dictionary form,
        Iterates over each item in the returned data dictionary and appends the various data points to their respective lists,
        Prints the values.
        """
        try:
            api = Connection(siteid='EBAY-US', appid=self.api.key, config_file=None)
            for page in range(1, int(self.data['paginationOutput']['totalPages'])):  # for all of the pages in get_pages()
                search_body_data = {
                    # 'keywords': product,
                    'categoryId': self.cat_id,  # We need to feed in the list of ~20,000 (!) categories and subcategories to iterate over.
                    'itemFilter': [  # We also need to REMOVE DUPLICATE LISTINGS (?)
                        {'name': 'Condition', 'value': 'New'},
                        {'name': 'LocatedIn', 'value': 'US'},
                        {'name': 'MinPrice', 'value': '00000001', 'paramName': 'Currency', 'paramValue': 'USD'},
                        {'name': 'MaxPrice', 'value': '99999999', 'paramName': 'Currency', 'paramValue': 'USD'},
                        {'name': 'ListingType', 'value': ['FixedPrice', 'StoreInventory', 'AuctionWithBIN']},
                    ],
                    'paginationInput':
                    {'entriesPerPage': '100',
                    'pageNumber': f'{page}'},
                    'sortOrder': 'PricePlusShippingLowest'}  # can filter this to multiple different options as well
                # Execute QUERY for predefined category
                api.execute('findItemsByCategory', search_body_data)
                self.data = api.response.dict()
                time.sleep(1)
                try:
                    for item in self.data['searchResult']['item']:
                        data = json.dumps(item)
                        if 'watchCount' not in data:
                            active_product_watchers.append(0)  # append 0 if result is not in data
                            # print('Watch count: {}'.format(0))
                        else:
                            active_product_watchers.append(item['listingInfo']['watchCount'])  # otherwise append respective watchCount
                            # print('Watch count: {}'.format(item['listingInfo']['watchCount']))

                        active_product_titles.append(item['title'])
                        active_product_ids.append(item['itemId'])
                        active_product_prices.append(item['sellingStatus']['currentPrice']['value'])  # need to make a float?
                        active_product_cat_names.append(item['primaryCategory']['categoryName'])
                        active_product_cat_ids.append(item['primaryCategory']['categoryId'])
                        active_product_img_thumb.append(item['galleryURL'])
                        active_product_img_url.append(item['viewItemURL'])
                        active_product_lst_type.append(item['listingInfo']['listingType'])
                        active_product_con.append(item['condition']['conditionDisplayName'])
                        active_product_loc.append(item['location'])
                        active_product_start.append(item['listingInfo']['startTime'])

                        print('Title: {}'.format(item['title']))
                        print('Item ID: {}'.format(item['itemId']))
                        print('Price: ${}'.format(item['sellingStatus']['currentPrice']['value']))
                        print('Category Name: {}'.format(item['primaryCategory']['categoryName']))
                        print('Category ID: {}'.format(item['primaryCategory']['categoryId']))
                        print('Image Thumbnail: {}'.format(item['galleryURL']))
                        print('Image URL: {}'.format(item['viewItemURL']))
                        print('Listing type: {}'.format(item['listingInfo']['listingType']))
                        print('Product location: {}'.format(item['location']))
                        print('Condition: {}'.format(item['condition']['conditionDisplayName']))
                        print('Start time: {}'.format(item['listingInfo']['startTime']))
                        print('Page: {}/{}'.format(int(page), int(self.data['paginationOutput']['totalPages'])))
                        print()

                        if page == int(self.data['paginationOutput']['totalPages']):
                            break  # break if last page has been reached

                except KeyError as e:
                    # TODO: temp error catch, add logging here
                    print('Temp key error placeholder')
                    print(e)
                    tb = sys.exc_info()[-1]
                    print(traceback.extract_tb(tb, limit=1)[-1][1])  # Returns the error and the line that threw it.
                    continue

        except ConnectionError as e:
            print('Temp connection error placeholder')
            print(e)
            tb = sys.exc_info()[-1]
            print(traceback.extract_tb(tb, limit=1)[-1][1])

    def zip_value(self):
        """() -> Iterates over any number of lists and returns a comprehensive zip.
        """
        self.x = zip(
            active_product_titles,
            active_product_ids,
            active_product_prices,
            active_product_cat_names,
            active_product_cat_ids,
            active_product_img_thumb,
            active_product_img_url,
            active_product_lst_type,
            active_product_watchers,
            active_product_con,
            active_product_loc,
            active_product_start)
        return self.x

    def write_values(self):
        """() -> Returns a completed-delimited TXT output.

        Zips all of the produict lists for easy indexing,
        Opens the respective .CSV,
        Iterate over the respective data points,
        Write to respective .CSV.
        """
        with open(f'eBay_category_{self.cat_id}.tsv', 'a', encoding="utf-8") as of:
            of.write("active_product_titles\tactive_product_ids\tactive_product_prices\tactive_product_cat_names\tactive_product_cat_ids\tactive_product_img_thumb\tactive_product_img_url\tactive_product_lst_type\tactive_product_watchers\tactive_product_con\tactive_product_loc\tactive_product_start\n")
            for each in self.zip_value():
                # Append values to lists and temporarily print data
                of.write(
                    str(each[0]) + "\t" +
                    str(each[1]) + "\t" +
                    str(each[2]) + "\t" +
                    str(each[3]) + "\t" +
                    str(each[4]) + "\t" +
                    str(each[5]) + "\t" +
                    str(each[6]) + "\t" +
                    str(each[7]) + "\t" +
                    str(each[8]) + "\t" +
                    str(each[9]) + "\t" +
                    str(each[10]) + "\t" +
                    str(each[11]) + "\t" + "\n")

if __name__ == '__main__':
    x = SearchRequest('YOUR-API-KEY-HERE', 'YOUR-CAT(s)-HERE')
    x.fetch_active_data(x.get_pages())
    x.write_values()
