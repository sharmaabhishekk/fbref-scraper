import requests
from bs4 import BeautifulSoup
import pandas as pd
from bs4 import Comment
from functools import reduce
import os
from tqdm import tqdm
import argparse

def get_all_player_links(url):
    """Get the all_players links from the base url"""
    
    r = requests.get(url)
    soup = BeautifulSoup(r.content, "lxml")
    player_table_links = soup.find_all("a", text="View Player Stats")
    return player_table_links

def get_table_df(url):
    """For each player_link, scrape the raw HTML table"""
    
    r = requests.get("https://fbref.com" + url.attrs["href"])
    s = BeautifulSoup(r.content, "html.parser")
    comments = s.find_all(string=lambda text: isinstance(text, Comment))
    comments = sorted(comments, key=len, reverse=True)
    t = BeautifulSoup(comments[0], "lxml").find("table")
    return pd.read_html(t.prettify(), flavor='bs4')[0]

def clean_df(df):
    """Clean up the dataframes:
        * Change multi-index
        * Drop some useless columns and rows
        * Make sure 90s column has no NaNs
        * Drop duplicate players (players who've played for more than one team)
        * Tidy column names

    """
    df.columns = [f"{y}_{x}" for x, y in df.columns.to_flat_index()] ##change multi-level index to flat index
    if "90s_" in df.columns:
        df["90s_"] = df["90s_"].fillna(0)
    df.columns = df.columns.str.replace("Unnamed: [0-9]+_level_0", "") ##clean up the column names       
    df = df.drop(columns = ["Rk_", "Matches_"])

    df = df.query("Player_ != 'Player'") ##drop rows where Player is the name
    df = df.drop_duplicates(subset=["Player_"], keep=False).reset_index(drop=True) ##drop players who've played for multiple teams in a season (assuming first row is current club)
    
    for column in df.columns: ##remove those underscorse at the end of column_names
        if column[-1] == "_":
            df.rename(columns={f"{column}": f"{column[:-1]}"})
            
    return df

    
if __name__ == "__main__":

    ap = argparse.ArgumentParser()
    ap.add_argument("-u", "--url", required=True, help="base fbref url from where to scrape data from")
    args = vars(ap.parse_args())

    url = args["url"]
    dir_name = url.split("/")[-1]
    if not os.path.exists(f"../scraped_data/{dir_name}"):
        os.mkdir(f"../scraped_data/")
        os.mkdir(f"../scraped_data/{dir_name}")
    full_path = os.path.abspath(f"../scraped_data/{dir_name}")
    
    dflist = []
    player_table_links = get_all_player_links(url)
    if len(player_table_links)>0:
        
        print(f"Found {len(player_table_links)} players tables. Starting scraping")
        for link in tqdm(player_table_links, desc="Scraping..."):
            df = get_table_df(link)
            dflist.append(clean_df(df))
            
        print("Saving...")    
        for num, df in enumerate(dflist, start=1):
            file_name = os.path.join(full_path, f"data_{num}.csv")
            df.to_csv(file_name, index=False)
            
        print(f"All done! Data saved at: '{full_path}'")
    else:
        print("Can't find any tables. Something went wrong. Maybe try a different url?")
            
    
    
