#python3 crawl.py url.txt technologies.txt
import sys
from bs4 import BeautifulSoup
import requests
import xml.etree.ElementTree as ET

def get_technologies(url, tech_list):
    try:
        page = requests.get(url)
        technologies = []
        if page.headers['Content-Type'].startswith('text/html'):
            soup = BeautifulSoup(page.content, 'html.parser')
            scripts = soup.find_all('script')
            for script in scripts:
                if 'src' in script.attrs:
                    src = script['src']
                    for tech in tech_list:
                        if tech.lower() in src.lower():
                            technologies.append(tech)
        elif page.headers['Content-Type'].startswith('application/xml') or page.headers['Content-Type'].startswith('text/xml'):
            root = ET.fromstring(page.content)
            for elem in root.iter():
                if elem.tag == 'script':
                    src = elem.get('src')
                    if src is not None:
                        for tech in tech_list:
                            if tech.lower() in src.lower():
                                technologies.append(tech)
        return ', '.join(technologies)
    except:
        return ''

if len(sys.argv) < 3:
    print("Please provide the filenames as command line arguments")
    sys.exit(1)

url_filename = sys.argv[1]
tech_filename = sys.argv[2]

with open(url_filename) as f:
    urls = f.read().splitlines()

with open(tech_filename) as f:
    techs = f.read().splitlines()

print(f'{"URL":<60} {"Technologies"}')
for url in urls:
    detected_techs = get_technologies(url, techs)
    print(f'{url:<60} {detected_techs}')
