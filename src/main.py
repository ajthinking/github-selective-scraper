import datetime
import sys
import os
from dotenv import load_dotenv
from pathlib import Path
#load_dotenv(dotenv_path=Path('../../../') / '.env')
load_dotenv()

# Add parent src hack 
sys.path.append(os.path.join(os.path.dirname(os.path.realpath(__file__)), "../../"))

from Print import Print #pylint: disable=E0401
from GithubScraper import GithubScraper #pylint: disable=E0401

GithubScraper(        
        filters = [
                "database/migrations",
                "composer.json"
        ],
        
        # set this in your .env
        start_date = datetime.datetime.strptime(os.getenv("START_SCRAPING_AT"), r'%Y%m%d').date(),
        
        #interval_length = 1
).scrape()
