import os
from google.cloud import texttospeech

# Set the environment variable to point to your service account key file
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

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

for i, review in enumerate(reviews):
    output_file = f"review_{i+1}.mp3"
    text_to_speech(review, output_file)
