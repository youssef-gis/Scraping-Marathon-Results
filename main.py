import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import re

request = requests.get('https://www.hubertiming.com/results/2018CRFH')
request.raise_for_status()

soup= BeautifulSoup(request.text, "html.parser")
title= soup.title.text
content= soup.get_text()
anchors= soup.find_all("a")

rows= soup.find_all("tr")

row_cells=[]
for row in rows:
    row_td= row.find_all("td")
    cell_td= str(row_td)
    clean_td= re.compile(r'<.*?>')
    cleaned_td= re.sub(clean_td ,'', cell_td)
    # Step 1: Remove all newlines and excessive whitespace
    cleaned = ' '.join(cleaned_td.split())
    # Step 2: Remove brackets and strip whitespace
    cleaned = cleaned.strip('[]').strip()
    # Step 3: Split into components and clean each item
    items = [x.strip() for x in cleaned.split(',')]
    row_cells.append(items)


row_cells= row_cells[5:]
#find table headers
headers= soup.find_all("th")
header_cells=[]
for header in headers:
    header_str= str(header)
    cleaned_header= re.compile(r'<.*?>')
    clean_header= re.sub(cleaned_header, '', header_str)
    header_cells.append(clean_header)

#print(header_cells)

df= pd.DataFrame(row_cells, columns=header_cells)

df.to_csv(f'{title}.csv', index=False)
