"""Old helper function to fetch individual budget motions."""

import requests
import pandas as pd


def get_docs(party):
    search_url = 'https://data.riksdagen.se/dokumentlista/'
    params = {
        'sok': 'utgiftsområde',
        'doktyp': 'mot',
        'rm': '2021/22',
        'parti': party,
        'sort': 'rel',
        'sortorder': 'desc',
        'utformat': 'json',
        'a': 's'}

    resp = requests.get(search_url, params=params)
    data = resp.json()
    doc_list = data['dokumentlista']['dokument']

    while '@nasta_sida' in data['dokumentlista']:
        resp = requests.get(data['dokumentlista']['@nasta_sida'])
        data = resp.json()
        doc_list.extend(data['dokumentlista']['dokument'])

    docs = pd.DataFrame(doc_list)
    docs = docs[docs.titel.str.startswith('Utgiftsområde')]
    docs = docs[['titel', 'undertitel', 'rm', 'dokument_url_html']]
    docs['Utgiftsområde'] = docs.titel.str.extract('Utgiftsområde (\d+)')
    docs['Utgiftsområde'] = docs['Utgiftsområde'].astype(int)
    docs = docs.sort_values('Utgiftsområde').reset_index(drop=True)
    docs = docs.drop_duplicates(subset=['dokument_url_html'])
    return docs