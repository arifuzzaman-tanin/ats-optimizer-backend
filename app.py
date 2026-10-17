import os
from pathlib import Path
import sys
from time import perf_counter

from flask import Flask, request, jsonify
from flask_cors import CORS
from werkzeug.exceptions import RequestEntityTooLarge

# PythonAnywhere deploys this repository as source rather than installing its
# package. Put the src-layout package on the import path for every WSGI entry
# point, while keeping local editable and wheel installs working as before.
PROJECT_ROOT = Path(__file__).resolve().parent
SOURCE_ROOT = PROJECT_ROOT / "src"
if SOURCE_ROOT.is_dir() and str(SOURCE_ROOT) not in sys.path:
    sys.path.insert(0, str(SOURCE_ROOT))

from ats_optimizer import ATSOptimizer, compare_skills, load_catalog

# -------------------- Initialize Flask App --------------------
app = Flask(__name__)
app.config["MAX_CONTENT_LENGTH"] = int(os.getenv("MAX_REQUEST_BYTES", 512 * 1024))
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
    r"/extract_skills": {
        "origins": ALLOWED_ORIGINS,
        "methods": ["GET", "POST", "OPTIONS"],
        "allow_headers": ["Content-Type", "Authorization"],
        "supports_credentials": True,
    }
})

# Build and validate the catalogue at process startup instead of delaying the
# first user request in each worker.
load_catalog()
optimizer = ATSOptimizer()

# -------------------- Utility Functions --------------------

def find_missing_skills_in_resume(skills_in_job_description, skills_in_resume):
    return compare_skills(skills_in_job_description, skills_in_resume, matching=False)


def find_matching_skills_in_resume(skills_in_job_description, skills_in_resume):
    return compare_skills(skills_in_job_description, skills_in_resume, matching=True)


# -------------------- Main API Endpoint --------------------

@app.route('/health', methods=['GET'])
def health_check():
    return jsonify({"status": "ok"}), 200


@app.errorhandler(RequestEntityTooLarge)
def request_too_large(_error):
    return jsonify({"error": "Request body is too large"}), 413


@app.route('/extract_skills', methods=['POST', 'OPTIONS'])
def extract_skills_from_description():
    # Handle preflight OPTIONS request
    if request.method == "OPTIONS":
        return jsonify({"message": "CORS preflight OK"}), 200

    try:
        data = request.get_json(silent=True)
        if not isinstance(data, dict):
            return jsonify({"error": "Invalid request data"}), 400

        if not all(isinstance(data.get(field), str) for field in ('job_description', 'resume')):
            return jsonify({"error": "job_description and resume must be strings"}), 400

        job_description = data['job_description'].strip()
        resume = data['resume'].strip()

        if not job_description:
            return jsonify({"error": "Empty job description"}), 400
        if not resume:
            return jsonify({"error": "Empty resume"}), 400

        analysis_started = perf_counter()
        result = optimizer.analyze(
            resume=resume,
            job_description=job_description,
        )
        analysis_ms = (perf_counter() - analysis_started) * 1000

        response = jsonify(result.to_dict())
        response.headers["Server-Timing"] = f"ats-optimizer;dur={analysis_ms:.2f}"
        return response, 200

    except RequestEntityTooLarge:
        raise
    except Exception:
        app.logger.exception("Skill extraction failed")
        return jsonify({"error": "Skill extraction failed"}), 500


# -------------------- Run Flask App --------------------
if __name__ == '__main__':
    # Accessible externally
    app.run(host='0.0.0.0', port=5000, debug=True)
