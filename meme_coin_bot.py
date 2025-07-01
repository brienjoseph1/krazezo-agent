import os
import openai
import tweepy
import logging

# Setup logging
logging.basicConfig(level=logging.INFO)

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

twitter_auth = tweepy.OAuth1UserHandler(
    os.getenv("API_KEY"),
    os.getenv("API_KEY_SECRET"),
    os.getenv("ACCESS_TOKEN"),
    os.getenv("ACCESS_TOKEN_SECRET")
)
twitter_api = tweepy.API(twitter_auth)

# === Generate meme caption ===
def generate_meme_caption():
    prompt = "Create a funny meme caption about a Solana meme coin called Krazezo."
    try:
        response = openai.Completion.create(
            model="text-davinci-003",
            prompt=prompt,
            max_tokens=60,
            temperature=0.9,
        )
        caption = response.choices[0].text.strip()
        logging.info(f"Generated meme caption: {caption}")
        return caption
    except Exception as e:
        logging.error(f"OpenAI error: {e}")
        return "Buy $KZ. It's not financial advice, it's destiny. 🚀"

# === Post to Twitter ===
def post_to_twitter(text):
    try:
        twitter_api.update_status(f"{text} #Krazezo #Solana #MemeCoin")
        logging.info("Tweet posted successfully.")
    except Exception as e:
        logging.error(f"Twitter error: {e}")

# === Optional: Mint token (placeholder) ===
def mint_token():
    logging.info("Minting logic placeholder — skipped for now.")
    # from solana.rpc.api import Client
    # from solana.keypair import Keypair
    # client = Client("https://api.mainnet-beta.solana.com")
    # ... (handle mint logic here)

# === Main ===
if __name__ == "__main__":
    caption = generate_meme_caption()
    post_to_twitter(caption)
    # mint_token()
