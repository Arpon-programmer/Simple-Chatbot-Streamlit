import json
from difflib import get_close_matches
import string
import re
from nltk.stem import PorterStemmer
from nltk.tokenize import word_tokenize
import nltk
nltk.download('punkt_tab')

# Initialize Porter Stemmer for stemming
stemmer = PorterStemmer()

'''load file'''


def load_knowledge_base(file_path: str) -> dict:
    with open(file_path, 'r') as file:
        data: dict = json.load(file)
    return data


def save_knowledge_base(file_path: str, data: dict):
    with open(file_path, 'w') as file:
        json.dump(data, file, indent=2)


def preprocess_text(text: str) -> str:
    """Normalize text by converting to lowercase, removing punctuation, and stemming."""
    # Remove numbers and punctuation
    text = re.sub(r'[0-9]', '', text)  # Remove numbers
    text = text.translate(str.maketrans('', '', string.punctuation))  # Remove punctuation
    text = text.lower().strip()  # Lowercase and strip whitespace

    # Tokenize and stem
    tokens = word_tokenize(text)
    stemmed_tokens = [stemmer.stem(token) for token in tokens]
    return ' '.join(stemmed_tokens)


def find_best_match(user_question: str, questions: list[str]) -> str | None:
    """Find the best matching question using fuzzy matching."""
    user_question = preprocess_text(user_question)
    # Increase cutoff for better accuracy
    matches: list = get_close_matches(user_question, [preprocess_text(q) for q in questions], n=3, cutoff=0.5)
    return matches[0] if matches else None


def get_answer_for_question(question: str, knowledge_base: dict) -> str | None:
    """Retrieve the answer for the matched question."""
    for q in knowledge_base["questions"]:
        if preprocess_text(q["question"]) == question:
            return q["answer"]