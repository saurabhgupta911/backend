from flask import Flask, request, jsonify
import re
from portal_data import get_collection

app = Flask(__name__)

# --- Library catalogue loaded from portal_data.json ---
full_library_list = get_collection("libraryBooks")
# --- Synonyms / normalization ---
SUBJECT_MAP = {
    "artificial intelligence": ["ai", "a i", "a.i", "artificial intelligence", "soft computing", "pragmatic al", "al robots", "description logic"],
    "machine learning": ["ml", "m l", "m.l", "machine learning", "deep learning", "dl", "d l", "d.l", "transformers", "prml"],
    "data science": ["ds", "d s", "d.s", "data science", "business analytics", "essential math for data science", "python for data analysis", "r for data science"],
    "statistics": ["statistics", "stats", "statistical inference"],
    "programming": ["python", "java", "c++", "core java", "python programming"],
    "database systems": ["database", "dbms", "data warehouse", "data warehousing", "database management system"],
    "data structures & algorithms": ["data structures", "algorithms", "dsa", "computational geometry", "introduction to algorithms"],
    "computer networks & security": ["network", "networking", "security", "iot", "internet of things", "computer security"],
    "image processing": ["image processing", "digital image processing"],
    "computer graphics": ["graphics", "computer graphics"],
    "aptitude & competitive exams": ["aptitude", "cat", "verbal ability", "quantitative aptitude"],
    "business & management": ["business", "management", "marketing", "hr", "organization behaviour", "research methods", "human resource"]
}

ASK_KEYWORDS = [
    "book", "books", "suggest", "recommend", "list", "catalog", "catalogue",
    "library", "any", "have", "available", "find", "get", "show"
]

def normalize_subject(q: str) -> str:
    q = q.lower().strip()
    
    # special case → all books
    if "all books" in q or "full list" in q or "entire library" in q:
        return "all"
    
    for subject, keys in SUBJECT_MAP.items():
        for k in keys:
            if re.search(rf"\b{re.escape(k)}\b", q, flags=re.IGNORECASE):
                return subject
    return ""

def match_books_locally(subject: str):
    if subject == "all":
        return full_library_list
    out = []
    s = subject.lower()
    for b in full_library_list:
        if b.get("category", "").lower() == s:
            out.append(b)
    return out

@app.route("/ask_book", methods=["POST"])
def ask_book():
    data = request.get_json(force=True) or {}
    question = (data.get("question") or "").strip()
    confirm = data.get("confirm", None)

    subject = normalize_subject(question)
    if not subject:
        return jsonify({
            "answer": "Sorry, I couldn't understand the subject you're asking about. Try AI, ML, Data Science, Statistics, Database, Python, etc."
        }), 200

    # If the user clearly wants books → return directly
    wants_books = any(w in question.lower() for w in ASK_KEYWORDS)
    if wants_books:
        books = match_books_locally(subject)
        if not books:
            return jsonify({"answer": f"I looked for {subject} but couldn't find any books right now."}), 200
        return jsonify({
            "answer": f"Here are {subject} books:",
            "books": books,
            "subject": subject
        }), 200

    # 2-step flow
    if confirm is None:
        return jsonify({
            "answer": f"Yes—reading helps a lot for {subject}. Would you like me to suggest a few books?",
            "subject": subject,
            "next": {"endpoint": "/ask_book", "payload_example": {"question": f"suggest {subject} books", "confirm": True}}
        }), 200

    if confirm is False:
        return jsonify({"answer": "No problem. I'm here if you need help—ask me anytime!"}), 200

    # confirm is True
    books = match_books_locally(subject)
    if not books:
        return jsonify({"answer": f"I looked for {subject} but couldn't find any books right now."}), 200
    return jsonify({
        "answer": f"Here are {subject} books:",
        "books": books,
        "subject": subject
    }), 200

if __name__ == "__main__":
    app.run(debug=True)
