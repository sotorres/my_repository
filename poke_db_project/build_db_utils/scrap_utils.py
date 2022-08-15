import pandas  as pd
from bs4 import BeautifulSoup
import string

import requests
import re

class ScrapUtils():
    
    def __init__(self):
        pass
    
    
    def getHTMLdocument(self, url):

        response = requests.get(url)
      
        # response will be provided in JSON format
        return response.text
    
    def clean_list(self, line):
            text_list = line.findAll(text=True)
            text_list = [text.replace("\n", '') for text in text_list]
            text_list = [text for text in text_list if len(text)>0]
            return text_list
        
    
    def get_df(self, html_tab):
        lines = html_tab.findAll('tr')
        df = pd.DataFrame(columns=['Característica', 'Base', 'Nivel 50 - Min',
                               'Nivel 50 - Max', 'Nivel 100 - Min', 'Nivel 100 - Max', 'PE'], index=list(range(6)))
        
        for index in list(range(1,7)):
            df.iloc[index-1] = self.clean_list(lines[index])

        df['Característica'] = df['Característica'].astype(str)
        int_cols = [cols for cols in list(df.columns) if cols !='Característica']
        df[int_cols] = df[int_cols].astype(int)

        return df
    
    def get_soup_section(self, url_to_scrape, section:str):
        
        html_doc = self.getHTMLdocument(url_to_scrape)

        soup = BeautifulSoup(html_doc, 'html.parser')  
        
        soup_section = soup.select(section)
        
        return soup_section
    
    def get_mon_stats(self, name='Pikachu'):
        url_to_scrape = f"https://www.wikidex.net/wiki/{name}"

        mitab = self.get_soup_section(url_to_scrape, '.tabpokemon')[1]

        df = self.get_df(mitab)

        return df
    
    def build_gen_df(self, lines, genlen, genid):
    
        df = pd.DataFrame(columns=['N_dex_number', 'Name', 'Generation'], index=range(1,genlen))

        for index in range(1, genlen):
            text_list = self.clean_list(lines[index])
            vals = text_list[:2]
            vals.append(f'Gen {genid+1}')
            df.iloc[index-1] = vals
        return df