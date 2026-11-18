# DSAI Information Portal (local JSON build)

The portal's Firestore collections have been migrated into `portal_data.json` using the user-provided export. The rule-based chatbot logic and existing page structure are retained.

## Imported records
- Faculty: 8
- DSAI course/syllabus document: 1
- Events: 3
- Placement information documents: 2
- Timetables: 3
- Sessions: 4
- Admin information documents: 3
- Co-curricular activities: 4
- Library books: 62 (retained from the existing local catalogue)

## Setup
```bash
pip install -r requirements.txt
python app.py
```
Open `http://127.0.0.1:5000`.

## Data
`portal_data.py` provides the JSON data access functions. `portal_data.json` contains the migrated records. No Firebase Admin SDK or Firestore connection is required by this local build.

**Storage assets:** Imported data still contains existing Firebase Storage URLs for files and images. These assets have not been migrated; move them to the target storage service and update the URLs before shutting down Firebase Storage.
