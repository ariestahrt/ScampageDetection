import lxml.html
import difflib
from io import StringIO
from bs4 import BeautifulSoup
from sklearn.feature_extraction.text import CountVectorizer
import re
from collections import Counter
import math

# Cosine Similarity
def calculate_cosine(arr1, arr2):
    numerator = sum([arr1[i] * arr2[i] for i in range(0, len(arr1))])
    len_vec1 = math.sqrt(sum([x ** 2 for x in arr1]))
    len_vec2 = math.sqrt(sum([x ** 2 for x in arr2]))

    denominator = len_vec1 * len_vec2
    if not denominator:
        return 0.0
    else:
        return float(numerator) / denominator

# Longest Common Subsequence
def lcs(setA, setB):
    dp = [[0 for i in range(len(setB)+1)] for j in range(len(setA)+1)]
    for i in range(1, len(setA)+1):
        for j in range(1, len(setB)+1):
            if setA[i-1] == setB[j-1]:
                dp[i][j] = 1 + dp[i-1][j-1]
            else:
                dp[i][j] = max(dp[i-1][j], dp[i][j-1])
        
    i=len(setA)
    j=len(setB)
    res=[]

    # Dapatkan subsequencenya
    while i > 0 and j > 0:
        if setA[i-1] == setB[j-1]:
            res=[setB[j-1]]+res
            j-=1
            i-=1
        else:
            if dp[i-1][j] > dp[i][j-1]:
                i-=1
            else:
                j-=1

    # Return berupa panjang subsequencenya dan subsequence itu sendiri
    return [dp[len(setA)][len(setB)] , res]

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

# Get rendered text
def get_rendered_text(html):
    soup = BeautifulSoup(html, "html.parser")
    html_text = soup.get_text()

    # Cleaning the text
    while "\n\n" in html_text:
        html_text=html_text.replace("\n\n", "\n")

    while "\t" in html_text:
        html_text=html_text.replace("\t", " ")

    while "  " in html_text:
        html_text=html_text.replace("  ", " ")

    return html_text

def similarity_by_structure(html1, html2):
    try:
        html1 = lxml.html.parse(StringIO(html1))
        html2 = lxml.html.parse(StringIO(html2))
    except Exception as ex:
        print(ex)
        return 0
    
    tags_html1 = get_html_tag(html1)
    tags_html2 = get_html_tag(html2)

    lcs_result = lcs(tags_html1, tags_html2)
    return float(lcs_result[0]/len(tags_html1))*100

    # diff = difflib.SequenceMatcher()
    # diff.set_seq1(tags_html1)
    # diff.set_seq2(tags_html2)

    # return diff.ratio()

def similarity_by_text(text1, text2):
    count_vect = CountVectorizer()
    text_arr_tokenize = count_vect.fit_transform([text1, text2])

    return calculate_cosine(text_arr_tokenize.toarray()[0], text_arr_tokenize.toarray()[1]) * 100

html1 = read_file("amazon_fake.html")
html2 = read_file("amazon_real.html")

html1_text = get_rendered_text(html1)
html2_text = get_rendered_text(html2)

print("======================")
print(html1_text)
print("======================")

print("======================")
print(html2_text)
print("======================")

sim_by_html_structure = similarity_by_structure(html1, html2)
sim_by_rendered_text = similarity_by_text(html1_text, html2_text)

print("Similarity by html structure:", sim_by_html_structure)
print("Similarity by rendered text:", sim_by_rendered_text)