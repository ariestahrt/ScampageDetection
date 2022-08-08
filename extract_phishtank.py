import requests
import re

def pishtank_scrapper(page, targetid):
    URL = f"https://phishtank.org/target_search.php?page={page}&target_id={targetid}&Search=Search&valid=y&active=y"
    r = requests.get(URL)

    regex = r"(?<=href=\"phish_detail\.php\?phish_id=).*?(?=\">)"
    matches = re.finditer(regex, r.text, re.MULTILINE)
    for matchNum, match in enumerate(matches, start=1):
        report_id = match.group()
        r2 = requests.get(f"https://phishtank.org/phish_detail.php?phish_id={report_id}")
        phis_url = r2.text.split('<span style="word-wrap:break-word;"><b>')[1].split('</b>')[0]
        print(phis_url)

        f = open("phis_paypal.txt", "a")
        f.write(phis_url+"\n")
        f.close()
        # print(match.group())

for i in range(10):
    pishtank_scrapper(i, 1)