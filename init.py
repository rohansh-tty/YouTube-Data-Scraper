import os
import sys  
import argparse
from automate_scraping import write_to_excel 

# sys.path.append(r'C:\Users\Rohan Shetty\Desktop\YouTube Data Scraper1\src')  


def_path = os.getcwd()
def_filename = 'scraped_results.xlsx'


yt_parser = argparse.ArgumentParser( description='Pass in the Path to store Scraped Results', epilog='Keep Scraping :)')


yt_parser.add_argument('--path', metavar='Path', type=str, default=def_path, help='Pass in the Path to store Scraped Results' )
yt_parser.add_argument('--filename', metavar='FileName', type=str,  default=def_filename, help='Pass in the Filename to store Scraped Results')

# Execute args
args = yt_parser.parse_args() # Name Space object created with command line params it's respective args

class YouTube_Scrape:
	def __init__(self, path, filename):
		self.path = path
		self.filename = filename
	def scrape_and_write(self):
		response = yt.write_to_excel(self.path, self.filename)
		print(f'Scraped Data written to {os.path.join(path, filename)}.')
		return response

y1 = YouTube_Scrape(args.path, args.filename)
print(y1.scrape_and_write())