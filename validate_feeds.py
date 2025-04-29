import json
import sys
import hashlib
import base64

FEEDS_FILE = "feeds.json"

def generate_uniqueid(url):
    sha256_hash = hashlib.sha256(url.encode('utf-8')).digest()
    base64_hash = base64.urlsafe_b64encode(sha256_hash).decode('utf-8').rstrip('=')
    return base64_hash

def validate_feeds(filepath):
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            feeds = json.load(f)
    except Exception as e:
        print(f"ERROR: Unable to read or parse {filepath}: {e}")
        sys.exit(1)

    if not isinstance(feeds, list):
        print(f"ERROR: {filepath} must contain a JSON array.")
        sys.exit(1)

    errors_found = False

    for idx, feed in enumerate(feeds):
        if not isinstance(feed, dict):
            print(f"ERROR: Entry {idx} is not a JSON object.")
            errors_found = True
            continue

        missing_fields = [field for field in ("source", "url", "uniqueid") if field not in feed]
        if missing_fields:
            print(f"ERROR: Entry {idx} missing fields: {', '.join(missing_fields)}")
            errors_found = True
            continue

        expected_uniqueid = generate_uniqueid(feed["url"])
        if feed["uniqueid"] != expected_uniqueid:
            print(f"ERROR: Entry {idx} ('{feed['source']}') has incorrect uniqueid. Expected: {expected_uniqueid}")
            errors_found = True

    if errors_found:
        print(f"❌ Validation failed for {filepath}. Please fix the above errors.")
        sys.exit(1)
    else:
        print(f"✅ {filepath} is valid.")

if __name__ == "__main__":
    validate_feeds(FEEDS_FILE)
