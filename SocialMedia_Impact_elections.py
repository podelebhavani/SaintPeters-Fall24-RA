#!/usr/bin/env python
# coding: utf-8

# In[1]:


import praw
import json
import pandas as pd

# Custom function to convert Submission to a dictionary
def submission_to_dict(submission):
    # Extract attributes from the Submission object
    submission_dict = {
        'id': submission.id,
        'title': submission.title,
        'url': submission.url,
        'selftext': submission.selftext,
        'score': submission.score,
        'num_comments': submission.num_comments,
        'author': str(submission.author),  
        'subreddit': str(submission.subreddit),  
        'created_utc': submission.created_utc,  
        'upvote_ratio': submission.upvote_ratio,
        'permalink': submission.permalink,
        'stickied': submission.stickied
    }
    
    return submission_dict

# Authentication using your credentials
def auth_reddit():
    reddit = praw.Reddit(
        client_id='4SNi9OCfmygMxklDWCcwEA',
        client_secret='8jl8xBSblGSkiBqE-zD3S7X1vSQB1w',
        user_agent='Far_Yesterday_2201'
    )
    return reddit

# Specify the subreddit you want to fetch from
def speficy_subreddit(reddit, keyword):
    subreddit = reddit.subreddit(keyword)
    search_post_results = subreddit.search(
        keyword, 
        sort='top', 
        time_filter='week', 
        limit=2
    )
    return search_post_results


def process_search_results(search_post_results):
    submission_json_list = []

    for post in search_post_results:
        # Convert the submission to a dictionary
        submission_data = submission_to_dict(post)
        submission_json_list.append(submission_data)

    submission_json = json.dumps(submission_json_list, indent=4)
    #print(submission_json)
    return submission_json

def output_to_csv(submission_json):
    data = json.loads(submission_json)

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv('/Users/bhanupodele/Downloads/dataverse_files/Reddit_output.csv', index='id')

def main():
    reddit = auth_reddit()
    search_post_results = speficy_subreddit(reddit, 'Kamala')
    submission_json = process_search_results(search_post_results)
    output_to_csv(submission_json)

main()


# In[3]:


import praw
import json
import pandas as pd
from datetime import datetime, timedelta

# Custom function to convert Submission to a dictionary
def submission_to_dict(submission):
    submission_dict = {
        'id': submission.id,
        'title': submission.title,
        'url': submission.url,
        'selftext': submission.selftext,
        'score': submission.score,
        'num_comments': submission.num_comments,
        'author': str(submission.author),  
        'subreddit': str(submission.subreddit),  
        'created_utc': submission.created_utc,  
        'upvote_ratio': submission.upvote_ratio,
        'permalink': submission.permalink,
        'stickied': submission.stickied
    }
    
    return submission_dict

# Authentication using your credentials
def auth_reddit():
    reddit = praw.Reddit(
        client_id='4SNi9OCfmygMxklDWCcwEA',
        client_secret='8jl8xBSblGSkiBqE-zD3S7X1vSQB1w',
        user_agent='Far_Yesterday_2201'
    )
    return reddit

# Function to filter posts from the last 2 years
def filter_posts_by_date(post, years=2):
    # Convert submission's created_utc to datetime object
    post_date = datetime.utcfromtimestamp(post.created_utc)
    
    # Get the date 2 years ago from today
    two_years_ago = datetime.utcnow() - timedelta(days=years*365)
    
    # Return True if the post is within the last 2 years
    return post_date >= two_years_ago

# Specify the subreddits and search terms
def search_subreddit_posts(reddit, keyword):
    # Specify subreddits to search in
    subreddits = ['politics', 'news', 'worldnews', 'election2024']
    
    all_posts = []
    
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        search_results = subreddit.search(
            keyword, 
            sort='top', 
            time_filter='all',  # Fetch posts from all time
            limit=1000           # Adjust the limit as needed
        )
        
        for post in search_results:
            if filter_posts_by_date(post, years=2):  # Check if post is from the last 2 years
                submission_data = submission_to_dict(post)
                all_posts.append(submission_data)

    return all_posts

