import os
import random
import requests
import openai
import tweepy
from solana.rpc.api import Client
from solana.transaction import Transaction
from solana.account import Account
from spl.token.client import Token
from solana.publickey import PublicKey
from solana.keypair import Keypair
import base64
import json

# Load environment variables
openai.api_key = os.getenv("OPENAI_API_KEY")

TWITTER_CONSUMER_KEY = os.getenv("API_KEY")
TWITTER_CONSUMER_SECRET = os.getenv("API_KEY_SECRET")
TWITTER_ACCESS_TOKEN = os.getenv("ACCESS_TOKEN")
TWITTER_ACCESS_SECRET = os.getenv("ACCESS_TOKEN_SECRET")
SOLANA_KEYPAIR = os.getenv("SOLANA_KEYPAIR")

# === Twitter Auth ===
auth = tweepy.OAuth1UserHandler(
    TWITTER_CONSUMER_KEY, TWITTER_CONSUMER_SECRET,
    TWITTER_ACCESS_TOKEN, TWITTER_ACCESS_SECRET
)
twitter_api = tweepy.API(auth)

# === Meme Generator ===
def generate_meme_caption():
    prompt = "Generate a funny meme caption for a Solana-based meme coin called Krazezo."
    response = openai.Completion.create(
        model="text-davinci-003",
        prompt=prompt,
        max_tokens=60,
        temperature=0.8,
    )
    return response.choices[0].text.strip()

# === SPL Token Mint ===
def mint_token():
    decoded = json.loads(base64.b64decode(SOLANA_KEYPAIR))
    keypair = Keypair.from_secret_key(bytes(decoded))
    client = Client("https://api.mainnet-beta.solana.com")

    token = Token.create_mint(
        client,
        payer=keypair,
        mint_authority=keypair.public_key,
        decimals=9,
        program_id=Token.SPL_TOKEN_PROGRAM_ID,
    )

    print(f"Token minted: {token.pubkey}")
    return token.pubkey

# === Tweet Function ===
def tweet_meme(caption):
    hashtags = "#Solana #Crypto #MemeCoin #Krazezo"
    twitter_api.update_status(f"{caption} 🚀\n{hashtags}")

# === MAIN EXECUTION ===
if __name__ == "__main__":
    meme = generate_meme_caption()
    tweet_meme(meme)
    print("Meme tweeted.")

    # Optional: Uncomment to mint on first run
    # token = mint_token()
