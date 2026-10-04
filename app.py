from flask import Flask, request, jsonify
from flask_cors import CORS
import math
from access_keys import get_first_key, is_valid_key
from skill_extractor import compare_skills, extract_skill_evidence, extract_skills

# -------------------- Initialize Flask App --------------------
app = Flask(__name__)
ALLOWED_ORIGINS = [
    "http://localhost:5173",
    "http://127.0.0.1:5173",
    "http://localhost:5500",
    "http://127.0.0.1:5500",
    "http://www.atsoptimizer.com",
    "https://www.atsoptimizer.com",
    "https://arifuzzaman-tanin.github.io",
]

CORS(app, resources={
    r"/(?:access_key|extract_skills)": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
    }
})

# -------------------- Utility Functions --------------------

def find_missing_skills_in_resume(skills_in_job_description, skills_in_resume):
    return compare_skills(skills_in_job_description, skills_in_resume, matching=False)


def find_matching_skills_in_resume(skills_in_job_description, skills_in_resume):
    return compare_skills(skills_in_job_description, skills_in_resume, matching=True)


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

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.route('/access_key', methods=['GET'])
def access_key():
    try:
        key = get_first_key()
    except Exception:
        app.logger.exception("Unable to read access key from Google Sheet")
        return jsonify({"error": "Unable to retrieve access key"}), 503

    if key is None:
        return jsonify({"error": "No access key found"}), 404

    return jsonify({"access_key": key}), 200


@app.route('/extract_skills', methods=['POST', 'OPTIONS'])
def extract_skills_from_description():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight OK"}), 200

    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request data"}), 400

        access_key_value = data.get('access_key')
        if not isinstance(access_key_value, str) or not access_key_value.strip():
            return jsonify({"error": "Access key is required"}), 400

        try:
            key_is_valid = is_valid_key(access_key_value)
        except Exception:
            app.logger.exception("Unable to validate access key with Google Sheet")
            return jsonify({"error": "Unable to validate access key"}), 503

        if not key_is_valid:
            return jsonify({"error": "Invalid access key"}), 401

        if not all(isinstance(data.get(field), str) for field in ('job_description', 'resume')):
            return jsonify({"error": "job_description and resume must be strings"}), 400

        job_description = data['job_description'].strip()
        resume = data['resume'].strip()

        if not job_description:
            return jsonify({"error": "Empty job description"}), 400
        if not resume:
            return jsonify({"error": "Empty resume"}), 400

        # Compare canonical skill names; preserve the phrases that support them.
        job_evidence = extract_skill_evidence(job_description, source="job_description")
        resume_evidence = extract_skill_evidence(resume, source="resume")
        skills_in_job_description = list(job_evidence)
        skills_in_resume = list(resume_evidence)

        missing_skills = find_missing_skills_in_resume(skills_in_job_description, skills_in_resume)
        matching_skills = find_matching_skills_in_resume(skills_in_job_description, skills_in_resume)

        missing_skills_formatted = format_skills(missing_skills, False)
        matching_skills_formatted = format_skills(matching_skills, True)
        all_skills = matching_skills_formatted + missing_skills_formatted
        for skill in all_skills:
            name = skill["name"]
            skill["category"] = job_evidence[name].category
            skill["job_description_evidence"] = list(job_evidence[name].phrases)
            skill["resume_evidence"] = list(resume_evidence[name].phrases) if name in resume_evidence else []

        total_required = len(all_skills)
        total_matching = total_required - len(missing_skills_formatted)
        resume_score = round_number_ceil_or_floor(100 * total_matching / total_required) if total_required else 0

        response_data = {
            "resume_score_in_percentage": resume_score,
            "resume_status": resume_status_pass_fail(resume_score),
            "total_required_skills_in_job_description": total_required,
            "total_missing_skills_in_resume": len(missing_skills_formatted),
            "total_matching_skills_in_resume": total_matching,
            "skills": all_skills,
            "comma_separated_missing_skills": ', '.join(missing_skills),
            "skill_extraction_method": "curated_catalogue_with_context_and_aliases",
            "score_scope": "Recognized job skills evidenced in the resume; not an overall ATS score",
        }
        if not total_required:
            response_data["warning"] = "No recognized job skills found. Extend skills_catalog.json for this domain; the score is not informative."

        return jsonify(response_data), 200

    except Exception:
        app.logger.exception("Skill extraction failed")
        return jsonify({"error": "Skill extraction failed"}), 500


# -------------------- Run Flask App --------------------
if __name__ == '__main__':
    # Accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
