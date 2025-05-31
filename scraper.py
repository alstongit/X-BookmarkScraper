from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.options import Options
import time
import sqlite3

def save_to_db(tweets):
    conn = sqlite3.connect('bookmarks.db')
    cursor = conn.cursor()
    
    # Create table
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS tweets (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            url TEXT,
            content TEXT
        )
    ''')

    # Insert tweets
    for url, content in tweets:
        cursor.execute('INSERT INTO tweets (url, content) VALUES (?, ?)', (url, content))
    
    conn.commit()
    conn.close()

# Optional: make Chrome headless (run in background)
options = Options()
# options.add_argument("--headless")

driver = webdriver.Chrome(options=options)

# Step 1: Open Twitter bookmarks
driver.get("https://x.com/i/bookmarks")

# Step 2: Let user manually log in
print("Please log in manually in the opened browser...")
time.sleep(60)  # Adjust as needed to allow login

# Step 3: Scroll and scrape
tweets = set()
scroll_pause = 2
last_height = driver.execute_script("return document.body.scrollHeight")

while True:
    elements = driver.find_elements(By.XPATH, "//article[@data-testid='tweet']")
    
    for el in elements:
        try:
            content = el.text
            tweet_url = el.find_element(By.XPATH, ".//a[contains(@href, '/status/')]").get_attribute("href")
            tweets.add((tweet_url, content))
        except Exception:
            continue

    # Scroll down
    driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
    time.sleep(scroll_pause)
    
    new_height = driver.execute_script("return document.body.scrollHeight")
    if new_height == last_height:
        break
    last_height = new_height

# Step 4: Print or save tweets
print(f"Found {len(tweets)} bookmarked tweets.\n")
for url, text in tweets:
    print(f"{url}\n{text}\n{'-'*40}")

print(f"Found {len(tweets)} bookmarked tweets.\n")

driver.quit()

save_to_db(tweets)
print("✅ All tweets saved to bookmarks.db")