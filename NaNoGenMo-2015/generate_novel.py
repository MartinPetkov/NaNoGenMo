#!/usr/bin/python

import sys, getopt
from datetime import datetime, timedelta
import requests
import json
import codecs
import urllib
import pdb
import math


request_url = 'https://tt-history.appspot.com/rpc'
world_woeid = 1

tweets_url = 'http://otter.topsy.com/search.txt'

TOPSY_API_KEY = ''

def str_replace(c):
    if c.isalnum() or c.isspace():
        return c
    else:
        return ' '

def get_word_count(s):
    return len(''.join([str_replace(c) for c in s]).split())


def get_topics(days):
    topics = []

    # Remove the hours, minutes, seconds and microseconds to get the start of the day
    today = datetime.today()
    today -= timedelta(hours=today.hour,\
                       minutes=today.minute,\
                       seconds=today.second,\
                       microseconds=today.microsecond)

    days_ago = 0
    while days_ago < days:
        # Get the current days start and end in milliseconds from Jan. 1, 1970
        start_of_day = today - timedelta(days=days_ago)
        end_of_day = start_of_day + timedelta(hours=23)

        start_of_day_s = int(start_of_day.timestamp())
        end_of_day_s = int(end_of_day.timestamp())

        # Get the top trending topic for this day
        payload = {
            'woeid': world_woeid,
            'timestamp': start_of_day_s,
            'end_timestamp': end_of_day_s,
            'limit': '1'
        }
        r = requests.get(request_url, params=payload);
        topic = r.json()['trends'][0]['name']

        # Collect the topic, along with the related dates
        topics.append({
            'start_of_day': start_of_day,
            'end_of_day': end_of_day,
            'topic': topic
        })
        days_ago += 1

    return topics


# Use the Twitter API to get 100 tweets for this topic on those dates
def get_tweets(start_of_day_s, end_of_day_s, topic):
    payload = {
        'ie': 'UTF-8',
        'q': topic.encode('utf-8'),
        'perpage': 100,
        'type': 'tweet',
        'mintime': start_of_day_s,
        'maxtime': end_of_day_s,
        'apikey': TOPSY_API_KEY
    }
    res = requests.get(tweets_url, params=payload)

    # Need to do this because the response is wrapped in a <pre></pre> tag
    json_res = json.loads(res.text.replace('<pre>','',1).replace('</pre>','',1))

    # Extract just the tweet contents from the response
    tweets = [tweet['content'] for tweet in json_res['response']['list']]

    return tweets


# Return the full text for the 'chapter', which is just words_per_day's worth of
# words based on tweets from this topic for this day
def write_chapter(topic_info, words_per_day):
    start_of_day = topic_info['start_of_day']
    end_of_day = topic_info['end_of_day']
    topic = topic_info['topic']

    chapter = '****************************************\n'
    chapter_title = 'Dear diary: On ' + start_of_day.strftime('%b %d, %Y') + ', I thought about ' + topic + ':\n'
    chapter += chapter_title

    # Get the relevant tweets and build a chapter here
    start_of_day_s = int(start_of_day.timestamp())
    end_of_day_s = int(end_of_day.timestamp())
    tweets = get_tweets(start_of_day_s, end_of_day_s, topic)

    # Go through the tweets and collect word_per_day or more words
    word_count = 0
    tweet_number = 0
    for tweet in tweets:
        word_count += get_word_count(tweet)
        tweet_number += 1
        if word_count >= words_per_day:
            break

    chapter += '. '.join(tweets[:tweet_number])

    chapter += '\n****************************************\n\n'
    return chapter

def generate_novel(title, author, days, words_per_day):
    topics = get_topics(days)

    today_str = datetime.today().strftime('%b %d, %Y')
    novel_filename = title + ' (' + today_str + ')' + '.txt'
    with codecs.open(novel_filename, 'w', encoding='utf-8') as novel:
        novel.write(title + '\n')
        novel.write('By: ' + author + '\n')
        novel.write('Generated On: ' + today_str)
        novel.write('\n====================\n')

        for topic in topics:
            chapter = write_chapter(topic, words_per_day)
            novel.write(chapter)

        novel.write("The End.")

def main(argv):
    title = 'Novel'
    author = ''
    days = 30
    words = 50000
    try:
        opts, args = getopt.getopt(argv,'ht:a:d:w:',['title=','author=','days=','words='])
    except getopt.GetoptError:
        print('generate_novel.py -t <title> -a <author> -d <days> -w <words>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generate_novel.py -t <title> -a <author> -d <days> -w <words>')
            sys.exit()
        elif opt in ('-t', '--title'):
            title = arg
        elif opt in ('-a', '--author'):
            author = arg
        elif opt in ('-d', '--days'):
            days = int(arg)
            if days > 365:
                print('Please choose less than 365 days.')
                sys.exit()
        elif opt in ('-w', '--words'):
            words = int(arg)
            
            
    if not title:
        print('Please provide a title')
        sys.exit()
        
    if not author:
        print('Please provide an author')
        sys.exit()

    words_per_day = math.ceil(words // days)
    if words_per_day > 3000: # More or less arbitrarily chosen
        print('Too many tweets per day (' + str(words_per_day) + '). Please pick a smaller value of days or words in the novel.')
        sys.exit()

    print('Novel Title: ', title)
    print('Author: ', author)
    print('Days going back: ', days)
    print('Number of words: ', words)
    print('Words per day: ', words_per_day)


    generate_novel(title, author, days, words_per_day)

if __name__ == '__main__':
    with open('api_key.txt', 'r') as api_key:
        TOPSY_API_KEY = api_key.read()
    main(sys.argv[1:])
