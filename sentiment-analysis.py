import os
from google.cloud import language_v1
import mysql.connector

# Set the environment variable to point to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# Function to perform sentiment analysis on multiple reviews
def analyze_reviews(reviews):
    client = language_v1.LanguageServiceClient(credentials=None)
    sentiment_scores = []
    sentiment_magnitudes = []
    for review in reviews:
        document = language_v1.Document(content=review, type_=language_v1.Document.Type.PLAIN_TEXT)
        response = client.analyze_sentiment(request={'document': document})
        sentiment_score = response.document_sentiment.score
        sentiment_magnitude = response.document_sentiment.magnitude
        sentiment_scores.append(sentiment_score)
        sentiment_magnitudes.append(sentiment_magnitude)
    return sentiment_scores, sentiment_magnitudes

# Example usage:
reviews = [
    "This product exceeded my expectations! It's fantastic!",
    "I love this product. It's perfect for my needs.",
    "Outstanding quality and great value for the price.",
    "I'm very disappointed with this product. It broke after just one use.",
    "Poor quality. Not worth the money.",
    "Terrible experience. The product didn't work as advertised.",
    "I regret buying this product. It's a waste of money.",
    "The product is okay. It works as expected.",
    "Decent product. Not bad, but not exceptional either."
]

sentiment_scores, sentiment_magnitudes = analyze_reviews(reviews)

for i, review in enumerate(reviews):
    print("Review:", review)
    print("Sentiment Score:", sentiment_scores[i])
    print("Sentiment Magnitude:", sentiment_magnitudes[i])
    print()
