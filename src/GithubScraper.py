import os
import sys
import base64
import time
import datetime
from datetime import timedelta

from github import Github
from Print import Print

print = Print() # add glorious indentation and colors to print

class GithubScraper(object):
    def __init__(
                    self,
                    max_repos = float('inf'),
                    overwrite_repos = True,
                    filters = [],
                    start_date = datetime.datetime.strptime('20080401', r'%Y%m%d').date(),
                    interval_length = 10000, # Default interval in days so big it will be only one interval
                ):
        self.max_repos = max_repos
        self.filters = filters
        self.start_date = start_date
        self.interval_length = interval_length
        self.github = Github(os.getenv("GITHUB_ACCESS_TOKEN"))
        self.root = os.path.join(os.path.dirname(os.path.realpath(__file__)), "../")
        
    def scrape(self):
        print.info("Initializing scrape")
        # github API limit search results to 1000 pages.
        # Therefore, cut up the search in several time intervals
        for interval in self.make_time_intervals():
            self.scrape_interval(interval)

    def search(self, interval):
        while True:
            try:
                it = enumerate(self.github.search_repositories(query="Laravel created:" + interval, sort="stars"))
                yield from it
                return   # if we completed the yield from without an exception, we're done!

            except:  # you should probably limit this to catching a specific exception types
                print.warning("Going to sleep for 1 hour. The search API hit the limit?", datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"))
                time.sleep(3600)
                print.warning("Finished sleeping what happens now ... (debug)")


    def scrape_interval(self, interval):
        print.info("Scraping matches in timeframe", interval)
        for repo_number, repo in self.search(interval):
            print.reset()
            if repo_number >= self.max_repos:
                print.warning("Max number of repos processed, bye bye")
                break

            if self.github.rate_limiting[0] <= 1:
                print.warning("Going to sleep for 60 seconds due to API rate limiting:")
                print(self.github.rate_limiting[1] - self.github.rate_limiting[0], "/",self.github.rate_limiting[1])
                time.sleep(60)
                # Hack! resets the rate_limit dump to the core API
                # Then the rate will probably OK so we dont go back to sleep
                self.github.get_rate_limit()

            print.info(datetime.datetime.now().strftime("%I:%M%p on %B %d, %Y"), interval, "repo number", repo_number, repo.full_name, '**************************************************************************************')    
            print.group()

            repo_folder = os.path.join(self.root, "data/raw", repo.full_name)
            
            if os.path.isdir(repo_folder):
                print.warning('Skipping already harvested repo', repo.full_name)
                continue
            
            os.makedirs(repo_folder, exist_ok=True)
            
            for filter in self.filters:
                try:
                    item = repo.get_contents(filter)
                except:
                    continue                                           
                if isinstance(item, list):
                    self.save_dir(repo, filter)    
                elif item.type == "file":
                    self.save_file(repo, filter) 
                else:
                    raise Exception('Unexpected item type (only support dir/file')                                           
        
        print.success("Done!")

    # Split up the queries since max results per query is 1000
    def make_time_intervals(self):
        intervals = []
        start_date = self.start_date

        # emulate do-while
        while True:
            end_date = start_date + timedelta(days=self.interval_length)
            intervals.append(str(start_date) + ".." + str(end_date))
            start_date = end_date + timedelta(days=1)
            if end_date > datetime.datetime.now().date():
                break
        
        return intervals

    def save_dir(self, repo, dir):
        try:
            dir_content = repo.get_dir_contents(dir)

            for item in dir_content:
                try:
                    if item.type == "dir":
                        self.save_dir(repo, item.path)    
                    elif item.type == "file":
                        self.save_file(repo, item.path) 
                    else:
                        raise Exception('Unexpected item type (only support dir/file')                               
                except:
                    print.fail('Could not save', item.type, "from", repo.full_name)                    
        except:
            print.fail('Could not find specified folder of', repo.full_name)

    def save_file(self, repo, file):
        try:
            filename = os.path.join(self.root, "data/raw", repo.full_name, file)
            os.makedirs(os.path.dirname(filename), exist_ok=True)
            with open(filename, "wb") as f:
                f.write(
                        base64.b64decode(
                                repo.get_contents(file).content
                        )
                )
                f.close()
                print.success('Saved', file)
        except:
            print.fail("Could not save file", file)