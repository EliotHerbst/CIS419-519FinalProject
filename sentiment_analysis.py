import sys
import io
from nltk.tokenize import word_tokenize
from nltk.sentiment.vader import SentimentIntensityAnalyzer

sid = SentimentIntensityAnalyzer()
filename = sys.argv[1]
output_file = sys.argv[2]

output = []
with io.open(filename, "r", encoding="utf-8") as f:
    lines = f.readlines()
    for line in lines:
        initial_date_string = line[0: line.index(",")]
        words = line[line.index(",") + 1:]
        date = initial_date_string[0: line.index(" ")]
        pol = sid.polarity_scores(words)
        output.append(",".join([str(date), str(pol['neg']), str(pol['neu']), str(pol['pos']), str(pol['compound'])]))
with io.open(output_file, "w", encoding="utf-8") as f:
    f.write("date,neg,neu,pos,compound\n")
    for o in output:
        f.write(o + "\n")