# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/lib')
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), os.pardir)) + '/my')
import urllib
from gae import logging
from scraping import gamewith

def read_html(filepath):
    file = open(filepath)
    html = file.read()
    file.close()
    return html

html = read_html('data/29878.html')
spirit = gamewith.perse_spirit_state(html)
print spirit

#html = read_html('data/11554.html')
#spirit = gamewith.perse_spirit_state(html)
#print spirit['id']
