# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/lib')
from bs4 import BeautifulSoup

def read_html(filepath):
    file = open(filepath)
    html = file.read()
    file.close()
    return html

html = read_html('data/29849.html')
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())

spirit_name = ''
spirit_src_url = ''

wiz_value = soup.find('h2', id='wiz_value')
spirit_image_url = wiz_value.find_next_siblings('img')[0]['src']
wiz_value_table = wiz_value.find_next_siblings('table')[0]
for row in wiz_value_table.find_all('tr'):
    for col in row.find_all('td'):
        spirit_name = col.string
        break

print (spirit_name)
print (spirit_image_url)
