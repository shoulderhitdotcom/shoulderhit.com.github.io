import os
import json
import praw

FLAIR_ID = {
    "Japan": "9131d7e0-879c-11eb-8b3b-0e08ed08bdc9",
    "Europe": "8550c5a8-879c-11eb-a602-0eeed234ac3d",
    "North America": "8c805dca-879c-11eb-97b6-0e09cd9fd211",
    "China": "93bfe15a-879c-11eb-bab7-0ec71b25ae91",
    "Korea": "98381a72-879c-11eb-93e6-0e632d260907",
    "Taiwan": "9d3e8c0e-879c-11eb-93b2-0e52a3abedeb",
    "Rest of the world": "b0202120-879c-11eb-a7b4-0ecdeaf3c563",
    "Non-location specific": "ab4a3b30-879d-11eb-a7aa-0e99429f6b11",
    "International": "ee8b0328-8b5f-11eb-a60a-0e834a48c4f9"
    }

def submit_gallery(title, image_paths, flair_id=None):
    f = open("client_secrets.json", "r")
    cred = json.load(f)
    f.close()

    client_id = cred["client_id"]
    client_secret = cred["client_secret"]
    user_agent = cred["user_agent"]
    redirect_uri = cred["redirect_uri"]
    refresh_token = cred["refresh_token"]

    reddit = praw.Reddit(client_id=client_id, client_secret=client_secret,
                         user_agent=user_agent, redirect_uri=redirect_uri, refresh_token=refresh_token)

    subreddit = reddit.subreddit('proweiqi')
    images = [{'image_path': ip} for ip in image_paths]

    subreddit.submit_gallery(title=title, images=images, flair_id=flair_id)

def submit_gallery_by_folder(title, path):
    upload_files = [f for f in os.listdir(
        path) if os.path.splitext(f)[1] == ".peg"]
    image_paths = [os.path.join(path, f) for f in upload_files]
    submit_gallery(title, image_paths)