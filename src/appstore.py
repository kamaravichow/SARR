import os
import requests
import json
import requests, time, json
from authlib.jose import jwt
from utils import *

ISSUER_ID = os.environ.get("ASC_ISSUER_ID")
KEY_ID = os.environ.get("ASC_ADMIN_KEY_ID")
PRIVATE_KEY = os.environ.get("ASC_ADMIN_KEY")

EXPIRATION_TIME = int(round(time.time() + (20.0 * 60.0)))  # 20 minutes timestamp
header = {"alg": "ES256", "kid": KEY_ID, "typ": "JWT"}
payload = {"iss": ISSUER_ID, "exp": EXPIRATION_TIME, "aud": "appstoreconnect-v1"}
token = jwt.encode(header, payload, PRIVATE_KEY)  # Create the JWT


def get_appstore_instructions():
    instructions = open(f"./src/files/instructions-appstore.txt", "r").read()
    return instructions


def get_reviews(appId: str):
    # API Request
    JWT = "Bearer " + str(token.decode())
    HEAD = {"Authorization": JWT}
    response = requests.get(
        "https://api.appstoreconnect.apple.com/v1/apps/{id}/customerReviews".format(
            id=appId
        ),
        params={"limit": 100},
        headers=HEAD,
    )
    output_path = make_folder("./apps/{id}/reviews".format(id=appId))

    # print(response.status_code)
    # print(response.text)
    # save to json with name reviews.json
    with open(f"{output_path}/reviews.json", "w") as outfile:
        json.dump(response.json(), outfile, indent=4, sort_keys=True)

    return response.json()


def check_review_response(review_id: str):
    # https://api.appstoreconnect.apple.com/v1/customerReviews/{id}/response
    JWT = "Bearer " + str(token.decode())
    HEAD = {"Authorization": JWT}
    response = requests.get(
        "https://api.appstoreconnect.apple.com/v1/customerReviews/{id}/response".format(
            id=review_id
        ),
        headers=HEAD,
    )
    if response.status_code == 200:
        print(f"Customer review response found. : {response.json()}")
        return response.json()
    else:
        return None


def post_review(customer_review_id: str, response_text: str):
    JWT = "Bearer " + str(token.decode())
    HEAD = {"Authorization": JWT}
    # POST https://api.appstoreconnect.apple.com/v1/customerReviewResponses
    response = requests.post(
        "https://api.appstoreconnect.apple.com/v1/customerReviewResponses",
        json={
            "data": {
                "attributes": {
                    "responseBody": response_text,
                },
                "relationships": {
                    "review": {
                        "data": {
                            "id": customer_review_id,
                            "type": "customerReviews",
                        },
                    },
                },
                "type": "customerReviewResponses",
            }
        },
        headers=HEAD,
    )
    if response.status_code == 201:
        print("Customer review response created successfully.")
    else:
        print(response.status_code)
        print(response.text)
        print("Failed to create customer review response.")
    return ""
