import sys
import ssl
import os
import json
import httplib2
import openai

from oauth2client.service_account import ServiceAccountCredentials
from googleapiclient.discovery import build
from distutils.util import strtobool

ssl._create_default_https_context = ssl._create_unverified_context

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

ADMIN_JSON = os.getenv("PLAY_DEVELOPER_ADMIN_JSON")

credentials = ServiceAccountCredentials.from_json_keyfile_dict(
    json.loads(ADMIN_JSON),
    scopes=[
        "https://www.googleapis.com/auth/androidpublisher",
    ],
)

http = httplib2.Http()
http = credentials.authorize(http)
service = build("androidpublisher", "v3", http=http)
reviews_service = service.reviews()


def get_play_instructions():
    instructions = open(f"./src/files/instructions-playstore.txt", "r").read()
    return instructions


def post_reply(package_name, review_id, reply):
    print("Replying 💪🏻 to review: ", review_id)
    try:
        review_response = reviews_service.reply(
            packageName=package_name,
            reviewId=review_id,
            body={"replyText": reply},
        ).execute()
        print("Replied ✅ to review: ", review_response)
        return review_response
    except Exception as e:
        print("Error: ", e)
        return None


def load_reviews(package, max_results=100, start_index=0):
    try:
        reviews_page = reviews_service.list(
            packageName=package,
            maxResults=max_results,
            startIndex=start_index,
        ).execute()
        return reviews_page["reviews"]
    except Exception as e:
        print("Error: loading ", e)
        return []
