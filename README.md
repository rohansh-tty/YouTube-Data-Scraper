# YouTube-Data-Scraper
      Pass on a query & scrape results to CSV

![](https://images.pexels.com/photos/5077064/pexels-photo-5077064.jpeg?auto=compress&cs=tinysrgb&dpr=2&h=650&w=940)

# Usage
  
  * **Setup the Environment**
  
  Open your terminal, using either Conda/Pip, install the requirements.

      conda create --name <env> --file requirements.txt
     
      pip install -r requirements.txt
     
     
  * **Generate a YouTube API Key ![here](https://developers.google.com/youtube/v3/getting-started)**
  
  Once the key is generated restrict it to YouTube Data only and use v3 version. 
  
  
  * **Run the File**
  
  Once the environment is setup, run
    
      python init.py --path <path\to\save\results> --filename <xlsx filename>
  
  With the default path set to current working directory & filename set to *'scraped_results.xlsx'*.
  
  
  
  
