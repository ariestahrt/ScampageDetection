from ast import parse
from urllib import request
import lxml.html
import difflib
from io import StringIO
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import re
from collections import Counter
import math
import requests
import tinycss

# Baca file content
def read_file(filename):
	try:
		with open(filename, 'r', encoding="utf8") as f:
			data = f.read()
		return data

	except Exception as ex:
		print("Error opening or reading input file: ", ex)
		exit()

# Ekstrak tag HTML
def get_html_tag(html):
    tags = list()

    for element in html.getroot().iter():
        if isinstance(element, lxml.html.HtmlElement):
            tags.append(element.tag)
        elif isinstance(element, lxml.html.HtmlComment):
            tags.append('comment')
        else:
            raise ValueError(f"Unknown element {element}");

    return tags

html1 = read_file("amazon_real.html")
html2 = read_file("paypal_real.html")

css_text = '''
div {padding : 2px; }
p {padding : 3px; color : #ff0000}
.class1 {padding : 2px; color : #ff0000}
.class2 {padding : 3px}
#id1 {padding : 2px; color : #ff0000} 
#id2 {padding : 3px; color : #00ff00}
'''

example = {
    "padding": {
        '2px': ['div', '.class1','#id1'],
        '3px': ['p', '.class2', '#id2']
    }
}

arr_css= {}

css_parser=tinycss.make_parser('page3');
stylesheet=css_parser.parse_stylesheet(css_text);

for rule in stylesheet.rules:
    for d in rule.declarations:
        for v in d.value:
            if d.name not in arr_css.keys():
                arr_css[d.name] = {}

            if v.as_css() not in arr_css[d.name].keys():
                arr_css[d.name][v.as_css()] = []

            if rule.selector.as_css() not in arr_css[d.name][v.as_css()]:
                arr_css[d.name][v.as_css()].append(rule.selector.as_css())

print(arr_css)

exit()
soup = BeautifulSoup(html1, "html.parser")
print("ok")
for link in soup.select('link'):
    if "css" in link["rel"] or "stylesheet" in link["rel"]:
        print(link["href"])
        r = requests.get(link["href"])
        # print(r.text)
        arr_css = {}

        css_parser=tinycss.make_parser('page3');
        stylesheet=css_parser.parse_stylesheet(r.text);

        for rule in stylesheet.rules:
            for d in rule.declarations:
                for v in d.value:
                    if d.name not in arr_css.keys():
                        arr_css[d.name] = {}

                    if v.as_css() not in arr_css[d.name].keys():
                        arr_css[d.name][v.as_css()] = []

                    if rule.selector.as_css() not in arr_css[d.name][v.as_css()]:
                        arr_css[d.name][v.as_css()].append(rule.selector.as_css())

        print(arr_css)

    break