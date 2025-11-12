from flask import Flask, request, jsonify
from flask_cors import CORS
import spacy
from spacy.lang.en.stop_words import STOP_WORDS
import string
import numpy as np
import math
import re

# -------------------- Load spaCy Model --------------------
nlp = spacy.load("en_core_web_sm")

# -------------------- Initialize Flask App --------------------
app = Flask(__name__)
# Update CORS configuration to be more specific
CORS(app, resources={
    r"/extract_skills": {
        "origins": [
            "http://127.0.0.1:5500",
            "http://www.atsoptimizer.com",
            "https://www.atsoptimizer.com"
        ],
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"]
    }
})

# -------------------- Utility Functions --------------------

def extract_skills(job_description):
    """Extract potential skill words from job description."""
    doc = nlp(job_description)
    skills = set()
    skill_pos_tags = {"NOUN", "PROPN"}
    exclude_pos_tags = {"DET", "NUM", "SYM", "PUNCT", "SPACE", "ADP", "CONJ"}
    stop_words = set(STOP_WORDS)
    exclude_characters = string.punctuation
    exclude_terms = {"day", "days", "week", "weeks", "month", "months", "year", "years"}
    url_pattern = re.compile(r'https?://\S+|www\.\S+')

    for token in doc:
        if (
            len(token.text) > 1
            and token.pos_ in skill_pos_tags
            and token.pos_ not in exclude_pos_tags
            and token.text.lower() not in stop_words
            and token.text.lower() not in exclude_terms
            and not all(char in exclude_characters for char in token.text)
            and not re.match(url_pattern, token.text)
        ):
            skill = token.text.lower()
            skills.add(skill)
            # Add combined 2-word skill
            if token.i < len(doc) - 1 and doc[token.i + 1].pos_ in skill_pos_tags:
                combined_skill = skill + " " + doc[token.i + 1].text.lower()
                skills.add(combined_skill)
    return list(skills)


def find_missing_skills_in_resume(skills_in_job_description, skills_in_resume):
    skills_in_job_description_lower = np.char.lower(skills_in_job_description)
    skills_in_resume_lower = np.char.lower(skills_in_resume)
    missing_skills = np.setdiff1d(
        skills_in_job_description_lower,
        skills_in_resume_lower,
        assume_unique=True
    )
    missing_skills_original_case = np.array([
        skills_in_job_description[i]
        for i in range(len(skills_in_job_description_lower))
        if skills_in_job_description_lower[i] in missing_skills
    ])
    return missing_skills_original_case


def find_matching_skills_in_resume(skills_in_job_description, skills_in_resume):
    skills_in_job_description_lower = np.char.lower(skills_in_job_description)
    skills_in_resume_lower = np.char.lower(skills_in_resume)
    matching_skills = np.intersect1d(
        skills_in_job_description_lower,
        skills_in_resume_lower,
        assume_unique=True
    )
    matching_skills_original_case = np.array([
        skills_in_job_description[i]
        for i in range(len(skills_in_job_description_lower))
        if skills_in_job_description_lower[i] in matching_skills
    ])
    return matching_skills_original_case


def round_number_ceil_or_floor(number):
    return math.ceil(number) if number % 1 >= 0.5 else math.floor(number)


def resume_status_pass_fail(number):
    if 81 <= number <= 100:
        return 'Best'
    elif 61 <= number <= 80:
        return 'Excellent'
    elif 41 <= number <= 60:
        return 'Good'
    elif 21 <= number <= 40:
        return 'Average'
    elif 1 <= number <= 20:
        return 'Below Average'
    else:
        return 'Below Average'


def format_skills(skills, is_available_in_resume: bool):
    return [{"name": skill, "is_available_in_resume": is_available_in_resume} for skill in skills]


# -------------------- Main API Endpoint --------------------

@app.route('/extract_skills', methods=['POST', 'OPTIONS'])
def extract_skills_from_description():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight OK"}), 200

    try:
        data = request.get_json() or {}
        if 'job_description' not in data or 'resume' not in data:
            return jsonify({"error": "Invalid request data"}), 400

        job_description = data['job_description'].strip()
        resume = data['resume'].strip()

        if not job_description:
            return jsonify({"error": "Empty job description"}), 400
        if not resume:
            return jsonify({"error": "Empty resume"}), 400

        # Extract skills
        skills_in_job_description = extract_skills(job_description)
        skills_in_resume = extract_skills(resume)

        missing_skills = find_missing_skills_in_resume(skills_in_job_description, skills_in_resume)
        matching_skills = find_matching_skills_in_resume(skills_in_job_description, skills_in_resume)

        missing_skills_formatted = format_skills(missing_skills, False)
        matching_skills_formatted = format_skills(matching_skills, True)
        all_skills = matching_skills_formatted + missing_skills_formatted

        total_required = len(all_skills)
        total_matching = total_required - len(missing_skills_formatted)
        resume_score = round((100 * total_matching) / total_required, 2)
        resume_score = round_number_ceil_or_floor(resume_score)
        if resume_score == 100:
            resume_score = 99  # slight adjustment

        response_data = {
            "resume_score_in_percentage": resume_score,
            "resume_status": resume_status_pass_fail(resume_score),
            "total_required_skills_in_job_description": total_required,
            "total_missing_skills_in_resume": len(missing_skills_formatted),
            "total_matching_skills_in_resume": total_matching,
            "skills": all_skills,
            "comma_separated_missing_skills": ', '.join(missing_skills),
        }

        return jsonify(response_data), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


# -------------------- Run Flask App --------------------
if __name__ == '__main__':
    # Accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)