import wikipedia
import json
from bs4 import BeautifulSoup


import time
def get_official():
    r = wikipedia.page('Yevgeny Prigozhin', auto_suggest=False)
    soup = BeautifulSoup(r.html(), 'html.parser')
    country_table = None
    person_info = {

    }
    for table in soup.find_all('table'):
        if table['class'].count('infobox') > 0 and table['class'].count('biography') > 0:
            country_table = table
            for td in table.find_all('td', recursive=True):
                if td.get('class').count('org') > 0 and td.get('class').count('infobox-data') > 0:
                    text = []
                    for elem in td.find_all('a'):
                        if len(elem.text) > 1:
                            text.append(elem.text)
                    person_info['orgs'] = text
            break
    print(text)

    time.sleep(20)

def get_country_infobox(country_name):
    country = wikipedia.search(country_name)
    country = wikipedia.page(title=country[0], auto_suggest=False)
    soup = BeautifulSoup(country.html(), 'html.parser')
    country_table = None
    for table in soup.find_all('table'):
        if table['class'].count('infobox') > 0 and table['class'].count('ib-country') > 0:
            country_table = table
            break

    rows = table.find("tbody", recursive=False)
    if isinstance(rows, list): rows = rows[0]

    rows = rows.findChildren('tr', recursive=False)
    print(len(rows))
    import time
    time.sleep(1)
    people = []
    gov_active = False
    for row in rows:
        try:
            
            th = row.find('th', recursive=False)
            if gov_active:
                if row['class'][0] != 'mergedrow':
                    gov_active = False
                if gov_active:
                    politician = {
                        "name": row.find('td', recursive= False).text,
                        "titles": []
                    }
                    for a in th.findChildren(recursive=True):
                        try:
                            t = a.get('title')
                            if t != None:
                                politician['titles'].append(t)
                        except: pass
                    people.append(politician)
            if th.text == 'Government':
                gov_active = True
        except:
            pass
    return people
