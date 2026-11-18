"""Print a collection from portal_data.json (no Firebase/Firestore required)."""
import argparse
import json
from portal_data import get_collection, get_document

parser = argparse.ArgumentParser(description="Read local DSAI portal data")
parser.add_argument("collection", nargs="?", default="courses", help="Collection name")
parser.add_argument("--document", help="Optional document ID, e.g. DSAI")
args = parser.parse_args()

if args.document:
    result = get_document(args.collection, args.document)
else:
    result = get_collection(args.collection)
print(json.dumps(result, indent=2, ensure_ascii=False))
