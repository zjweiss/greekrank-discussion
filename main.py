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
    #print(f"base_discussion_url: {base_discussion_url}")
    #print(f"num: {num}")
    post_scraper(num, base_discussion_url)
    #post_content_scraper(["https://www.greekrank.com/uni/62/topic/2858570/sorority-rankings-2021/"])





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
    content_list = []

    for url in url_list:
        with urlopen(url) as response:
            soup = BeautifulSoup(response, 'html.parser')
            
            # Ttile
            title = list(soup.find("div", "discussion-box-head-div", "h1").children)[0].text

            # Text
            text = soup.find("div", "discussion-box-content").find("p").text.split("                                        Posted By: ")[0][46:]

            # Author
            author = " ".join(soup.find("span", "comment").text.split()[1:])

            # Date
            date = soup.find("span", "posted-date").text

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
            content_list.append(cur_post)

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
                        date = list(post.find("span").children)[1].text

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


                        comment_list += child_posts(num,new_children)
                        


                    # Get next page if available
                    next_page = soup.find(string='NEXT >')
                    if not next_page:
                        next_page_exists = False
                    else:
                        next_page = next_page.parent
                        cur_url = BASE + next_page.attrs["href"]



    json_object = json.dumps(content_list, indent = 4) 
    print(json_object)


def child_posts(parent_num, children_list):
    output_list = []
    count = 0
    for post in children_list:
        # Num
        num = str(parent_num) + "." + str(count)
        count += 1

        # Author
        author = " ".join(list(post.find("span").children)[0].text.split()[1:])

        # Date
        date = post.find("span", "posted-date").text

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