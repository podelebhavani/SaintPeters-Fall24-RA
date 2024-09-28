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
        client_id='',
        client_secret='',
        user_agent=''
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
    df.to_csv('./Data/chenzhou_reddit_output.csv', index='id')

def main():
    reddit = auth_reddit()
    search_post_results = speficy_subreddit(reddit, 'Kamala')
    submission_json = process_search_results(search_post_results)
    output_to_csv(submission_json)

main()
