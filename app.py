import os
import json

from datetime import datetime

from src.openai import get_ai_response
from src.playstore import load_reviews, post_reply, get_play_instructions
from src.appstore import (
    get_reviews,
    post_review,
    get_appstore_instructions,
    check_review_response,
)
from utils import *

# from dotenv import load_dotenv, find_dotenv
# load_dotenv(find_dotenv())

print("==== Starting SAAR 🤖 ====")
print("Let's get to work, hmm what new reviews do we have today ?")

# load apps from apps.json
apps = json.load(open("./apps.json", "r"))
total_app_count = len(apps)

print(f"Oh, we have {total_app_count} apps to check for today.")


def loadReviewsFromPlayStore(package, path):
    print("Let me see the reviews for the app: ", package)
    timestamp = datetime.now()
    # make reviews folder
    rv_folder = make_folder(f"{path}/reviews")

    # load from files if exists
    if os.path.exists(f"{rv_folder}/reviews.json"):
        cache = json.load(open(f"{rv_folder}/reviews.json", "r"))
        response_time = datetime.strptime(cache["timestamp"], "%d/%m/%Y %H:%M:%S")
        if (timestamp - response_time).seconds < 60 * 60:
            response = cache["reviews"]
            return response

    response = load_reviews(package, max_results=100, start_index=0)
    total_review_count = len(response)
    print(
        f"Yo, we have {total_review_count} on this app... Let check for unreplied ones"
    )

    # save response to file
    open(f"{rv_folder}/reviews.json", "w").write(
        json.dumps(
            {
                "timestamp": timestamp.strftime("%d/%m/%Y %H:%M:%S"),
                "reviews": response,
            },
            indent=2,
        )
    )
    return response


def main():
    for app in apps:
        package = app["id"]  # id is package name and appid
        store = app["store"]
        app_name = app["name"]
        summary = app["summary"]
        folder = make_folder(f"apps/{package}")

        if store == "play":
            reviews = loadReviewsFromPlayStore(package, folder)
            instruction = get_play_instructions()

            for review in reviews:
                # check if already replied
                comments_count = len(review["comments"])
                if comments_count > 1:
                    rew_id = review["reviewId"]
                    print(f"I Already replied to this review, skippin it - {rew_id}")
                    # continue

                name = review["authorName"]
                reviewId = review["reviewId"]
                starRating = review["comments"][0]["userComment"]["starRating"]
                comment_text = review["comments"][0]["userComment"]["text"]
                print(f"Review: {reviewId} \n\nRating: {starRating} / 5 stars\n\n")
                text = f"Name: {name},\n\n\n{comment_text} \n\n\nRating: {starRating} / 5 stars\n\n\n"
                print(text)
                parsed = instruction.replace("[INPUT]", text)
                response = get_ai_response(
                    prompt=parsed,
                    max_tokens=160,
                    store="Google Play Store",
                )
                print("Reply: ", response)
                response = response.replace("[Your Name]", "Aravind Chowdary")
                reply = post_reply(
                    package,
                    reviewId,
                    response,
                )
            print(f"I've finished replying to all reviews for the {app_name}")
            print("Sayonara 👋🏻 ")
            # App Store ================================
        elif store == "apple":
            print("App Store === App Name: ", app_name)

            reviews = get_reviews(package)["data"]
            instruction = get_appstore_instructions()

            for review in reviews:
                rat_id = review["id"]
                rat_title = review["attributes"]["title"]
                rat_text = review["attributes"]["body"]
                rat_rating = review["attributes"]["rating"]
                rat_name = review["attributes"]["reviewerNickname"]

                # print(f"Review: {rat_text} \n\nRating: {rat_rating} / 5 stars\n\n")
                # print("Oh a new review, let me reply to it... 🤖")

                # check if already replied
                if check_review_response(rat_id) != None:
                    print("Skipping... Already replied to this review - " + rat_id)
                    continue

                formatted_review = f"Name: {rat_name},\n\n\n {rat_title}, {rat_text} \n\n\nRating: {rat_rating} / 5 stars\n\n\n"
                prompt = instruction.replace("[INPUT]", formatted_review)
                response = get_ai_response(prompt)
                print(f"Reply: {response} \n\n ---")
                print(
                    f"replying this review.... 🥳, here is my reply \n\n\n {rat_name}\n\n---"
                )
                post_review(rat_id, response)
                print("Replied to review: ", rat_id)

            print(f"Done replying to all reviews for {app_name}, Sayonara 👋🏻 ")
        else:
            print("Store not supported yet.")
            continue


main()
