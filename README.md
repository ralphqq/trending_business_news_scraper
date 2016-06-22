## trending_business_news_scraper
This scrapes Google Trends page for trending business news in the Philippines. This scraper runs on scrapy, selenium and PhantomJS.

## Requirements
1. Selenium (`pip install selenium`)
2. PhantomJS (from http://phantomjs.org/download.html)
3. Scrapy (`pip install scrapy`)

## Running the Scraper
cd to the project's root directory and then run:
```
$ scrapy gtrends
```
To save the output to a JSON file, append `-o <filename.json>` to the above command.

## Output Data
Each scraped item contains the following fields:
* `title`: The news article's title.
* `publisher`: The name of its publisher.
* `since_published`: Time elapsed since first published (string).
* `time_scraped`: A string of the form `'%Y-%m-%d %H:%M:%S'`.
* `story`: The trending story in which the news article belongs.
* `link`: The news article's URL.

## Settings
All settings under `gtrends_scraper\settings.py` are left with their default values, except for the following:
```
ROBOTSTXT_OBEY = False
AUTOTHROTTLE_ENABLED = True
AUTOTHROTTLE_START_DELAY = 5            # uncommented
AUTOTHROTTLE_MAX_DELAY = 60             # uncommented
AUTOTHROTTLE_TARGET_CONCURRENCY = 0.5
```

## Contributing
Please feel free to comment or suggest improvements.
