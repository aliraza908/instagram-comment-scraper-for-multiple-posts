# instagram-comment-scraper-for-multiple-posts

Instagram Comments Scraper
This is a Python script that allows you to scrape comments from Instagram posts. It uses the Selenium library for web automation to log in to an Instagram account, access specific post URLs, and extract comments along with their usernames, timestamps, and likes. The comments are then saved to a CSV file.

Prerequisites
Before using this script, make sure you have the following prerequisites installed:

Python 3.x
Selenium
Chrome WebDriver (or other browser drivers compatible with Selenium)
Chrome Browser
You can install the necessary Python packages using pip:

bash
Copy code
pip install selenium
Getting Started
Clone this repository or download the script to your local machine.

Ensure that you have the Chrome WebDriver installed and the path to the WebDriver is added to your system's PATH environment variable.

Open the script in a code editor of your choice and make the following modifications:

Replace 'your username' and 'your password' with your Instagram username and password.
Add the URLs of the Instagram posts you want to scrape in the post_urls list.
Adjust the number of threads (num_threads) based on your system's capabilities. More threads can speed up the scraping process, but be mindful of Instagram's rate limits to avoid getting temporarily banned.

Save your changes.

Usage
Run the script by executing it with Python:

bash
Copy code
python instagram_comments_scraper.py
The script will perform the following steps:

Initialize a CSV file for storing the comments.

Log in to your Instagram account using the provided credentials.

Scrape comments from the specified Instagram post URLs using multi-threading for faster scraping.

Save the comments to a CSV file.

Note
The script is set to use the Chrome WebDriver. If you prefer to use a different browser, you can replace webdriver.Chrome() with the appropriate WebDriver setup.

This script uses web scraping techniques, and it's important to be aware of Instagram's terms of service and rate limits. Excessive scraping can result in temporary or permanent bans from Instagram.

Make sure to replace the sample post URLs with the actual URLs of the posts you want to scrape.

The script is configured to wait for elements to load on the page before interacting with them to ensure reliable scraping. However, if Instagram's structure changes, you may need to update the script accordingly.

The CSV file will be saved in the specified path, and the file name is instagram_comments.csv.


License
This script is provided under the MIT License. Feel free to use, modify, and distribute it as needed.
