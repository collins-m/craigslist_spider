# craigslist_spider
A webscraper designed using scrapy.

  The 'run_program' batch file executes the spider, exporting all required fields to a csv file
titled 'house_listings.csv' and saving all relevant images to a folder in the root directory.
  The spider itself scrapes craigslist's housing advertisements and exports fileds such as price,
location, and the linkto the ad. It was created as a demonstartation of the scrapy library. No
output was uploaded as none of the images were my own.

  To run the program on your own machine, you will have to change the IMAGES_STORE variable to
your preferred image export location.
For example: IMAGES_STORE = '..\..\craigslist_spider\images'
  
NOTE: This program was made for Windows machines, thus it may not work on other operating systems
      with the batch file. If this is the case, write 'scrapy crawl listings -o foobar.csv' to
      the terminal from the root-directory of this project.
