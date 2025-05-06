import pandas as pd
import numpy as np
import requests
from bs4 import BeautifulSoup
import os, time, csv, re
from selenium import webdriver
from selenium.webdriver import Chrome
from selenium.webdriver.common.by import By


def scrape_hubertiming(rows, headers,title, type_result):
    row_cells= []
    for row in rows:
        row_tds = row.find_all("td")
        row_td= [td.get_text(strip=True) for td in row_tds if 'splitCell' not in td.get('class', [])]
        row_cells.append(row_td)

    row_cells= row_cells[5:]
    if len(row_cells) == 0:
         print("No data found in this table")
         return    
    header_cells=[]
    for header in headers:
        header_str= str(header)
        cleaned_header= re.compile(r'<.*?>')
        clean_header= re.sub(cleaned_header, '', header_str)
        header_cells.append(clean_header)

    df= pd.DataFrame(row_cells, columns=header_cells)
    df.to_csv(f'{type_result} {title}.csv', index=False)


driver= Chrome()
driver.get('https://www.hubertiming.com/')
time.sleep(3)

result_tab = driver.find_element(By.LINK_TEXT, 'Results')
result_tab.click()
time.sleep(3)
the_soup= BeautifulSoup(driver.page_source, 'html.parser')
driver.quit()

rows= the_soup.find_all("tr")
links=[]

for row in rows:
    row_a= row.find("a")
    if row_a is None:
        continue
    
    links.append(row_a.get('href'))

link_results = links[40:]

driver= Chrome()
for link in link_results[0:5]:
    print(f'----------------------{link}--------------------')
    driver.get(link)
    time.sleep(3)
    soup= BeautifulSoup(driver.page_source, 'html.parser')
    title= soup.title.text
    title= title.strip('Race results')
    type_result= soup.find('a', attrs={'id':'rootTab'}).text
    rows= soup.find_all('tr')
    headers= soup.find_all("th")
    scrape_hubertiming(rows, headers, title, type_result)

    #try:
    tab_results= [tab.get('href') for tab in soup.find_all('a', attrs={'role':"button"}) 
                      if 'btn-info' not in tab.get('class', [])]
      
    for tab in tab_results:
            #  '//a[contains(@href, "specific-page")]'
            result_tab= driver.find_element(By.XPATH, "//a[contains(@href, '"+tab+"')]")
            time.sleep(3)
          
            result_tab.click()
            soup= BeautifulSoup(driver.page_source, 'html.parser')
            title= soup.title.text
            title= title.strip('Race results')
            type_result= soup.find('a', attrs={'id':'rootTab'})
            if type_result is not None:
                 type_result= type_result.text
            else:
                 continue
            print(f'-----------------------------{type_result}-----------------------------')
            rows= soup.find_all('tr')
            headers= soup.find_all("th")
       
            
            scrape_hubertiming(rows, headers, title, type_result)

    # except Exception as e:
    #     print('No other tab results found', e)

    driver.close()


