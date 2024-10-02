import praw
import json
import pandas as pd
from datetime import datetime, timezone

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
        'created_utc': str(datetime.fromtimestamp(submission.created_utc, tz=timezone.utc)),  
        'upvote_ratio': submission.upvote_ratio,
        'permalink': submission.permalink,
        'stickied': submission.stickied
    }
    
    return submission_dict

# Authentication using your credentials
def auth_reddit():
    reddit = praw.Reddit(
        client_id='RuuhB65fi--czOJWAz5ndA',
        client_secret='kqVMfGyIxtLnuKBoiabaXQWgtAzzUg',
        user_agent='ChenZhouRedditApp/0.1'
    )
    return reddit

# Specify the subreddit you want to fetch from
def speficy_subreddit(reddit, keyword):
    subreddit = reddit.subreddit(keyword)
    search_post_results = subreddit.search(
        keyword, 
        sort='new', 
        time_filter='all', 
        limit=1000
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
    df.to_csv('./Data/chenzhou_reddit_output_1002_Trump.csv', index='id')

def main():
    reddit = auth_reddit()
    search_post_results = speficy_subreddit(reddit, 'Trump')
    submission_json = process_search_results(search_post_results)
    output_to_csv(submission_json)

main()