# Process search results and convert to JSON
def process_search_results(posts):
    submission_json = json.dumps(posts, indent=4)
    return submission_json

# Output to CSV
def output_to_csv(submission_json):
    data = json.loads(submission_json)

    # Create a DataFrame from the JSON data
    df = pd.DataFrame(data)

    # Save DataFrame to CSV
    df.to_csv('/Users/bhanupodele/Downloads/dataverse_files/Reddit_election_posts_last_2_years.csv', index=False)

def main():
    reddit = auth_reddit()
    
    # Search for posts with 'election' as the keyword across the specified subreddits
    posts = search_subreddit_posts(reddit, 'election')
    
    # Convert the list of posts to JSON
    submission_json = process_search_results(posts)
    
    # Output the results to CSV
    output_to_csv(submission_json)

main()


# In[5]:


import praw
import json
import pandas as pd
from datetime import datetime, timedelta
import time

# Custom function to convert Submission to a dictionary
def submission_to_dict(submission):
    submission_dict = {
        'id': submission.id,
        'title': submission.title,
        'url': submission.url,
        'selftext': submission.selftext,
        'score': submission.score,
        'num_comments': submission.num_comments,
        'author': str(submission.author),  
        'subreddit': str(submission.subreddit),  
        'created_utc': submission.created_utc,  
        'upvote_ratio': submission.upvote_ratio,
        'permalink': submission.permalink,
        'stickied': submission.stickied
    }
    return submission_dict

# Authentication using your credentials
def auth_reddit():
    reddit = praw.Reddit(
        client_id='4SNi9OCfmygMxklDWCcwEA',
        client_secret='8jl8xBSblGSkiBqE-zD3S7X1vSQB1w',
        user_agent='Far_Yesterday_2201'
    )
    return reddit

# Function to filter posts from the last 2 years
def filter_posts_by_date(post, years=2):
    post_date = datetime.utcfromtimestamp(post.created_utc)
    two_years_ago = datetime.utcnow() - timedelta(days=years*365)
    return post_date >= two_years_ago

# Specify the subreddits and keywords
def search_subreddit_posts(reddit, subreddits, keywords):
    all_posts = []
    for subreddit_name in subreddits:
        subreddit = reddit.subreddit(subreddit_name)
        for keyword in keywords:
            try:
                search_results = subreddit.search(
                    keyword, 
                    sort='top', 
                    time_filter='all',  # Fetch posts from all time, will manually filter for 2 years
                    limit=1000           # Adjust the limit as needed
                )
                
                for post in search_results:
                    if filter_posts_by_date(post, years=2):  # Filter posts within the last 2 years
                        submission_data = submission_to_dict(post)
                        all_posts.append(submission_data)
                
                # Introduce a small delay to avoid hitting API rate limits
                time.sleep(2)
            except Exception as e:
                print(f"Error fetching data for {keyword} in {subreddit_name}: {e}")
    
    return all_posts

# Process search results and convert to JSON
def process_search_results(posts):
    submission_json = json.dumps(posts, indent=4)
    return submission_json

# Output to CSV
def output_to_csv(submission_json, filename):
    data = json.loads(submission_json)
    df = pd.DataFrame(data)
    df.to_csv(filename, index=False)

def main():
    reddit = auth_reddit()
    
    # Define the subreddits to search in and the keywords to use
    subreddits = ['politics', 'news', 'worldnews', 'election2024', 'conservative', 'liberal']
    keywords = ['election', 'voting', 'presidential race', 'midterms', 'campaign', 'debate', 'polls', 'ballot', 'candidates']
    
    # Search for posts across subreddits and keywords
    posts = search_subreddit_posts(reddit, subreddits, keywords)
    
    # Convert the list of posts to JSON
    submission_json = process_search_results(posts)
    
    # Output the results to CSV
    output_to_csv(submission_json, '/Users/bhanupodele/Downloads/dataverse_files/Reddit_enlarged_election_posts.csv')

main()


# In[6]:


import pandas as pd

