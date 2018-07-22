# For some reason eBay make it surprisingly difficult to find every CATEGORY_ID and as a result I put together this script, 
# so hopefully this script helps a few people who were in my position. All you need is requests and xmltodict. 
# Cheers -- Cooper.

#! /usr/bin/env python
import xmltodict as xml
import requests

url = 'http://open.api.ebay.com/Shopping?callname=GetCategoryInfo&appid={}&siteid={}&CategoryID={}&version=729&IncludeSelector=ChildCategories'
app_id = 'YOUR-APP-ID-HERE'
site_id = '1' # 1 is US
to_get = [-1] # start at the top
done = []
categories = {}

if __name__ == "__main__":
    while len(to_get) > 0:
        cid = to_get.pop()
        re = requests.get(url.format(app_id, site_id, cid))
        root = xml.parse(re.text)
        cats = root['GetCategoryInfoResponse']['CategoryArray']['Category']
        for cat in cats:
            if cat['CategoryID'] not in categories:
                print(cat.get('CategoryName', 0))
                c = {'category_id': cat.get('CategoryID', 0),
                    'category_level': cat.get('CategoryLevel', 0),
                    'category_name': cat.get('CategoryName', 0),
                    'category_parent_id': cat.get('CategoryParentID', 0),
                    'leaf_category': cat.get('LeafCategory', 0),
                    'category_name_path': cat.get('CategoryNamePath', 0)}
                categories[cat['CategoryID']] = c
            done.append(cid)
            if cat['CategoryID'] not in done  and cat['LeafCategory'] == 'false' :
                to_get.append(cat['CategoryID'])

# Returns the data in a tab-seperated .txt file
with open('eBay_categories.tsv', 'w', encoding="utf-8") as of:
    of.write("category_id\tcategory_level\tcategory_name\tcategory_parent_id\tleaf_category\tcategory_name_path\n")
    for k,v in categories.items():
        of.write(str(v['category_id']) + "\t" + str(v['category_level']) + "\t" + str(v['category_name']) + "\t" + str(v['category_parent_id']) + "\t" + str(v['leaf_category']) + "\t" + str(v['category_name_path']) + "\n")
