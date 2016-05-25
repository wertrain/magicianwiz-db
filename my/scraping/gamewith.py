# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import re
from gae import log

def perse_spirit_state(html):
    soup = BeautifulSoup(html, 'html.parser')
    spirit_id = None
    spirit_name = None
    spirit_image_url = None
    spirit_score = None
    spirit_type = None
    spirit_cost_base = None
    spirit_cost = None
    spirit_hp_base = None
    spirit_hp = None
    spirit_attack_base = None
    spirit_attack =  None
    spirit_as2 = None
    spirit_as1 = None
    spirit_ss2_type = None
    spirit_ss1_type = None
    spirit_ss2_base_turn = None
    spirit_ss2_turn = None
    spirit_ss1_base_turn = None
    spirit_ss1_turn = None
    spirit_ss2 = None
    spirit_ss1 = None
    spirit_as_name = None
    spirit_ss_name = None
    spirit_legend_mode = []
    spirit_potential = []
    spirit_attribution = []

    number_re = re.compile('\d.\d')
    status_re = re.compile('\d+')
    ss_type_re = re.compile('<\S+>')

    # ID の取得
    canonical_url = soup.find('link', rel='canonical')['href']
    spirit_id = canonical_url[canonical_url.rfind('/')+1:len(canonical_url)]
    # 画像 URL 
    spirit_image_url = soup.find('img', width='200')['src']
    wiz_value = soup.find('img', width='200')
    
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
    wiz_status_table = wiz_value.find_next_siblings('h3')[0].find_next_siblings('table')[0]
    
    # ASの展開
    row_count = 0
    wiz_as_table = wiz_status_table.find_next_siblings('h2', id='wiz_skill')[0].find_next_siblings('table')[0]
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
                m = status_re.findall(spirit_ss2_turn)
                if m is not None:
                    spirit_ss2_turn_base = m[0]
                    spirit_ss2_turn = m[1]
            elif row_count == 1:
                m = ss_type_re.findall(col.get_text())
                if m is not None:
                    spirit_ss1_type = m[0][1:-1]
                tmp = col.get_text()
                spirit_ss1 = tmp[tmp.find(u'>')+1:tmp.find(u'【')]
                spirit_ss1_turn = tmp[tmp.find(u'【')+1:tmp.find(u'】')]
                m = status_re.findall(spirit_ss1_turn)
                if m is not None:
                    spirit_ss1_turn_base = m[0]
                    spirit_ss1_turn = m[1]
            row_count = row_count + 1

    # レジェンドスキルの展開
    wiz_potential_single_table = wiz_ss_table.find_next_siblings('table')[0]
    wiz_legend_table = wiz_potential_single_table.find_next_siblings('table')[0]
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
    wiz_status = soup.find('h2', id='wiz_status')
    wiz_status_table = wiz_status.find_next_siblings('table')[0]
    for row in wiz_status_table.find_all('tr'):
        for col in row.find_all('td'):
            if row_count == 0:
                tags = str(col).split('<br>')
                for tag in tags:
                    tmp = BeautifulSoup(tag, 'html.parser')
                    if tmp.get_text() in ':':
                        spirit_attribution.append(tmp.get_text().split(':')[1])
                    else:
                        spirit_attribution.append(tmp.get_text())
            elif row_count == 1:
                spirit_type = col.get_text()
            elif row_count == 2:
                break
            row_count = row_count + 1

    row_count = 0
    wiz_all_status_table = wiz_status_table.find_next_siblings('table')[0]
    for row in wiz_all_status_table.find_all('tr'):
        for col in row.find_all('td'):
            #if row_count == 0:
            #    spirit_type = col.string
            #elif row_count == 1:
            if row_count == 1:
                m = status_re.findall(str(col))
                if m is not None:
                    spirit_cost_base = m[0]
                    spirit_cost = m[1] if len(m) > 1 else spirit_cost_base
            elif row_count == 2:
                m = status_re.findall(str(col))
                if m is not None:
                    spirit_hp_base = m[0]
                    spirit_hp = m[1] if len(m) > 1 else spirit_hp_base
            elif row_count == 3:
                m = status_re.findall(str(col))
                if m is not None:
                    spirit_attack_base = m[0]
                    spirit_attack = m[1] if len(m) > 1 else spirit_attack_base
            row_count = row_count + 1

    # AS名の取得
    as_name = wiz_status_table.find_next_siblings('h4')[0]
    as_name = as_name.get_text()
    spirit_as_name = as_name[as_name.find(u'【')+1:as_name.find(u'】')]

    # SS名の取得
    ss_name = wiz_status_table.find_next_siblings('h4')[0].find_next_siblings('h4')[0]
    ss_name = ss_name.get_text()
    spirit_ss_name = ss_name[ss_name.find(u'【')+1:ss_name.find(u'】')]
    
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
    # 辞書の生成
    spirit_dict = {
        'id': spirit_id,
        'name': spirit_name,
        'gamewith_score': float(spirit_score),
        'gamewith_image_url': spirit_image_url,
        'type': spirit_type,
        'base_cost': int(spirit_cost_base),
        'base_hp': int(spirit_hp_base),
        'base_attack': int(spirit_attack_base),
        'cost': int(spirit_cost),
        'hp': int(spirit_hp),
        'attack': int(spirit_attack),
        'as2': spirit_as2,
        'as1': spirit_as1,
        'as_name': spirit_as_name,
        'ss2': spirit_ss2,
        'ss1': spirit_ss1,
        'ss_name': spirit_ss_name,
        'ss2_type': spirit_ss2_type,
        'ss1_type': spirit_ss1_type,
        'ss2_turn_base': int(spirit_ss2_turn),
        'ss2_turn': int(spirit_ss2_turn),
        'ss1_turn_base': int(spirit_ss1_turn),
        'ss1_turn': int(spirit_ss1_turn),
        'potentials': spirit_potential,
        'legend_potentials': spirit_legend_mode,
        'attributions': spirit_attribution,
    }
    # パース漏れがないかチェック
    for key, value in spirit_dict.iteritems():
        if value is None:
            log.error ('Invalid Value: ' + key)
    return spirit_dict