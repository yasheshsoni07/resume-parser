import re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
from nltk.stem import WordNetLemmatizer

def parse_job(job_text):
    job_text = job_text.lower()

    # Extract required experience
    exp_match = re.findall(r'(\d+)\s+years', job_text)
    required_experience = int(exp_match[0]) if exp_match else 0

    tokens = word_tokenize(job_text)
    stop_words = set(stopwords.words("english"))
    lemmatizer = WordNetLemmatizer()

    keywords = [
        lemmatizer.lemmatize(word)
        for word in tokens
        if word.isalpha() and word not in stop_words
    ]

    requirements = detect_mandatory_requirements(job_text)

    return {
        "required_skills": list(set(keywords)),
        "required_experience": required_experience,
        "job_text": job_text,
        "mandatory": requirements
    }


def detect_mandatory_requirements(job_text):
    job_text = job_text.lower()

    requirements = {
        "education": False,
        "experience": False
    }

    if "education" in job_text or "degree" in job_text:
        requirements["education"] = True

    if "year" in job_text:
        requirements["experience"] = True

    return requirements
