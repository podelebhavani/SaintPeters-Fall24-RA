import praw
import csv
import time
import os
from datetime import datetime, timezone
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Access environment variables
client_id = os.getenv("client_id")
client_secret = os.getenv("client_secret")
user_agent = os.getenv("user_agent")

print(client_secret)

# Reddit API credentials
reddit = praw.Reddit(
    client_id=client_id,
    client_secret=client_secret,
    user_agent=user_agent
)

# Function to pull Reddit posts and save to CSV in batches
def fetch_reddit_data_by_sub_query(
        subreddit_name, 
        search_query, 
        output_file, 
        total_posts, 
        batch_size=100
):
    subreddit = reddit.subreddit(subreddit_name)
    after = None  # Keeps track of pagination
    posts_fetched = 0  # Counter for total posts fetched
    retrieved_ids = set()
    
    # Check if the file already exists to handle appending
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=[
                'id',
                'title',
                'url',
                'selftext',
                'score',
                'num_comments',
                'author',  
                'subreddit',  
                'created_utc',  
                'upvote_ratio',
                'permalink',
                'stickied'
            ]
        )
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()

        while posts_fetched < total_posts:
            # Fetch data from Reddit using subreddit.search()
            search_results = subreddit.search(
                search_query, 
                sort='new', 
                limit=batch_size, 
                params={
                    'after': after
                }
            )

            batch_posts = []
            for submission in search_results:

                if submission.id not in retrieved_ids:
                    retrieved_ids.add(submission.id)
                    batch_posts.append({
                        'id': submission.id,
                        'title': submission.title,
                        'url': submission.url,
                        'selftext': submission.selftext,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'author': str(submission.author),  
                        'subreddit': str(submission.subreddit),  
                        'created_utc': str(datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)),  
                        'upvote_ratio': submission.upvote_ratio,
                        'permalink': submission.permalink,
                        'stickied': submission.stickied
                    })

            if batch_posts:
                # Write the batch to the CSV file
                writer.writerows(batch_posts)
                
                # Update post counter and last fetched post ID (for pagination)
                posts_fetched += len(batch_posts)

                if batch_posts:
                    after = f't3_{batch_posts[-1]["id"]}'
                
                print(f"Fetched {posts_fetched}/{total_posts} posts")
            else:
                print("No more posts found.")
                break
            
            # Respect Reddit's rate limits (sleep for 2 seconds between batches)
            time.sleep(2)

    print(f"Total posts fetched and saved: {posts_fetched}")

# Function to pull Reddit posts and save to CSV
def fetch_reddit_data_by_sub(
        subreddit_name, 
        output_file, 
        total_posts
):
    subreddit = reddit.subreddit(subreddit_name)
    posts_fetched = 0  # Counter for total posts fetched
    retrieved_ids = set()
    
    # Check if the file already exists to handle appending
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=[
                'id',
                'title',
                'url',
                'selftext',
                'score',
                'num_comments',
                'author',  
                'subreddit',  
                'created_utc',  
                'upvote_ratio',
                'permalink',
                'stickied'
            ]
        )
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()

        for submission in subreddit.new(limit=None):
            if posts_fetched >= total_posts:
                break

            if submission.id not in retrieved_ids:
                retrieved_ids.add(submission.id)
                writer.writerow({
                    'id': submission.id,
                    'title': submission.title,
                    'url': submission.url,
                    'selftext': submission.selftext,
                    'score': submission.score,
                    'num_comments': submission.num_comments,
                    'author': str(submission.author),  
                    'subreddit': str(submission.subreddit),  
                    'created_utc': str(datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)),  
                    'upvote_ratio': submission.upvote_ratio,
                    'permalink': submission.permalink,
                    'stickied': submission.stickied
                })
                posts_fetched += 1
                print(f"Fetched {posts_fetched}/{total_posts} posts")
            
            # Respect Reddit's rate limits (sleep for 2 seconds between batches)
            time.sleep(2)

    print(f"Total posts fetched and saved: {posts_fetched}")


# Function to pull Reddit posts and save to CSV
def fetch_reddit_data_by_time(
        subreddit_name, 
        output_file, 
        total_posts,
        start_time,
        end_time
):
    subreddit = reddit.subreddit(subreddit_name)
    posts_fetched = 0
    retrieved_ids = set()
    
    # Check if the file already exists to handle appending
    file_exists = os.path.isfile(output_file)

    with open(output_file, mode='a', newline='', encoding='utf-8') as file:
        writer = csv.DictWriter(
            file, 
            fieldnames=[
                'id',
                'title',
                'url',
                'selftext',
                'score',
                'num_comments',
                'author',  
                'subreddit',  
                'created_utc',  
                'upvote_ratio',
                'permalink',
                'stickied'
            ]
        )
        
        # Write header if file doesn't exist
        if not file_exists:
            writer.writeheader()

        for submission in subreddit.new(limit=None):
            if posts_fetched >= total_posts:
                break
            
            if start_time <= submission.created_utc <= end_time:
                if submission.id not in retrieved_ids:
                    retrieved_ids.add(submission.id)
                    writer.writerow({
                        'id': submission.id,
                        'title': submission.title,
                        'url': submission.url,
                        'selftext': submission.selftext,
                        'score': submission.score,
                        'num_comments': submission.num_comments,
                        'author': str(submission.author),  
                        'subreddit': str(submission.subreddit),  
                        'created_utc': str(datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)),  
                        'upvote_ratio': submission.upvote_ratio,
                        'permalink': submission.permalink,
                        'stickied': submission.stickied
                    })
                    posts_fetched += 1
                    print(f"Fetched {posts_fetched}/{total_posts} posts")
                
            # Respect Reddit's rate limits (sleep for 2 seconds between batches)
            time.sleep(2)

    print(f"Total posts fetched and saved: {posts_fetched}")


# Parameters for subreddit, search term, and output
subreddit_name = 'Trump' # Search within a subreddit
search_query = 'Trump' # contain key words
output_file = './Data/raw_1021/subreddit_politics.csv'  # Output CSV file
total_posts = 10000 # Total number to pull

# Fetch 10,000 posts
#fetch_reddit_data_by_sub_query(subreddit_name=subreddit_name, search_query=search_query, output_file=output_file, total_posts=total_posts)

# fetch_reddit_data_by_sub(subreddit_name=subreddit_name, output_file=output_file, total_posts=total_posts)
# Subreddit: politics, democrats, Republican, PoliticalDiscussion

# start_time = datetime(2024, 10, 10).timestamp()
# end_time = datetime(2024, 10, 20).timestamp()
# fetch_reddit_data_by_time(
#     subreddit_name='politics', 
#     output_file=output_file, 
#     total_posts=total_posts, 
#     start_time=start_time, 
#     end_time=end_time
# )