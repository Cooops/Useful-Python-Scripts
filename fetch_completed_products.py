from ebaysdk.finding import Connection
from ebaysdk.exception import ConnectionError
import time
from gen_utils import get_trace_and_log
import psycopg2

completed_product_ids = []
completed_product_nick = []
completed_product_titles = []
completed_product_prices = []
completed_product_cat_names = []
completed_product_cat_ids = []
completed_product_img_thumb = []
completed_product_img_url = []
completed_product_lst_type = []
completed_product_con = []
completed_product_loc = []
completed_product_start = []
completed_product_end = []


class SearchRequest(object):
    def __init__(self, api_key, keyword):
        self.api_key, self.keyword = api_key, keyword
        self.search_body_pages = {
            'keywords': keyword,
            'itemFilter': [
                # can be used, etc as well
                # {'name': 'Condition', 'value': 'New'},
                {'name': 'LocatedIn', 'value': 'US'},
                # US only sellers -- can also limit by feedback score, business type, top-rated status, charity, etc.
                {'name': 'MinPrice', 'value': '5', 'paramName': 'Currency', 'paramValue': 'USD'},
                {'name': 'MaxPrice', 'value': '99999999', 'paramName': 'Currency', 'paramValue': 'USD'},
                # pre-filter to only actionable items (non-bids, etc.)
                # {'name': 'ListingType', 'value': ['FixedPrice', 'StoreInventory', 'AuctionWithBIN']},
                # sold items only
                {'name': 'SoldItemsOnly', 'value': 'true'},
            ],
            'paginationInput': {
                # always 100 (maximum) &
                'entriesPerPage': '100',
                # always 1, as we want to pull the maximum number of pages given a maximum of 100 results per page
                'pageNumber': '1'
            },
            # can filter this to multiple different options as well (Best Offer, Most Watched, etc.)
            'sortOrder': 'PricePlusShippingLowest'
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
            api.execute('findCompletedItems', self.search_body_pages)
            self.data = api.response.dict()
            self.pages = int(self.data['paginationOutput']['totalPages'])
            return self.pages
        except ConnectionError as e:
            get_trace_and_log(e)

    def fetch_completed_data(self, pages):
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
            api = Connection(siteid='EBAY-US', appid=self.api_key, config_file=None)
            search_body_data = {
                'keywords': self.keyword,
                # 'categoryId': self.cat_id,
                'itemFilter': [  # We also need to REMOVE duplicate listings in the future (?)
                    # {'name': 'Condition', 'value': 'New'},  # NEW ONLY FOR NOW
                    {'name': 'LocatedIn', 'value': 'US'},
                    {'name': 'MinPrice', 'value': '5', 'paramName': 'Currency', 'paramValue': 'USD'},
                    {'name': 'MaxPrice', 'value': '99999999', 'paramName': 'Currency', 'paramValue': 'USD'},
                    # {'name': 'ListingType', 'value': ['FixedPrice', 'StoreInventory', 'AuctionWithBIN']},
                    # sold items only
                    {'name': 'SoldItemsOnly', 'value': 'true'},
                ],
                'paginationInput':
                    {'entriesPerPage': '100',
                     'pageNumber': f'{page}'},
                # can filter this to multiple different options as well
                'sortOrder': 'PricePlusShippingLowest'}

            api.execute('findCompletedItems', search_body_data)
            self.data = api.response.dict()
            time.sleep(1)
        except KeyError as e:
            get_trace_and_log(e)

        outliers = ["Collector's", "collector's edition", "Collectors", "International", "CE", "Ce", "IE", "Ie",
                    "Poster", "Proxy", "Misprint", "Puzzle", "READ DESCRIPTION", "PLAYTEST", "error", "display",
                    "promo", "display/promo", "framed", "Reprint", "Booster", "Pack", "Factory Sealed"]
        try:
            # search p9 prices everyday?
            # link data points on graph with thumb and url link to historical listing?
            if "Beta" or "Alpha" in input:  # assert certain categories are true?
                # print('Alpha or Beta keyword detected. Pruning CE, IE, and other outliers from search results...')
                print(f'Chugging through...{page}/{self.pages} page(s)...\n')
                for item in self.data['searchResult']['item']:
                    # add catch/skip block for this in future -- using .pop somehow perhaps?
                    assert item['sellingStatus']['sellingState'] == 'EndedWithSales'
                    # TODO: is there a better way to do this?
                    if not any(x in item['title'] for x in outliers):
                        try:
                            completed_product_img_thumb.append(item['galleryURL'])
                        except Exception as e:
                            completed_product_img_thumb.append('No picture')
                        completed_product_nick.append(word)
                        completed_product_titles.append(item['title'])
                        completed_product_ids.append(item['itemId'])
                        completed_product_prices.append(item['sellingStatus']['currentPrice']['value'])
                        completed_product_cat_names.append(item['primaryCategory']['categoryName'])
                        completed_product_cat_ids.append(item['primaryCategory']['categoryId'])
                        completed_product_img_url.append(item['viewItemURL'])
                        completed_product_lst_type.append(item['listingInfo']['listingType'])
                        completed_product_con.append(item['condition']['conditionDisplayName'])
                        completed_product_loc.append(item['location'])
                        completed_product_start.append(item['listingInfo']['startTime'])
                        completed_product_end.append(item['listingInfo']['endTime'])

                        # print('Title: {}'.format(item['title']))
                        # print('Item ID: {}'.format(item['itemId']))
                        # print('Price: ${}'.format(item['sellingStatus']['currentPrice']['value']))
                        # print('Category Name: {}'.format(item['primaryCategory']['categoryName']))
                        # print('Category ID: {}'.format(item['primaryCategory']['categoryId']))
                        # print('Image Thumbnail: {}'.format(item['galleryURL']))
                        # print('Image URL: {}'.format(item['viewItemURL']))
                        # print('Listing type: {}'.format(item['listingInfo']['listingType']))
                        # print('Product location: {}'.format(item['location']))
                        # print('Condition: {}'.format(item['condition']['conditionDisplayName']))
                        # print('Start time: {}'.format(item['listingInfo']['startTime']))
                        # # print('Page: {}/{}'.format(int(page), int(self.data['paginationOutput']['totalPages'])))
                        # print()
        except KeyError as e:
            get_trace_and_log(e)


class DatabaseConnection(object):
    def __init__(self):
        try:
            self.connection = psycopg2.connect("dbname='a' user='b' host='c' password='d' port='e'")
            self.connection.autocommit = True
            self.cursor = self.connection.cursor()
            print("Successfully connected to database.")
        except Exception as e:
            get_trace_and_log(e)
            print("Cannot connect to database.")

    def insert_completed_products(self, ):
        for a, b, c, d, e, f, g, h, i, j, k, l, m in zip(completed_product_nick, completed_product_titles, completed_product_ids, completed_product_prices, completed_product_cat_names, completed_product_cat_ids, completed_product_img_thumb, completed_product_img_url, completed_product_lst_type, completed_product_con, completed_product_loc, completed_product_start, completed_product_end):
            try:
                self.cursor.execute("""INSERT INTO completed_products(completed_product_nick, completed_product_titles, completed_product_ids, completed_product_prices, completed_product_cat_names, completed_product_cat_ids, completed_product_img_thumb, completed_product_img_url, completed_product_lst_type, completed_product_con, completed_product_loc, completed_product_start, completed_product_end)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)""", (a, b, c, d, e, f, g, h, i, j, k, l, m,))  # MAKE SURE to leave the trailing comma (d-->,<--), this will NOT work otherwise.
                print("Unique value inserted...")
            except Exception as e:
                print("Unique value skipped...")
                # get_trace_and_log(e)
        print()
        print('(<*.*<) DATABASE HAS BEEN |P I P E D| (>*.*>)')


if __name__ == '__main__':
    #TODO: could add back in time vaults?
    words = ['Alpha Black Lotus', 'Alpha Mox Sapphire', 'Alpha Mox Jet', 'Alpha Mox Pearl', 'Alpha Mox Ruby', 'Alpha Mox Emerald', 'Alpha Timetwister', 'Alpha Ancestral Recall', 'Alpha Time Walk',
             'Beta Black Lotus MTG', 'Beta Mox Sapphire', 'Beta Mox Jet', 'Beta Mox Pearl', 'Beta Mox Ruby', 'Beta Mox Emerald', 'Beta Timetwister', 'Beta Ancestral Recall', 'Beta Time Walk',
             'Unlimited Black Lotus MTG', 'Unlimited Mox Sapphire', 'Unlimited Mox Jet', 'Unlimited Mox Pearl', 'Unlimited Mox Ruby', 'Unlimited Mox Emerald', 'Unlimited Timetwister', 'Unlimited Ancestral Recall', 'Unlimited Time Walk',]
    for word in words:
        print(f'Searching keyword: {word}')
        x = SearchRequest('API-KEY', word)
        print()
        pages = x.get_pages()+1
        for page in range(1, pages):
            x.fetch_completed_data(page)
    database_connection = DatabaseConnection()
    database_connection.insert_completed_products()
