#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import click

@click.command()
@click.option('--num', default=100000, help='Number of Greek Rank posts to be loaded.')
@click.argument('base_discussion_url', help='URL of the Greek Rank discussion page')

def scraper(num, base_discussion_url):
    """ 
    

    """
    next_page = True
    cur_discussion_url = base_discussion_url

    while next_page:
        with urlopen('base_discussion_url') as response:
            soup = BeautifulSoup(response, 'html.parser')
            for anchor in soup.find_all('a'):
                print(anchor.get('href', '/'))
        pass

if __name__ == '__main__':
    scraper()