# Import required libraries
import os
import argparse
import pandas as pd
import xlsxwriter
import matplotlib.pyplot as plt
from apiclient.discovery import build
from apiclient.errors import HttpError
from oauth2client.tools import argparser
from googleapiclient.discovery import build


# CREDENTIALS
DEVELOPER_KEY = ''
YOUTUBE_API_SERVICE_NAME = "youtube"
YOUTUBE_API_VERSION = "v3"


# YOUTUBE API BUILD OBJECT
youtube = build(YOUTUBE_API_SERVICE_NAME, YOUTUBE_API_VERSION,developerKey=DEVELOPER_KEY) 

# Passed in some links also queries can be passed in here. 
query_link = ['https://www.youtube.com/watch?v=udEFwab2txA', 'https://www.youtube.com/watch?v=0r6C3z3TEKw', 
			'https://www.youtube.com/watch?v=xC-c7E5PK0Y', 'https://www.youtube.com/watch?v=3hcQKZ774QQ',
			'https://www.youtube.com/watch?v=z2DAfhsg0I8', 'https://www.youtube.com/watch?v=sa-TUpSx1JA',
			'https://www.youtube.com/watch?v=Tzl0ELY_TiM', 'https://www.youtube.com/watch?v=vEq6vmKIJwo',
			'https://www.youtube.com/watch?v=iURPY28jOD4', 'https://www.youtube.com/watch?v=X3paOmcrTjQ',
			'https://www.youtube.com/watch?v=l8KqHviJ-bg', 'https://www.youtube.com/watch?v=JntENdz4g1M',
			'https://www.youtube.com/watch?v=Ck0ozfJV9-g', 'https://www.youtube.com/watch?v=GWGDlM1KNTU',
			'https://www.youtube.com/watch?v=1w3iHEBv1vo', 'https://www.youtube.com/watch?v=HixtlBP4IwY'] # 16 Query Links



#, 'https://www.youtube.com/watch?v=FKihkRS4_iI', 'https://www.youtube.com/watch?v=s98fD6ILORo', 'https://www.youtube.com/watch?v=1Hbh3VN4IU4']
# _scrapedFile = open(r'C:\Users\Rohan Shetty\Desktop\YouTube Data Scraper1\video_links.txt', 'r')
# query_link = [f for f in _scrapedFile]
# print(query_link)
# print('lenght of query', len(query_link))


def yt_query_stats(queries, max_results=500, order="relevance", token=None, location=None, location_radius=None):
	'''
	Func: Sends a request to YouTube V3 API which returns a search response to a query/query links passed in 
	'''
	
	response = {}
	for query in queries:
		search_response = youtube.search().list(
		q=query,
		type="video",
		pageToken=token,
		order = order,
		part="id,snippet",
		maxResults=max_results,
		location=location,
		locationRadius=location_radius).execute()
		print("Search Completed...")


		items = search_response['items'] #50 "items"
		print('len of items', len(items))

		#Assign 1st results to title, channelId, datePublished 
		title = items[0]['snippet']['title']
		channelId = items[0]['snippet']['channelId']
		datePublished = items[0]['snippet']['publishedAt']
		print("First result is: \n Title: {0} \n Channel ID: {1} \n Published on: {2}".format(title, channelId, datePublished))
		response[queries.index(query)] = search_response

	return response

def store_results(response):

	'''
	Func: This is store the results from response in a form of dict, so that we can later export as a dataframe to csv
	'''

	title, channelId, channelTitle = [], [], []
	categoryId, videoId, publishedDate = [], [], []
	viewCount, likeCount, dislikeCount = [], [], []
	commentCount, favoriteCount = [],  []
	category, tags, videos = [], [], []

	for res in response:
		for search_result in response[res].get("items", []):
			if search_result["id"]["kind"] == "youtube#video": # append title and video for each item
				title.append(search_result['snippet']['title'])
				videoId.append(search_result['id']['videoId']) # collect stats on each video using videoId

				stats = youtube.videos().list(
				part='statistics, snippet',
				id=search_result['id']['videoId']).execute()

				channelId.append(stats['items'][0]['snippet']['channelId']) # CHANNEL ID
				channelTitle.append(stats['items'][0]['snippet']['channelTitle']) # CHANNEL TITLE

				categoryId.append(stats['items'][0]['snippet']['categoryId']) # CATEGORY ID
				favoriteCount.append(stats['items'][0]['statistics']['favoriteCount']) # FAVORITE COUNT

				publishedDate.append(stats['items'][0]['snippet']['publishedAt']) # PUBLISHED DATE
				viewCount.append(stats['items'][0]['statistics']['viewCount']) # VIEW COUNT


		# Not every video has likes/dislikes enabled so using try & except

				try:
					likeCount.append(stats['items'][0]['statistics']['likeCount']) # LIKE COUNT
				except:
					print("Video titled {0}, on Channel {1} Likes Count is not available".format(stats['items'][0]['snippet']['title'],
				                                                                         stats['items'][0]['snippet']['channelTitle']))
					print(stats['items'][0]['statistics'].keys())
					likeCount.append("Not available")

				try:
					dislikeCount.append(stats['items'][0]['statistics']['dislikeCount']) # DISLIKE COUNT
				except:

					print("Video titled {0}, on Channel {1} Dislikes Count is not available".format(stats['items'][0]['snippet']['title'],
				                                                                            stats['items'][0]['snippet']['channelTitle']))
					print(stats['items'][0]['statistics'].keys())
					dislikeCount.append("Not available")

				if 'commentCount' in stats['items'][0]['statistics'].keys():
					commentCount.append(stats['items'][0]['statistics']['commentCount']) # COMMENT COUNT
				else:
					commentCount.append(0)

				        

				youtube_dict = {query:query_link[res], 'channelTitle': channelTitle,
				            'categoryId':categoryId,'title':title, 'publishedAt':publishedDate,
				            'viewCount':viewCount,'likeCount':likeCount,'dislikeCount':dislikeCount,
				            'commentCount':commentCount}

	return youtube_dict


#Run YouTube Search


def write_to_excel(query_link, path, filename):
	'''
	Func: Writes the scraped data to dataframe which's then written to xlsx file.
	'''

	response = yt_query_stats(query_link)
	results = store_results(response)
	yt_data = pd.DataFrame(results) # Write the results to Dataframe

	# Create or Add a new Worksheet
	if os.path.join(path, filename):
		workbook = xlsxwriter.Workbook(filename)
		worksheet = workbook.add_worksheet()
	else:
		workbook = xlsxwriter.Workbook(os.path.join(path,filename))

	# Write Dataframe to the Excel File
	try:
		yt_data.to_excel(os.path.join(path, filename),
                  sheet_name= filename)
		return True
	except Exception as e:
		return e


path = r'C:\Users\Rohan Shetty\Desktop\YouTube Data Scraper1'

print(write_to_excel(query_link, path, filename='test10.xlsx')) # Excel File with all the Data*
