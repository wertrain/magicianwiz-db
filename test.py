# -*- coding: utf-8 -*-
import sys, os
sys.path.append(os.path.dirname(os.path.abspath(__file__)) + '/lib')
from bs4 import BeautifulSoup

html = """
    <html>
    ...
    </html>
"""
soup = BeautifulSoup(html, 'html.parser')
print(soup.prettify())