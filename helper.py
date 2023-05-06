import datetime
import requests
from config import *

class Helper():
    "Helper Class"

    def url_to_text(self, url):
        r = requests.get(url)
        if r.status_code == 200:
            return r.text
        return None

    def year_date(self):
        if START_YEAR == None:
            now = datetime.datetime.now()
            return now.year

        assert isinstance(START_YEAR, int)
        assert isinstance(COUNT_YEAR, int)
        assert len(f"{START_YEAR}") == 4
