# Import libraries
import requests
from bs4 import BeautifulSoup
import pandas as pd
import os

BASE_DIRS = os.path.dirname(os.path.abspath(__file__))


class ScrapingReport:
    def parse_extract(self):
        pages = []

        # Collect first page of artists’ list
        for i in range(1, 5):
            url = f'https://web.archive.org/web/20121007172955/https://www.nga.gov/collection/anZ{str(i)}.htm'
            pages.append(url)
        
        for item in pages:
            headers = {
              'User-Agent': 'Khalid Arsa',
              'From': 'sanggoyodk8@gmail.com'
            }
            
            page = requests.get(item, headers=headers)

            # Create a BeautifulSoup object
            soup = BeautifulSoup(page.text, 'html.parser')

            # Pull all text from the BodyText div
            artist_name_list = soup.find(class_="BodyText")

            # Remove bottom links
            last_links = soup.find(class_="AlphaNav")
            last_links.decompose()

            # Pull text from all instances of <a> tag within BodyText div
            artist_name_list_items = artist_name_list.find_all("a")

            table_data = []
            header_names = ["Name", "Link"]

            # Use .contents to pull out the <a> tag's children
            for artist_name in artist_name_list_items:
                names = artist_name.contents[0]
                links = f'https://web.archive.org{artist_name.get("href")}'
                artist_data = [names, links]

                row_data = {}
                for i, data in enumerate(artist_data):
                    header_name = header_names[i]
                    row_data[header_name] = data

                table_data.append(row_data)

            df = pd.DataFrame(table_data)
            folder_path = os.path.join(BASE_DIRS, "data")
            os.makedirs(folder_path, exist_ok=True)
            filename_path = os.path.join(folder_path, f"z-artist-names.csv")

            finished = df.to_csv(filename_path, index=False)

            if not finished:
                print("Finished")
            else:
                print("Not finished")


if __name__ == "__main__":
    url = ScrapingReport()
    url.parse_extract()
