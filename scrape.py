import requests
import pandas as pd
import datetime
import os
import sys
from requests_html import HTML

BASE_DIRS = os.path.dirname(os.path.abspath(__file__))

def url_to_text(url, filename="world.html"):
    r = requests.get(url)
    if r.status_code == 200:
        html_text = r.text
        with open(filename, "w") as f:
            f.write(html_text)
        return html_text
    return None

def parse_and_extract(url, name):
    result = url_to_text(url)
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
    filename_path = os.path.join(folder_path, f"{name}.csv")
    df.to_csv(filename_path, index=False)

    return True

def run_date(start_year=None, end_year=0):
    if start_year == None:
        now = datetime.datetime.now()
        start_year = now.year

    assert isinstance(start_year, int)
    assert isinstance(end_year, int)
    assert len(f"{start_year}") == 4

    for i in range(0, end_year+1):
        url = f"https://www.boxofficemojo.com/year/world/{start_year}"
        finished = parse_and_extract(url, name=start_year)

        if finished:
            print(f"Finished {start_year}")
        else:
            print(f"{start_year} is not finished")

        start_year -= 1

if __name__ == "__main__":
    try:
        start = int(sys.argv[1])
    except:
        start = None
    try:
        end = int(sys.argv[2])
    except:
        end = 0
    run_date(start_year=start, end_year=end)
