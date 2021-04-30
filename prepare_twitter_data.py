import sys
import io
import re
import emoji
import nltk
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import dateutil.parser
from Tweet import Tweet
from nltk.corpus import stopwords
stop_words = stopwords.words('english')

filename = sys.argv[1]
output_filename = sys.argv[2]
count = 0
iso_regex = r'20\d\d-[012]\d-[0123]\d \d\d:\d\d:\d\d\+00:00'
username_regex = r'[^,]*'
likes_regex = r'[^,]*'
body_regex = r'\".*?\"'
tweet_re = '{0},{1},{2},{3},20'.format(iso_regex,username_regex, likes_regex,body_regex)
tweet_re = re.compile(tweet_re)
with io.open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        initial_date_string = line[0: line.index(",")]
        line = line[line.index(",") + 1:]
        initial_date = dateutil.parser.isoparse(initial_date_string)
        days_tweets = []
        line = line[0: -1]
        line += "20"
        all_tweets = []
        while tweet_re.search(line) != None:
            match = tweet_re.search(line)
            end = match.end()
            all_tweets.append(line[0: end - 2])
            line = line[end - 2:]
        tweet_arr = []
        for t_string in all_tweets:
            tweet_date_string = t_string[0: t_string.index(",")]
            t_string = t_string[t_string.index(",") + 1:]
            tweet_date = dateutil.parser.isoparse(tweet_date_string)
            tweet_author = t_string[0: t_string.index(",")]
            t_string = t_string[t_string.index(",") + 1:]
            tweet_likes = t_string[0: t_string.index(",")]
            t_string = t_string[t_string.index(",") + 1:]
            tweet_body = t_string[1: -2]
            tweet_arr.append(Tweet(tweet_date, tweet_author, tweet_body, tweet_likes))
        # Make all tweets lowercase
        for t in tweet_arr:
            t.text = t.text.lower()
        # Demoji text
        for t in tweet_arr:
            t.text = emoji.demojize(t.text)
        # Remove twitter handles
        for t in tweet_arr:
            t.text = re.sub("(@[A-Za-z0-9_]+)","", t.text)
        # Remove urls
        for t in tweet_arr:
            t.text = re.sub('http[s]?://(?:[a-zA-Z]|[0-9]|[$-_@.&+#]|[!*\(\),]|(?:%[0-9a-fA-F][0-9a-fA-F]))+','', t.text)
        # Remove Digits and Symbols
        for t in tweet_arr:
            t.text = t.text.replace("_", "")
            t.text = re.sub(r'\d+', '', t.text)
            t.text = re.sub(r"[^\w\s']", ' ', t.text)
        # Remove non-ascii symbols
        for t in tweet_arr:
            t.text = t.text.encode('ascii', errors='ignore').decode()
        # Apply stemming
        ps = PorterStemmer()
        words_for_day = []
        for t in tweet_arr:
            words = word_tokenize(t.text)
            for w in words:
                words_for_day.append(ps.stem(w))
        # Remove Stopwords
        words_for_day = [t for t in words_for_day if t not in stop_words]
        #Write out
        with io.open(output_filename, "a", encoding="utf-8") as f:
            f.write(str(initial_date) + ",")
            f.write(" ".join(words_for_day))
            f.write("\n")