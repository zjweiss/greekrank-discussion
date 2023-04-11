# greekrank-discussion

##
Promote usability and searchability within the Greek Rank platform.

###
Greek Rank is a popular social media platform within Greek Life circles across the United States. People can post about their fraternal organizations, events they are doing, and (of course) rank how their fraternity/sorrority is. The site has a slow UI, and does not allow users to search based on keywords.

### Use

#### Help Section
```
Usage: main.py [OPTIONS]

  Scrape Greek Rank Discussion section for a given university.

Options:
  -n, --num INTEGER               Number of Greek Rank posts to be loaded.
  -u, --base_discussion_url, --url TEXT
                                  URL of the Greek Rank discussion page
                                  [required]
  --help                          Show this message and exit.
```
 Use:
 `python3 main.py -url <url>`

 Example Use:
`python3 main.py https://www.greekrank.com/uni/62/discussion/`

 Pre-requisites:
  All required libraries are saved in the `requirements.txt file`. 
  
  To install the required libraries please run:
  `pip install -r requirements.txt`