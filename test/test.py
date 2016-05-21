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

def perse_spirit_state(html):
    soup = BeautifulSoup(html, 'html.parser')
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
    spirit_ss2_turn = ''
    spirit_ss1_turn = ''
    spirit_ss2 = ''
    spirit_ss1 = ''
    spirit_legend_mode = []
    spirit_potential = []
    spirit_attribution = []

    number_re = re.compile('\d.\d')
    status_re = re.compile('\d+')
    ss_type_re = re.compile('<\S+>')

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

    # ASの展開
    row_count = 0
    wiz_as_table = wiz_status_table.find_next_siblings('h3')[0].find_next_siblings('table')[0]
    for row in wiz_as_table.find_all('tr'):
        for col in row.find_all('td'):
            if row_count == 0:
                spirit_as2 = col.string
            elif row_count == 1:
                spirit_as1 = col.string
            row_count = row_count + 1

    # SSの展開
    row_count = 0
    wiz_ss_table = wiz_as_table.find_next_siblings('table')[0]
    for row in wiz_ss_table.find_all('tr'):
        for col in row.find_all('td'):
            if row_count == 0:
                m = ss_type_re.findall(col.get_text())
                if m is not None:
                    spirit_ss2_type = m[0][1:-1]
                tmp = col.get_text()
                spirit_ss2 = tmp[tmp.find(u'>')+1:tmp.find(u'【')]
                spirit_ss2_turn = tmp[tmp.find(u'【')+1:tmp.find(u'】')]
            elif row_count == 1:
                m = ss_type_re.findall(col.get_text())
                if m is not None:
                    spirit_ss1_type = m[0][1:-1]
                tmp = col.get_text()
                spirit_ss1 = tmp[tmp.find(u'>')+1:tmp.find(u'【')]
                spirit_ss1_turn = tmp[tmp.find(u'【')+1:tmp.find(u'】')]
            row_count = row_count + 1

    row_count = 0
    wiz_awaken_table = wiz_ss_table.find_next_siblings('table')[0]
    wiz_legend_table = wiz_awaken_table.find_next_siblings('table')[0]
    name = ''
    explanation = ''
    for row in wiz_legend_table.find_all('tr'):
        for col in row.find_all('td'):
            if len(name) == 0:
                name = col.get_text();
            else:
                explanation = col.get_text();
                spirit_legend_mode.append({
                  'name': name,
                  'explanation': explanation
                })
                name = ''

    # 属性の展開
    row_count = 0
    wiz_status = wiz_legend_table.find_next_siblings('h2', id='wiz_status')[0]
    wiz_status_table = wiz_status.find_next_siblings('table')[0]
    for row in wiz_status_table.find_all('tr'):
        for col in row.find_all('td'):
            if row_count == 0:
                tags = str(col).split('<br>')
                for tag in tags:
                    tmp = BeautifulSoup(tag, 'html.parser')
                    spirit_attribution.append(tmp.get_text().split(':')[1])
            row_count = row_count + 1

    # 潜在能力の展開
    wiz_potential = soup.find('h2', id='wiz_potential')
    wiz_potential_table = wiz_potential.find_next_siblings('table')[0]
    name = ''
    explanation = ''
    for row in wiz_potential_table.find_all('tr'):
        for col in row.find_all('td'):
            if len(name) == 0:
                name = col.get_text();
            else:
                explanation = col.get_text();
                spirit_potential.append({
                  'name': name,
                  'explanation': explanation
                })
                name = ''
    return {
        'name': spirit_name,
        'gamewith_score': spirit_score,
        'gamewith_image_url': spirit_image_url,
        'type': spirit_type,
        'cost': int(spirit_cost),
        'base_hp': int(spirit_hp_base),
        'base_attack': int(spirit_attack_base),
        'hp': int(spirit_attack_base),
        'attack': int(spirit_attack),
        'as2': spirit_as2,
        'as1': spirit_as1,
        'ss2': spirit_ss2,
        'ss1': spirit_ss1,
        'ss2_type': spirit_ss2_type,
        'ss1_type': spirit_ss1_type,
        'ss2_turn': spirit_ss2_turn,
        'ss1_turn': spirit_ss1_turn,
        'potentials': spirit_potential,
        'legend_potentials': spirit_legend_mode,
        'attributions': spirit_attribution,
    }

html = read_html('data/29849.html')
spirit = perse_spirit_state(html)
print spirit['legend_potentials']