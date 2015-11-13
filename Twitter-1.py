
# coding: utf-8

# In[3]:

#Import necessary libraries
#import sense
import tweepy
import csv
import sys
import copy
from datetime import datetime


# In[7]:


#Twitter API - Credentials: Please create a Twitter APP and provide the credentials
# Author - Arnab Dutta
# October 2015

reload(sys)
sys.setdefaultencoding('utf-8')

# Create a twitter application on Developers Page and allow access.

access_token = ""
access_token_secret = ""
consumer_key = ""
consumer_secret = ""

# List of hashtags that you need to scrape
matchCode = ["#customerService #banking", "#technology #banking", "#banking #security"]

# Date range for filter
startDate = datetime.strptime("01/01/14 00:01", '%d/%m/%y %H:%M')
endDate   = datetime.strptime("12/11/15 23:59", '%d/%m/%y %H:%M')

outtweets = [] #initialize master list to hold our ready tweets
#List to capture the tweets
alltweets = []
alltweets_temp = []
rec_count = 0

# max number of tweets
tweet_max_limit = 10000

def get_all_tweets(screen_name, api):
        #Only most recent 3240 tweets are available with this method
        rec_count = 0
        outtweets = []
        alltweets = []
        alltweets_temp = []
        
        #Filter out the match code of the account for which the function is being run
        matchCodeTemp = copy.copy(matchCode)
        #matchCodeTemp.remove(screen_name)
        print (screen_name)
        waitflag = True
        waitnotifyflag =  True
 
        #make initial request for most recent tweets (200 is the maximum allowed count)
        #new_tweets = api.user_timeline(screen_name = screen_name,count=1)
        new_tweets = tweepy.Cursor(api.search, q=screen_name, wait_on_rate_limit = True, wait_on_rate_limit_notify=True).items(100)
        #print (dir(new_tweets))
    	
        #if len(list(new_tweets)) <= 0:
        #    print ("No Tweets for %s" %(screen_name))
        #    return
		
        alltweets_temp = list(new_tweets)
        alltweets.extend(alltweets_temp)
                
        #keep grabbing tweets until there are no tweets left to grab
        while len(alltweets_temp) > 0:
            oldest = alltweets[-1].id #oldest id retrieved
            print oldest #test print
            rec_count = len(alltweets)
            
            if (rec_count > tweet_max_limit):
                alltweets_temp = []
            else:
                new_tweets = tweepy.Cursor(api.search, q=screen_name,since_id=oldest, wait_on_rate_limit = waitflag, 
                                     wait_on_rate_limit_notify=waitnotifyflag).items(200)
                    #print (new_tweets) 
                    #save most recent tweets
                alltweets_temp = list(new_tweets)
                alltweets.extend(alltweets_temp)
          

        for tweet in alltweets:
            #createdDateTime = datetime.strptime(tweet.created_at, '%d/%m/%y %H:%M')
            createdDateTime = tweet.created_at
            print createdDateTime #test print 
            if (startDate <= createdDateTime <= endDate):
              #matchedTags = [tag for tag in matchCodeTemp if tag in tweet.text]
              #print (matchedTags)
              outtweets.append([screen_name, tweet.id, tweet.created_at, tweet.text,  tweet.retweet_count, 
                                tweet.favorite_count, tweet.user.name, tweet.user.location, tweet.user.screen_name, 
                                tweet.user.followers_count, tweet.user.description])
    
                    
          #oldest = outtweets[-1][1]
          
          #save the id of the oldest tweet less one 
            #print ("getting tweets after %s" % (oldest))
     
                    #all subsequent requests use the max_id param to prevent duplicates
                    #new_tweets = api.user_timeline(screen_name = screen_name,count=200,max_id=oldest)
          
          #print ("...%s tweets downloaded so far" % (len(list(alltweets))))
     
            #print (matchCodeTemp)
            #write the csv  
        with open('%s_tweets.csv' % screen_name, 'wt') as f:
                writer = csv.writer(f)
                writer.writerow(["Tag","ID", "Created_at","Tweet_Text", "Retweet_Count", "Favourites_Count", "User Name",
                                "Location", "User Screen-Name", "Followers Count", "User Profile Desc"])
                writer.writerows(outtweets)
 
        pass
        
if __name__ == '__main__':
        #pass in the username of the account you want to download
        #accounts = matchCode.copy()
        accounts = copy.copy(matchCode)
        #accounts.remove("#irdl")
        auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
        auth.set_access_token(access_token, access_token_secret)
        api = tweepy.API(auth)
        
                
        [get_all_tweets(account, api) for account in accounts]
        #get_all_tweets("@l_zilinski", api)

