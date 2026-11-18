# DSAI Portal – Firestore to local JSON migration

## Imported data
The user-provided `firestore_export.json` has been converted into `portal_data.json`.

| Collection | Imported records |
|---|---:|
| Faculty | 8 |
| courses (DSAI document) | 1 |
| events | 3 |
| placementInfo | 2 |
| timetables | 3 |
| sessions | 4 |
| adminInfo | 3 |
| coCurricularActivities | 4 |
| libraryBooks | 62 (retained from the existing local catalogue; not part of this export) |

The `courses` collection is stored as a document map keyed by `DSAI`, because the application reads it by document ID. The other collections are stored as arrays of document fields, matching the existing local data access layer.

## Important storage note
Some imported records contain Firebase Storage download URLs for syllabus PDFs, notes, timetable PDFs, faculty photos and event photos. These URLs have been preserved so existing links are not discarded. This migration removes Firestore as the portal's data source; it does **not** migrate Firebase Storage files. Those assets must be copied to the eventual storage destination (for example, S3) and their URLs updated before Firebase Storage can be retired.

## Run locally
```bash
pip install -r requirements.txt
python app.py
```
Then open `http://127.0.0.1:5000`.

## Validation
Python syntax compilation and JSON parsing should be run after changes. A live Flask runtime test is still required in an environment where the requirements are installed.
