from .lib.replace_me import get, post, patch

from coinbase.rest import RESTClient
from dotenv import load_dotenv

load_dotenv()

db_host = os.getenv("DB_HOST")
db_name = os.getenv("DB_NAME")

api_key = "organizations/{org_id}/apiKeys/{key_id}"
api_secret = (
    "-----BEGIN EC PRIVATE KEY-----\nYOUR PRIVATE KEY\n-----END EC PRIVATE KEY-----\n"
)

client = RESTClient(api_key=api_key, api_secret=api_secret)


def main():
    print("Hello, world!")