# Load the dataset
file_path = '/Users/bhanupodele/Downloads/dataverse_files/Reddit_enlarged_election_posts.csv'
reddit_data = pd.read_csv(file_path)

# Inspect the first few rows of the data
print(reddit_data.head())

# Check for missing values and basic statistics
print(reddit_data.info())
print(reddit_data.describe())


# In[7]:


# Convert 'created_utc' to a readable datetime format
reddit_data['created_utc'] = pd.to_datetime(reddit_data['created_utc'], unit='s')

# Verify the conversion
print(reddit_data[['created_utc']].head())


# In[8]:


# Drop rows where 'title', 'created_utc', or 'score' are missing
reddit_data_clean = reddit_data.dropna(subset=['title', 'created_utc', 'score'])

# Fill missing 'selftext' values with empty strings
reddit_data_clean['selftext'].fillna("", inplace=True)

# Verify the cleaning
print(reddit_data_clean.isnull().sum())


# In[9]:


from textblob import TextBlob

# Function to calculate sentiment polarity (-1 to 1) using TextBlob
def get_sentiment(text):
    return TextBlob(text).sentiment.polarity

# Apply sentiment analysis to 'title' and 'selftext'
reddit_data_clean['title_sentiment'] = reddit_data_clean['title'].apply(get_sentiment)
reddit_data_clean['selftext_sentiment'] = reddit_data_clean['selftext'].apply(get_sentiment)

# Inspect the sentiment results
print(reddit_data_clean[['title', 'title_sentiment', 'selftext_sentiment']].head())


# In[10]:


# Top 10 posts by score
top_posts_by_score = reddit_data_clean.nlargest(10, 'score')
print(top_posts_by_score[['title', 'score', 'num_comments']])

# Top 10 posts by number of comments
top_posts_by_comments = reddit_data_clean.nlargest(10, 'num_comments')
print(top_posts_by_comments[['title', 'score', 'num_comments']])


# In[11]:


import matplotlib.pyplot as plt

# Create a 'month' column from 'created_utc'
reddit_data_clean['month'] = reddit_data_clean['created_utc'].dt.to_period('M')

# Group by month and calculate the average score, comments, and number of posts
monthly_engagement = reddit_data_clean.groupby('month').agg({
    'score': 'mean',
    'num_comments': 'mean',
    'id': 'count'
}).rename(columns={'id': 'num_posts'})

# Plot the monthly trends for posts, score, and comments
plt.figure(figsize=(10, 6))
monthly_engagement['num_posts'].plot(kind='line', label='Number of Posts', color='blue')
monthly_engagement['score'].plot(kind='line', label='Average Score', color='green')
monthly_engagement['num_comments'].plot(kind='line', label='Average Comments', color='red')
plt.title('Monthly Engagement on Election-Related Posts')
plt.xlabel('Month')
plt.ylabel('Engagement')
plt.legend()
plt.grid(True)
plt.show()


# In[12]:


# Group by subreddit to compare average score and comments
subreddit_engagement = reddit_data_clean.groupby('subreddit').agg({
    'score': 'mean',
    'num_comments': 'mean',
    'id': 'count'
}).rename(columns={'id': 'num_posts'}).sort_values(by='num_posts', ascending=False)

# Display the top 10 subreddits by number of posts
print(subreddit_engagement.head(10))


# In[13]:


# Scatter plot: Title sentiment vs. score
plt.figure(figsize=(10, 6))
plt.scatter(reddit_data_clean['title_sentiment'], reddit_data_clean['score'], alpha=0.5)
plt.title('Title Sentiment vs. Score')
plt.xlabel('Sentiment')
plt.ylabel('Score')
plt.grid(True)
plt.show()

# Scatter plot: Title sentiment vs. number of comments
plt.figure(figsize=(10, 6))
plt.scatter(reddit_data_clean['title_sentiment'], reddit_data_clean['num_comments'], alpha=0.5, color='red')
plt.title('Title Sentiment vs. Number of Comments')
plt.xlabel('Sentiment')
plt.ylabel('Number of Comments')
plt.grid(True)
plt.show()


# In[ ]:




