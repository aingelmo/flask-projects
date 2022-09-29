import os
from pathlib import Path

from dotenv import load_dotenv

env = load_dotenv()

PROJECT_DIR = Path(__file__).parents[0]
CREDS_DIR = f"{PROJECT_DIR}/bq-private-key.json"

GOOGLE_CLIENT_ID = os.environ.get("GOOGLE_CLIENT_ID", None)
GOOGLE_CLIENT_SECRET = os.environ.get("GOOGLE_CLIENT_SECRET", None)
GOOGLE_DISCOVERY_URL = os.environ.get("GOOGLE_DISCOVERY_URL", None)

OAUTHLIB_INSECURE_TRANSPORT = os.environ.get("OAUTHLIB_INSECURE_TRANSPORT", None)
OAUTHLIB_RELAX_TOKEN_SCOPE = os.environ.get("OAUTHLIB_RELAX_TOKEN_SCOPE", None)

DB_NAME = os.environ.get("DB_NAME", "str")
