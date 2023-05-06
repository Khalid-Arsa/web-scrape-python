from config import *
from helper import *

helper = Helper()

class URLCall():
  "Class for report scrape url"

  def get_reports():
    year = helper.year_date()
    
    if year == None:
      return None
      
    url = f"https://www.boxofficemojo.com/year/world/{year}"
    return url
