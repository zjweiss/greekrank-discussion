#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import click
import json

BASE = "https://www.greekrank.com"

@click.command()
@click.option('--num', "-n", default=100000, help='Number of Greek Rank posts to be loaded.')
@click.option('--base_discussion_url', "--url", "-u",required=True, type=click.STRING, help='URL of the Greek Rank discussion page')
def main(num, base_discussion_url):
    print(f"base_discussion_url: {base_discussion_url}")
    print(f"num: {num}")
    post_scraper(num, base_discussion_url)





def post_scraper(num, base_discussion_url):
    """ 
    

    """
    next_page_exists = True
    cur_discussion_url = base_discussion_url
    post_url_list = []

    while next_page_exists:
        with urlopen(cur_discussion_url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            
            # Get all post urls from page
            for post in soup.find_all('h5','discussion-box-head'):
                relative = post.find("a").get("href")
                post_url_list.append(BASE + relative)

            # Get next page if available
            next_page = soup.find(string='NEXT >')
            if not next_page:
                next_page_exists = False
            else:
                next_page = next_page.parent
                cur_discussion_url = BASE + next_page.attrs["href"]

    
    # We have all post urls.
    # Scrape individual posts now.
    post_content_scraper(post_url_list)

            
        


def post_content_scraper(url_list):
    content_list = {}

    for url in url_list:
        with urlopen(url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            
            # Get all post urls from page
            for post in soup.find_all('h5','discussion-box-head'):
                relative = post.find("a").get("href")
                post_url_list.append(BASE + relative)

            # Get next page if available
            next_page = soup.find(string='NEXT >')
            if not next_page:
                next_page_exists = False
            else:
                next_page = next_page.parent
                cur_discussion_url = BASE + next_page.attrs["href"]


            cur_post = {
                "title" : title,
                "author" : author,
                "date" : date,
                "views" : views,
                "upvotes" : upvotes,
                "downvotes" : downvotes,
                "comments" : comment_dict
            }
            content_list.append(cur_post)

    json_object = json.dumps(content_list, indent = 4) 
    print(json_object)

if __name__ == '__main__':
    main()