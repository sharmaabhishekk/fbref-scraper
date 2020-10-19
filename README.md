# fbref-scraper
A plain scraper to get data from fbref using only BeautifulSoup and Requests.

## How to use:

```
> python scraper.py --url https://fbref.com/en/comps/9/1889/2018-2019-Premier-League-Stats
```
`url` points to the base fbref url of any league of a given season (default season is the current season).
![Screenshot of base page](https://github.com/sharmaabhishekk/fbref-scraper/blob/main/Capture.PNG)

This creates a `scraped_data` main folder in the parent directory. Different seasons and leagues are stored in different folders within `scraped_data`. 
Each table is saved as a different CSV file. This is a choice I had to settle for since I couldn't figure out any single method to merge all dataframes into a single "main dataframe" which works reliably for all the different leagues without breaking down somewhere. Would appreciate any effort towards it!  
