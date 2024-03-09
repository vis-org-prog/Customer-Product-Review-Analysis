import os
from google.cloud import language_v1
from google.cloud import texttospeech
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

# Function to convert text to speech
def text_to_speech(text, output_file):
    client = texttospeech.TextToSpeechClient()
    synthesis_input = texttospeech.SynthesisInput(text=text)
    voice = texttospeech.VoiceSelectionParams(
        language_code="en-US", ssml_gender=texttospeech.SsmlVoiceGender.NEUTRAL
    )
    audio_config = texttospeech.AudioConfig(
        audio_encoding=texttospeech.AudioEncoding.MP3
    )
    response = client.synthesize_speech(
        input=synthesis_input, voice=voice, audio_config=audio_config
    )
    with open(output_file, "wb") as out:
        out.write(response.audio_content)
        print(f'Audio content written to file "{output_file}"')
    return output_file

# Function to create the sentiment_data table
def create_table():
    connection = mysql.connector.connect(host='localhost',
                                         database='admn5015',
                                         user='admn5015',
                                         password='Vishnu22@1997')
    cursor = connection.cursor()
    cursor.execute("""
        CREATE TABLE IF NOT EXISTS sentiment_data (
            id INT AUTO_INCREMENT PRIMARY KEY,
            review TEXT,
            sentiment_score FLOAT,
            sentiment_magnitude FLOAT,
            audio_file VARCHAR(255)
        )
    """)
    connection.commit()
    print("Table created successfully.")

# Function to insert sentiment analysis results and audio filenames into MySQL database
def insert_sentiment_data(review, score, magnitude, audio_file):
    connection = mysql.connector.connect(host='localhost',
                                         database='admn5015',
                                         user='admn5015',
                                         password='Vishnu22@1997')
    cursor = connection.cursor()
    sql = "INSERT INTO sentiment_data (review, sentiment_score, sentiment_magnitude, audio_file) VALUES (%s, %s, %s, %s)"
    val = (review, score, magnitude, audio_file)
    cursor.execute(sql, val)
    connection.commit()
    print(cursor.rowcount, "record inserted.")

# Example usage:
create_table()

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

for i, review in enumerate(reviews):
    sentiment_scores, sentiment_magnitudes = analyze_reviews([review])
    audio_file = text_to_speech(review, f"review_{i+1}.mp3")
    insert_sentiment_data(review, sentiment_scores[0], sentiment_magnitudes[0], audio_file)
