#!/usr/bin/python

import sys, getopt
import requests


def generate_novel(title, days, words):
    pass


def main(argv):
    title = ''
    days = 30
    words = 50000
    try:
        opts, args = getopt.getopt(argv,"ht:d:w:",["title=","days=","words="])
    except getopt.GetoptError:
        print('generate_novel.py -t <title> -d <days> -w <words>')
        sys.exit(2)
    for opt, arg in opts:
        if opt == '-h':
            print('generate_novel.py -t <title> -d <days> -w <words>')
            sys.exit()
        elif opt in ("-t", "--title"):
            title = arg
        elif opt in ("-d", "--days"):
            days = int(arg)
            if days > 365:
                print("Please choose less than 365 days.")
                sys.exit()
        elif opt in ("-w", "--words"):
            words = int(arg)

    words_per_day = words//days
    if words_per_day > 3000: # More or less arbitrarily chosen
        print("Too many tweets per day (" + str(words_per_day) + "). Please pick a smaller value of days or words in the novel.")
        sys.exit()

    print('Novel Title: ', title)
    print('Days going back: ', days)
    print('Number of words: ', words)
    print('Words per day: ', words_per_day)


    generate_novel(title, days, words)

if __name__ == "__main__":
   main(sys.argv[1:])