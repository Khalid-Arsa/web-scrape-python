import requests
import pandas as pd
import datetime
import os
import sys
from requests_html import HTML
from helper import *
from urlCall import *

helper = Helper()
urlCall = URLCall()

BASE_DIRS = os.path.dirname(os.path.abspath(__file__))

class ScrapingReport:
    "Scraping Report"
    
    def __init__(self):
        self.url_call = URLCall()

    def parse_and_extract():
        result = helper.url_to_text(url)
        year = helper.year_date()
        if result == None:
            return False
        r_html = HTML(html=result)  # data parsing
        r_table = r_html.find("#table")

        # before you debugging the html, disable the javascript first

        table_data = []
        if len(r_table) == 0:
            return False
        
        parse_table = r_table[0]
        rows = parse_table.find("tr")
        header_rows = rows[0]
        header_cols = header_rows.find("th")
        header_names = [x.text for x in header_cols]
            
        for row in rows[1:]:
            cols = row.find("td")
            row_data = {}
            for i, col in enumerate(cols):
                header_name = header_names[i]
                row_data[header_name] = col.text
            table_data.append(row_data)
            
        df = pd.DataFrame(table_data)
        folder_path = os.path.join(BASE_DIRS, "data")
        os.makedirs(folder_path, exist_ok=True)
        filename_path = os.path.join(folder_path, f"{year}.csv")
        
        for i in range(0, COUNT_YEAR+1):
            finished = df.to_csv(filename_path, index=False)

            if finished:
                print(f"Finished {year}")
            else:
                print(f"{year} is not finished")

            year -= 1

if __name__ == "__main__":
    url = ScrapingReport()
    url.parse_and_extract()
