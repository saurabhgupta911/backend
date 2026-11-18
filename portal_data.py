"""Local JSON data access for the DSAI portal.

This module intentionally has no Firebase/Firestore dependency. Data is read from
portal_data.json so the portal can run locally while the data is prepared for AWS.
"""
from __future__ import annotations
import json
from pathlib import Path
from typing import Any

DATA_FILE = Path(__file__).resolve().with_name("portal_data.json")

def load_data() -> dict[str, Any]:
    if not DATA_FILE.exists():
        return {}
    with DATA_FILE.open("r", encoding="utf-8") as file:
        return json.load(file)

def get_collection(name: str) -> list[dict[str, Any]]:
    data = load_data().get(name, [])
    if isinstance(data, list):
        return data
    if isinstance(data, dict):
        # Collection-style reads return the contained records.
        return list(data.values())
    return []

def get_document(collection_name: str, document_id: str) -> dict[str, Any]:
    data = load_data().get(collection_name, {})
    if isinstance(data, dict):
        document = data.get(document_id, {})
        return document if isinstance(document, dict) else {}
    return {}

def save_collection(name: str, records: list[dict[str, Any]]) -> None:
    data = load_data()
    data[name] = records
    _write_data(data)

def save_document(collection_name: str, document_id: str, document: dict[str, Any]) -> None:
    data = load_data()
    collection = data.get(collection_name)
    if not isinstance(collection, dict):
        collection = {}
    collection[document_id] = document
    data[collection_name] = collection
    _write_data(data)

def _write_data(data: dict[str, Any]) -> None:
    temporary_file = DATA_FILE.with_suffix(".tmp")
    temporary_file.write_text(json.dumps(data, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    temporary_file.replace(DATA_FILE)
