# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/lib')
from bs4 import BeautifulSoup
import urllib
import re

def read_html(filepath):
    file = open(filepath)
    html = file.read()
    file.close()
    return html

html = read_html('data/29849.html')
soup = BeautifulSoup(html, 'html.parser')
#print(soup.prettify())

spirit_name = ''
spirit_image_url = ''
spirit_score = ''
spirit_type = ''
spirit_cost = ''
spirit_hp_base = ''
spirit_hp = ''
spirit_attack_base = ''
spirit_attack =  ''
spirit_as2 =  ''
spirit_as1 =  ''
spirit_ss2_type = ''
spirit_ss1_type = ''

number_re = re.compile('\d.\d')
status_re = re.compile('\d+')
ss_re = re.compile('">\S+</a>')

wiz_value = soup.find('h2', id='wiz_value')
spirit_image_url = wiz_value.find_next_siblings('img')[0]['src']

# 名前とスコアの展開
row_count = 0
wiz_value_table = wiz_value.find_next_siblings('table')[0]
for row in wiz_value_table.find_all('tr'):
    for col in row.find_all('td'):
        if row_count == 0:
            spirit_name = col.string
        elif row_count == 1:
            m = number_re.search(str(col))
            if m is not None:
                spirit_score = m.group(0)
            break
        row_count = row_count + 1

# ステータスの展開
row_count = 0
wiz_status_table = wiz_value.find_next_siblings('h3')[0].find_next_siblings('table')[0]
for row in wiz_status_table.find_all('tr'):
    for col in row.find_all('td'):
        if row_count == 0:
            spirit_type = col.string
        elif row_count == 1:
            spirit_cost = col.string
        elif row_count == 2:
            m = status_re.findall(str(col))
            if m is not None:
                spirit_hp_base = m[0]
                spirit_hp = m[1]
        elif row_count == 3:
            m = status_re.findall(str(col))
            if m is not None:
                spirit_attack_base = m[0]
                spirit_attack = m[1]
        row_count = row_count + 1

# AS/SSの展開
row_count = 0
wiz_as_table = wiz_status_table.find_next_siblings('h3')[0].find_next_siblings('table')[0]
for row in wiz_as_table.find_all('tr'):
    for col in row.find_all('td'):
        if row_count == 0:
            spirit_as2 = col.string
        elif row_count == 1:
            spirit_as1 = col.string
        row_count = row_count + 1

row_count = 0
wiz_ss_table = wiz_as_table.find_next_siblings('table')[0]
for row in wiz_ss_table.find_all('tr'):
    for col in row.find_all('td'):
        if row_count == 0:
            m = ss_re.findall(str(col))
            if m is not None:
                spirit_ss2_type = unicode(m[0][2:-4],'utf-8')
        elif row_count == 1:
            m = ss_re.findall(str(col))
            if m is not None:
                spirit_ss1_type = unicode(m[0][2:-4],'utf-8')
        row_count = row_count + 1

#urllib.urlretrieve(spirit_image_url, 'data/29849.jpg')
#print (spirit_name)
#print (spirit_image_url)
#print (spirit_score)
#print (spirit_cost)
#print (sprite_attack_base)
#print (sprite_attack)
#print (sprite_as2)
print (spirit_ss1_type)
