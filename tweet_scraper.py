from selenium import webdriver
from selenium.common.exceptions import StaleElementReferenceException
import time
import os
import io
import dateutil.parser
from dateutil.relativedelta import relativedelta
import sys
from Tweet import Tweet

start_date = dateutil.parser.isoparse(sys.argv[1])
top_x = int(sys.argv[2])

query_word_count = int(sys.argv[3])
query_words = ""
for x in range(query_word_count):
    if x == query_word_count - 1:
        query_words += sys.argv[4 + x]
    else:
        query_words += sys.argv[4 + x] + "%20OR%20"

date_range = []
date_format = "%Y-%m-%d"
current = dateutil.parser.isoparse("2014-03-21")
while current >= start_date:
    date_range.append(current.strftime(date_format))
    current = current - relativedelta(days=1)

chrome_options = webdriver.ChromeOptions()
chrome_options.add_experimental_option("prefs", {"profile.default_content_settings.cookies": 2})

tweets = []
browser = webdriver.Chrome(options=chrome_options)

tweet_count = 0
# os.system('clear')
start_time = time.time()
for date in date_range:
    todays_tweets = set()
    from_date = (dateutil.parser.isoparse(date) - relativedelta(days=1)).strftime(date_format)
    url = "https://twitter.com/search?q=(" + query_words + ")%20min_retweets%3A5%20lang%3Aen%20until%3A" + date + "%20since%3A" + from_date + "&src=typed_query"
    browser.get(url)
    time.sleep(5)
    os.system('clear')
    print("Day Count: "  + str(len(tweets)))
    print("Tweet Count: " + str(tweet_count))
    elapsed = time.time() - start_time
    print("Elapsed Time: %s seconds" % (elapsed))
    print("Days / Min: " + str(len(tweets) / elapsed * 60))
    current_scroll_height = 0
    new_scroll_height = 1
    while len(todays_tweets) < top_x:
        twitter_elms = browser.find_elements_by_css_selector("div[data-testid='tweet']")
        for post in twitter_elms:
            try:
                if len(todays_tweets) >= top_x:
                    break
                date = dateutil.parser.isoparse(post.find_element_by_tag_name("time").get_attribute("datetime"))
                username_field = post.find_element_by_css_selector("div[class='css-901oao css-bfa6kz r-9ilb82 r-18u37iz r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-qvutc0']")
                username = username_field.find_element_by_tag_name("span").text
                text_field = post.find_elements_by_css_selector("div[class='css-901oao r-1fmj7o5 r-1qd0xha r-a023e6 r-16dba41 r-rjixqe r-bcqeeo r-bnwqim r-qvutc0']")
                like_container = post.find_element_by_css_selector("div[data-testid='like']")
                like_field = like_container.find_element_by_tag_name("span")
                likes = like_field.find_element_by_tag_name("span").text
                if len(text_field) == 1:
                    text = ''.join([x.text for x in text_field[0].find_elements_by_tag_name("span")])
                    todays_tweets.add(Tweet(date, username, text, likes))
                else:
                    print("No text in tweet at: " + str(date))
            except StaleElementReferenceException:
                continue
            except Exception as e:
                print(e)
        current_scroll_height += 500
        browser.execute_script("window.scrollTo(0, {})".format(current_scroll_height))
        time.sleep(0.5)
    tweets.append(todays_tweets)
    tweet_count += len(todays_tweets)
    with io.open("twitter_output2.csv", "a", encoding="utf-8") as f:
        f.write(str(date) + ",")
        for tweet in todays_tweets:
            f.write(str(tweet.date) + "," + str(tweet.author) + "," + str(tweet.likes) +",\"" + tweet.text.replace('\n', ' ').replace('\r', ' ') + "\",")
        f.write("\n")
browser.quit()