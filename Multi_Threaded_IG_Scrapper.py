import csv
import time
import re
import threading
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

# Function to initialize and return a CSV writer object
def initialize_csv_writer(file_path):
    csv_file = open(file_path, 'w', newline='', encoding='utf-8')
    csv_writer = csv.writer(csv_file)
    csv_writer.writerow(["Username", "Comment", "Timestamp", "Likes"])
    return csv_writer, csv_file

# Function to log in to Instagram
def login_to_instagram(username, password, driver, wait):
    start_time = time.time()  # Start measuring login time
    
    driver.get('https://www.instagram.com/accounts/login/')
    username_field = wait.until(EC.element_to_be_clickable((By.XPATH, '//input[@name="username" or @type="text"]')))
    username_field.send_keys(username)
    password_field = driver.find_element(By.XPATH, '//input[@name="password"]')
    password_field.send_keys(password)
    time.sleep(3)
    login_button = driver.find_element(By.XPATH, '//button[@type="submit"]')
    time.sleep(3)
    login_button.click()
    print('Logged in ...')
    element = wait.until(EC.visibility_of_element_located((By.CLASS_NAME, '_ac8f')))
    time.sleep(3)
    element.click()
    print('Not now clicked...')
    time.sleep(2)
    sure_button = wait.until(EC.presence_of_element_located((By.XPATH, '/html/body/div[3]/div[1]/div/div[2]/div/div/div/div/div[2]/div/div/div[3]/button[1]')))
    time.sleep(3)
    driver.execute_script("arguments[0].click();", sure_button)

    end_time = time.time()  # Stop measuring login time
    execution_time = end_time - start_time
    print(f"Login took {execution_time:.2f} seconds")

# Function to scrape comments from a post
def scrape_comments(driver, post_url, wait, csv_writer):
    start_time = time.time()  # Start measuring comment scraping time
    
    driver.get(post_url)
    time.sleep(3)
    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, '.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')))
    comment_section = driver.find_element(By.CSS_SELECTOR, '.x5yr21d.xw2csxc.x1odjw0f.x1n2onr6')
    comment_count = 0

    while True:
        driver.execute_script("arguments[0].scrollTop = arguments[0].scrollHeight;", comment_section)
        time.sleep(2)
        
        WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, '[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')))
        
        comments = driver.find_elements(By.CSS_SELECTOR, '[class="x9f619 xjbqb8w x78zum5 x168nmei x13lgxp2 x5pf9jr xo71vjh xsag5q8 xz9dl7a x1uhb9sk x1plvlek xryxfnj x1c4vz4f x2lah0s x1q0g3np xqjyukv x1qjc9v5 x1oa3qoh x1nhvcw1"]')
        new_comment_count = len(comments)

        if new_comment_count == comment_count:
            print(f"All comments have been scrolled: {comment_count} comments found.")
            break

        comment_count = new_comment_count
        print(f"Scrolled {comment_count} comments")

        for comment in comments:
            comment_text = comment.text
            lines = comment_text.split('\n')

            if len(lines) >= 4:
                username = lines[0]
                comment_text = lines[2]
                timestamp = lines[1]

                # Extract likes count using regular expression
                likes_text = lines[3]
                likes_match = re.search(r'(\d+)\s+likes', likes_text)
                if likes_match:
                    likes = int(likes_match.group(1))
                else:
                    likes = 0  # Default value if likes count cannot be extracted
   
                csv_writer.writerow([username, comment_text, timestamp, likes])
    
    end_time = time.time()  # Stop measuring comment scraping time
    execution_time = end_time - start_time
    print(f"Scraping comments took {execution_time:.2f} seconds")

# Function to scrape comments from multiple posts using multi-threading
def scrape_comments_from_multiple_posts(driver, post_urls, wait, csv_writer):
    for post_url in post_urls:
        scrape_comments(driver, post_url, wait, csv_writer)

# Main program
if __name__ == "__main__":
    csv_writer, csv_file = initialize_csv_writer(r'C:\Users\Administrator\Desktop\New folder/instagram_comments.csv')
    driver = webdriver.Chrome()
    wait = WebDriverWait(driver, 10)
    
    username = 'your username'
    password = 'your password'
    
    login_to_instagram(username, password, driver, wait)
    
    post_urls = [
        'https://www.instagram.com/p/Cxe-2iEo4Uw/',
        'https://www.instagram.com/p/CyDNaOPPyTm/',
        'https://www.instagram.com/p/Cx0MmBvPmSo/',
        'https://www.instagram.com/p/CxPc2KWINTo/',
        'https://www.instagram.com/p/CxM-_qYPeof/'
        # Add more post URLs here
    ]
    
    # Number of threads to use for scraping
    num_threads = 4  # Adjust this as needed

    # Divide the post URLs among the threads
    urls_per_thread = len(post_urls) // num_threads
    threads = []

    for i in range(num_threads):
        start_idx = i * urls_per_thread
        end_idx = (i + 1) * urls_per_thread if i < num_threads - 1 else len(post_urls)
        thread_urls = post_urls[start_idx:end_idx]
        thread = threading.Thread(target=scrape_comments_from_multiple_posts, args=(driver, thread_urls, wait, csv_writer))
        threads.append(thread)

    # Start the threads
    for thread in threads:
        thread.start()

    # Wait for all threads to complete
    for thread in threads:
        thread.join()

    csv_file.close()
    driver.quit()
