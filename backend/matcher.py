# matcher.py

# -----------------------------
# Configuration
# -----------------------------

STOP_WORDS = {
    "with", "and", "or", "in", "of", "for", "to",
    "a", "an", "the", "skills", "skill", "education", "degree"
}

DEGREE_RANK = {
    "bachelor": 1,
    "master": 2,
    "phd": 3
}

DEGREE_KEYWORDS = {
    "bachelor": ["bachelor", "bachelors", "b.tech", "btech", "bsc"],
    "master": ["master", "masters", "mba", "m.tech", "mtech", "msc"],
    "phd": ["phd", "doctorate"]
}


# -----------------------------
# Main hiring logic
# -----------------------------

def hiring_decision(
    resume_skills,
    resume_experience,
    resume_text,
    job_skills,
    required_experience,
    job_text
):
    # Defensive defaults
    resume_text = (resume_text or "").lower()
    job_text = (job_text or "").lower()
    resume_skills = [s.lower() for s in (resume_skills or [])]
    job_skills = [s.lower() for s in (job_skills or [])]

    # =================================================
    # RULE 1: SKILL ENFORCEMENT (HIGHEST PRIORITY)
    # =================================================
    # If job explicitly mentions skills, ALL must exist
    if job_skills:
        missing_skills = [
            skill for skill in job_skills
            if skill not in resume_text
        ]

        if missing_skills:
            return {
                "decision": "NOT HIRED",
                "reason": f"Missing required skills: {', '.join(missing_skills)}"
            }

    # =================================================
    # RULE 2: EXPERIENCE (ONLY IF MENTIONED)
    # =================================================
    if required_experience > 0:
        if resume_experience < required_experience:
            return {
                "decision": "NOT HIRED",
                "reason": "Required experience not met"
            }

    # =================================================
    # RULE 3: EDUCATION (DEGREE HIERARCHY + FIELD)
    # =================================================
    # Detect required degree from job
    job_degree = None
    for degree, keywords in DEGREE_KEYWORDS.items():
        if any(k in job_text for k in keywords):
            job_degree = degree
            break

    if job_degree:
        # Detect highest degree in resume
        resume_degree = None
        for degree, keywords in DEGREE_KEYWORDS.items():
            if any(k in resume_text for k in keywords):
                resume_degree = degree

        # Degree hierarchy check
        if not resume_degree or DEGREE_RANK[resume_degree] < DEGREE_RANK[job_degree]:
            return {
                "decision": "NOT HIRED",
                "reason": f"{job_degree.upper()} degree required"
            }

        # Education FIELD check (strict)
        edu_field_words = [
            w for w in job_text.split()
            if w not in STOP_WORDS
            and not any(w in kw for kws in DEGREE_KEYWORDS.values() for kw in kws)
            and len(w) > 2
        ]

        if not all(word in resume_text for word in edu_field_words):
            return {
                "decision": "NOT HIRED",
                "reason": "Education field not matched"
            }

    # =================================================
    # RULE 4: ROLE / REQUIREMENT WORD MATCH
    # =================================================
    job_words = [
        w for w in job_text.split()
        if w not in STOP_WORDS and len(w) > 2
    ]

    if job_words and all(word in resume_text for word in job_words):
        return {
            "decision": "HIRED",
            "reason": "Job role and requirements matched"
        }

    # =================================================
    # DEFAULT
    # =================================================
    return {
        "decision": "NOT HIRED",
        "reason": "Requirement not satisfied"
    }
