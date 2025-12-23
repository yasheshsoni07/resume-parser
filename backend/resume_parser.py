from io import BytesIO
import pdfplumber
import nltk
import re
from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize
from nltk.stem import WordNetLemmatizer

SKILLS_DB = [
    "python", "java", "machine learning", "deep learning",
    "nlp", "react", "sql", "fastapi", "django"
]


def extract_text_from_pdf(file_bytes):
    text = ""
    with pdfplumber.open(BytesIO(file_bytes)) as pdf:
        for page in pdf.pages:
            page_text = page.extract_text()
            if page_text:
                text += page_text + " "
    return text.lower()


def clean_text(text):
    tokens = word_tokenize(text)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    clean_tokens = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word.isalpha() and word not in stop_words
    ]
    return clean_tokens

def extract_skills(text):
    skills_found = []
    for skill in SKILLS_DB:
        if skill in text:
            skills_found.append(skill)
    return list(set(skills_found))

def extract_experience(text):
    match = re.findall(r'(\d+)\s+years', text)
    if match:
        return max(map(int, match))
    return 0

def parse_resume(file_bytes, filename):
    if filename.endswith(".pdf"):
        text = extract_text_from_pdf(file_bytes)
    else:
        text = file_bytes.decode("utf-8").lower()

    skills = extract_skills(text)
    experience = extract_experience(text)
    education = extract_education(text)

    return {
        "skills": skills,
        "education": education,
        "experience": experience,
        "raw_text": text
    }


def extract_education(text):
    education_keywords = [
        "master", "masters", "mba",
        "bachelor", "phd",
        "business management",
        "management"
    ]

    found = []
    for edu in education_keywords:
        if edu in text:
            found.append(edu)

    return list(set(found))
