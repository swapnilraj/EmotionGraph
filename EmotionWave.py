
import scrape
import scrapeFacebook
import multiprocessing as mp

def checkTweets(name, numberoftweets):
    scrape.analyzer(scrape.get_all_tweets(name, numberoftweets), name + " Twitter")

def twitter():
    checkTweets(raw_input("TwitterHandle:\n"), int(raw_input("Number of tweets:\n")))

def facebook():
    scrapeFacebook.scrapeUser(raw_input("FacebookName:"))
    
def checkExactTweets(name, numberoftweets):
    scrape.analyzer(scrape.get_all_tweets(name, numberoftweets), name + " Twitter")

def exactTwitter():
    checkExactTweets(raw_input("TwitterHandle:\n"), int(raw_input("Number of tweets:\n")))

if __name__ == "__main__":
    # twitter = raw_input("TwitterHandle:")
    # facebook = raw_input("FacebookName:")
    # thread1 = mp.Process(target = checkTweets, args = (twitter, ))
    # thread2 = mp.Process(target = scrapeFacebook.scrapeUser, args = (facebook, ))
    # thread1.start()
    # thread2.start()
    # thread1.join()
    # thread2.join()
    twitter()
