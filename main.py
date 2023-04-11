#!/usr/bin/env python3
from bs4 import BeautifulSoup
from urllib.request import urlopen
import click
import json
import threading
from datetime import datetime

BASE = "https://www.greekrank.com"

@click.command()
@click.option('--num', "-n", default=100000, help='Number of Greek Rank posts to be loaded.')
@click.option('--base_discussion_url', "--url", "-u",required=True, type=click.STRING, help='URL of the Greek Rank discussion page')
def main(num, base_discussion_url):
    post_scraper(num, base_discussion_url)

def post_scraper(num, base_discussion_url):
    """ 
    Scrape university specific discussion page to extract all individual post pages.
    """
    next_page_exists = True
    cur_discussion_url = base_discussion_url
    post_url_list = []

    while next_page_exists and len(post_url_list) < num:
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
    post_url_list = post_url_list[:num]
    post_content_scraper(post_url_list)

            
def post_content_scraper(url_list):
    """"
    Scrape individual posts by creating async thread for each post.
    """
    content_list = [None] * len(url_list)
    count = 0

    threads = []

    for url in url_list:
        thread = threading.Thread(target=post_content_scraper_thread,args=(url,count,content_list))
        thread.start()
        threads.append(thread)
        count += 1
    
    for thread in threads:
        thread.join()
       


    json_object = json.dumps(content_list, indent = 4) 
    print(json_object)

def post_content_scraper_thread(url, count,content_list):
     """"
     Scrape individual page for all required info.
     This is ran on a thread.
     """
     with urlopen(url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            
            # Ttile
            title = list(soup.find("div", "discussion-box-head-div", "h1").children)[0].text

            # Text
            text = soup.find("div", "discussion-box-content").find("p").text.split("                                        Posted By: ")[0][46:]

            # Author
            author = " ".join(soup.find("span", "comment").text.split()[1:])

            # Date
            date = format_time(soup.find("span", "posted-date").text)

            # Like Box

            like_box = soup.find("ul", "like-box").find_all("li")

            # Views
            views = like_box[2].text.split()[0]

            # Upvotes
            upvotes = int(like_box[0].text)

            # Downvotes
            downvotes = int(like_box[1].text)

            comment_list = []

            cur_post = {
                "title" : title,
                "author" : author,
                "date" : date,
                "text" : text,
                "views" : views,
                "upvotes" : upvotes,
                "downvotes" : downvotes,
                "comments" : comment_list,
                "url" : url
            }
            content_list[count] = cur_post

            next_page_exists = True
            cur_url = url

            while next_page_exists:
                with urlopen(cur_url) as response:
                    soup = BeautifulSoup(response, 'html.parser')
                    
                    # Get all post urls from page
                    for post in soup.find_all('div','discussion-box-reply'):
                        # Num
                        num = int(post.find("strong").text.split("#")[1])

                        # Author
                        author = list(post.find("span").children)[0].text.split()[1]

                        # Date
                        date = format_time(list(post.find("span").children)[1].text)

                        # Text
                        text = list(post.find("div", "discussion-box-content", "p").children)[3].text
                        
                        # Like Box
                        like_box = post.find("ul", "like-box").find_all("li")

                        # Upvotes
                        upvotes = int(like_box[1].text)

                        # Downvotes
                        downvotes = int(like_box[2].text)
                    
                        cur_comment = {
                            "num" : num,
                            "author" : author,
                            "date" : date,
                            "text" : text,
                            "upvotes" : upvotes,
                            "downvotes" : downvotes,
                        }
                        comment_list.append(cur_comment)

                        # Check for children comments
                        children = list(post.next_siblings)
                        children = [child for child in children if child != "\n"]
                        
                        count = 0
                        new_children = []
                        for child in children:
                            if "class" in child.attrs and child.attrs["class"][0] == "discussion-box-reply":
                                break

                            if "class" in child.attrs and child.attrs["class"][0] == "discussion-box-reply-comment":
                                new_children.append(child)


                        comment_list += child_comment_scraper(num,new_children)
                        


                    # Get next page if available
                    next_page = soup.find(string='NEXT >')
                    if not next_page:
                        next_page_exists = False
                    else:
                        next_page = next_page.parent
                        cur_url = BASE + next_page.attrs["href"]

def format_time(time):
    """
    Format time from GreekRank format (ex: Feb 7, 2011 12:18:24 PM) to ISO format.
    """
    time = time.replace("\u00a0","")
    time = datetime.strptime(time,
                  '%b %d, %Y %I:%M:%S %p')
    return time.isoformat(sep=" ")

def child_comment_scraper(parent_num, children_list):
    """
    Scrape child comment posts.
    Note: this has very simular capabilities, but was left seperate due to small changes in comment structure.
    """
    output_list = []
    count = 0
    for post in children_list:
        # Num
        num = str(parent_num) + "." + str(count)
        count += 1

        # Author
        author = " ".join(list(post.find("span").children)[0].text.split()[1:])

        # Date
        date = format_time(post.find("span", "posted-date").text)

        # Text
        text = list(post.find("div", "discussion-box-content", "p").children)[1].text
        
        # Like Box
        like_box = post.find("ul", "like-box").find_all("li")

        # Upvotes
        upvotes = int(like_box[0].text)

        # Downvotes
        downvotes = int(like_box[1].text)

        cur_comment = {
            "num" : num,
            "author" : author,
            "date" : date,
            "text" : text,
            "upvotes" : upvotes,
            "downvotes" : downvotes,
        }
        output_list.append(cur_comment)
    
    return output_list





if __name__ == '__main__':
    main()