#Diaries of the Internet: Twitter Novel Generator
A Python program that generates a 50,000 word novel using Twitter trending topics. It uses tt-history to get the worldwide top topic for each of the last 30 days and then uses the Twitter API to get enough tweets for each day from the corresponding topic to write a 50,000 word novel in the style of a diary.

##Commandline Arguments
-t --title  The title of the novel
-a --author The author of the novel
-d --days   How many days to go back for diary entries
-w --words  How many total words the novel should have

##Technical Details
The top topics of the day are pulled from [TT History](https://tt-history.appspot.com/), a website that keeps a history of trending topics on Twitter. The actual Tweet data is pulled from [Topsy](http://topsy.com/), since the regular Twitter API only provides data for the last week, and this project relies on having data for the past d days. A Topsy API key is required to run the generator yourself, and should be stored in a file called api_key.txt in the same directory as generate_novel.py.
