#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import click
import json

@click.command()
@click.option('--num', "-n", default=100000, help='Number of Greek Rank posts to be loaded.')
@click.option('--base_discussion_url', "--url", "-u",required=True, type=click.STRING, help='URL of the Greek Rank discussion page')
def main(num, base_discussion_url):
    print(f"base_discussion_url: {base_discussion_url}")
    print(f"num: {num}")
    pass





def post_scraper(num, base_discussion_url):
    """ 
    

    """
    next_page = True
    cur_discussion_url = base_discussion_url
    post_url_list = []

    while next_page:
        with urlopen('base_discussion_url') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for post in soup.find_all('discussion-box-head'):
                print(post.get('href', '/'))
        


def post_content_scraper(url_list):
    content_dict = {}

    for url in url_list:
        pass

    json_object = json.dumps(content_dict, indent = 4) 
    print(json_object)

if __name__ == '__main__':
    main()