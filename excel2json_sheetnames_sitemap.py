#! /usr/bin/env python

# Excel worksheet has columns: semester, status, lastmod, priority

import pandas as pd
import os
from bs4 import BeautifulSoup

data_dir = '/Users/emonson/Dropbox/Sites/FridayForum'
data_file = 'SheetNames.xlsx'
sheet_name = 'Sheet1'
out_file = 'sheet_names.json'

# site_base_url = 'http://vis.duke.edu/FridayForum/'
site_base_url = 'https://users.cs.duke.edu/~emonson/FridayForum/'
site_file = 'sitemap.xml'

# First, convert file to json for use in web schedule page
xl = pd.ExcelFile(os.path.join(data_dir, data_file))
df = xl.parse(sheet_name)

with open(os.path.join(data_dir, out_file), 'w') as f:
    f.write("sheets = " + df.to_json(orient='records'))


# Second, generate the sitemap.xml file
def create_sitemap_url(semester='', status='', lastmod=pd.NaT, priority=0.0):
    url = soup.new_tag('url')
    
    loc = soup.new_tag('loc')
    loc.string = site_base_url
    if semester:
        loc.string += '?semester=' + semester
    url.append(loc)
    
    if not pd.isnull(lastmod):
        modtag = soup.new_tag('lastmod')
        modtag.string = lastmod.strftime('%Y-%m-%d')
        url.append(modtag)
    
    if (priority > 0) and (priority <= 1.0):
        pritag = soup.new_tag('priority')
        pritag.string = str(priority)
        url.append(pritag)
    
    if status == 'current':
        freqtag = soup.new_tag('changefreq')
        freqtag.string = 'weekly'
        url.append(freqtag)
        
    return url


soup = BeautifulSoup(features="xml")
outer = soup.new_tag('urlset')
outer['xmlns'] = "http://www.sitemaps.org/schemas/sitemap/0.9"
soup.append(outer)

# site urls
# always create one for base site, and give it top priority
url = create_sitemap_url(semester='', status='current', priority=0.8)
outer.append(url)

# iterrows() returns (index, Series) tuples
for row in df.iterrows():
    sem_series = row[1]
    url = create_sitemap_url( **(sem_series.to_dict()) )
    outer.append(url)

with open(os.path.join(data_dir, site_file), 'w') as f:
    f.write( soup.prettify() )
