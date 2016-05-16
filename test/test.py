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
print(soup.prettify())


