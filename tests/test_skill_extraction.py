from pathlib import Path
import unittest

from app import app, find_matching_skills_in_resume, find_missing_skills_in_resume
from skill_extractor import extract_skill_evidence, extract_skills


JOB = Path(__file__).with_name("fixtures").joinpath("customer_support_job.txt").read_text(encoding="utf-8")
AUTODESK_JOB = Path(__file__).with_name("fixtures").joinpath(
    "autodesk_senior_software_developer.txt"
).read_text(encoding="utf-8")
ALPHASENSE_JOB = Path(__file__).with_name("fixtures").joinpath(
    "alphasense_excel_engineer.txt"
).read_text(encoding="utf-8")

# Selected experience and skills from the supplied resume, without personal data.
RESUME = """
Customer Service Representative
Proactively engage with clients through various communication channels to
deliver an outstanding customer service experience, making every client
interaction an exceptional one (phone/email).
Responding empathetically to questions and resolving client concerns at first
point of contact. Financial Services Representative (Call center).
Resolving customer complaints and answering inquiries with professionalism and
empathy. Coordinate with the production team to schedule projects.
Communication skills. Problem-solving skills. Active listening skills.
Patience and empathy. Attention to detail. Teamwork. Time management skills.
"""


class ExtractionTests(unittest.TestCase):
    def test_alphasense_excel_role_extracts_explicit_engineering_skills(self):
        skills = set(extract_skills(ALPHASENSE_JOB, source="job_description"))
        self.assertTrue({
            ".net", "advanced excel", "amazon web services", "artificial intelligence",
            "asynchronous programming", "c#", "cloud integration",
            "com add-in development", "corporate proxy support",
            "cross-platform development", "csv", "data analysis",
            "data synchronization", "data transformation", "debugging",
            "desktop application development", "distributed systems",
            "enterprise authentication", "error handling",
            "equity research", "event-driven architecture", "excel add-in development",
            "excel calculation engine", "excel formula development",
            "excel object model", "fault recovery", "financial analysis",
            "financial modeling", "financial technology", "json",
            "legacy system modernization", "macos", "market intelligence",
            "memory optimization", "microsoft excel", "microsoft office",
            "monitoring", "oauth", "office add-in development",
            "offline application development", "performance optimization",
            "real-time data feeds", "rest api", "saml", "single sign-on",
            "software deployment", "software development",
            "software development best practices", "software testing",
            "software update management", "software version management",
            "software reliability", "state management", "streaming architecture",
            "systems integration", "technical mentoring",
            "trading systems", "user interface design", "visual studio",
            "visual studio tools for office", "web development", "websocket",
            "windows", "xlsx",
        }.issubset(skills))
        self.assertNotIn("game development", skills)

    def test_autodesk_job_extracts_specific_engineering_skills(self):
        skills = set(extract_skills(AUTODESK_JOB, source="job_description"))
        self.assertTrue({
            "software development", "cloud services development",
            "web application development", "desktop application development",
            "software architecture", "software design patterns",
            "software development lifecycle", "requirements analysis",
            "cross-functional collaboration", "process improvement", "technical research",
            "prototyping", "technical writing", "presentation skills",
            "large language models", "artificial intelligence",
            "ai-assisted software development", "github copilot", "cursor", "claude",
            "on-call support", "production support", "high-throughput systems",
            "api development", "application security", "microservices",
            "relational databases", "postgresql", "database schema design",
            "query performance optimization", "monitoring", "logging", "alerting",
            "incident response", "debugging", "unit testing", "automated testing",
            "cypress", "playwright", "typescript", "c#", "python",
            "independent work", "prioritization", "ownership", "communication",
            "amazon web services", "aws lambda", "amazon api gateway", "amazon s3",
            "amazon rds", "computer-aided design", "autodesk inventor",
            "autodesk revit", "aec", "automation", "devops", "ci/cd",
            "infrastructure as code", "scrum",
        }.issubset(skills))
        self.assertNotIn("sales", skills)

    def test_supplied_job_produces_capabilities_only(self):
        self.assertEqual(set(extract_skills(JOB, source="job_description")), {
            "customer support", "troubleshooting", "ticket management",
            "phone support", "email support", "live chat support",
            "escalation management", "product setup", "knowledge base management",
            "technical writing", "customer feedback analysis", "trend analysis",
            "cross-functional collaboration", "outsourced support coordination",
            "first contact resolution", "empathy", "ownership",
        })

    def test_supplied_resume_matches_equivalent_experience(self):
        matches = find_matching_skills_in_resume(
            extract_skills(JOB, source="job_description"), extract_skills(RESUME)
        )
        self.assertEqual(set(matches), {
            "customer support", "phone support", "email support", "empathy",
            "first contact resolution", "cross-functional collaboration",
        })

    def test_problem_solving_does_not_imply_technical_troubleshooting(self):
        self.assertEqual(extract_skills("Problem-solving skills"), ["problem solving"])

    def test_generic_words_and_company_names_are_not_skills(self):
        self.assertEqual(extract_skills(
            "Manager, countries, job, lab, CTO, Dr. Yihong Qi, Pontosense, "
            "Silvie, January, Waterloo, patents, sensors, families, parent, "
            "safety, sleep, cameras, pendants, wearables, home, time, contact, "
            "team, head, company, rate, care, member, engineering, reports."
        ), [])

    def test_company_technology_is_not_a_job_requirement(self):
        description = """**The Company**
We build our platform with Python and Docker.
**Why now**
Our CEO wrote React.js software.
**The role**
Provide customer service and troubleshooting.
**How We Work**
We prize leadership and ownership.
**Required skills**
Zendesk experience.
"""
        self.assertEqual(extract_skills(description, source="job_description"),
                         ["customer support", "troubleshooting", "zendesk"])

    def test_context_does_not_cross_markdown_bullets(self):
        self.assertNotIn("email support", extract_skills(
            "- Customer service experience\n- Send emails to your friends"
        ))

    def test_context_does_not_cross_sentences(self):
        self.assertNotIn("phone support", extract_skills(
            "Customer support experience. I use my phone for photos."
        ))

    def test_plain_communication_channels_are_not_support_skills(self):
        self.assertEqual(extract_skills("Emails, phone calls and chats with friends."), [])

    def test_bpo_alone_does_not_imply_bpo_coordination(self):
        self.assertEqual(extract_skills("BPO company"), [])

    def test_articles_alone_do_not_imply_technical_writing(self):
        self.assertEqual(extract_skills("Read articles and travel guides."), [])

    def test_pdf_ligatures_line_breaks_and_hyphens(self):
        self.assertEqual(extract_skills(
            "ﬁnancial\n services\n Problem–solving\n customer\n service"
        ), ["customer support", "financial services", "problem solving"])

    def test_multiword_skills_are_not_split_into_nouns(self):
        self.assertEqual(extract_skills("Active listening and time management"),
                         ["active listening", "time management"])

    def test_aliases_are_deduplicated(self):
        self.assertEqual(extract_skills("Customer service, client support, customer support"),
                         ["customer support"])

    def test_alias_comparison_preserves_original_job_label(self):
        job = ["Customer Support", "customer service", "EXCEL", "Troubleshooting"]
        resume = ["client support", "Microsoft Excel"]
        self.assertEqual(find_matching_skills_in_resume(job, resume), ["Customer Support", "EXCEL"])
        self.assertEqual(find_missing_skills_in_resume(job, resume), ["Troubleshooting"])

    def test_empty_skill_comparison(self):
        self.assertEqual(find_matching_skills_in_resume([], []), [])
        self.assertEqual(find_missing_skills_in_resume(["Python"], []), ["Python"])

    def test_technical_symbols_and_boundaries(self):
        skills = extract_skills("C++, C#, .NET, JavaScript, PostgreSQL, React.js, Node.js, AWS")
        self.assertEqual(skills, [
            ".net", "amazon web services", "c#", "c++", "javascript",
            "node.js", "postgresql", "react",
        ])
        self.assertNotIn("java", skills)
        self.assertNotIn("sql", skills)

    def test_tool_names_are_not_substrings_of_other_words(self):
        self.assertEqual(extract_skills("GitHub, JavaScripted, SQLAlchemy, Pythonic"), [])

    def test_ambiguous_skill_words_require_context(self):
        self.assertEqual(extract_skills(
            "You excel at your job. React quickly to questions. Be agile. "
            "We photograph pandas and angular shapes."
        ), [])
        self.assertEqual(extract_skills(
            "Skills: React, Angular, Python, pandas, Excel, SQL, Agile methodology"
        ), ["agile", "angular", "microsoft excel", "pandas", "python", "react", "sql"])

    def test_named_tools_can_appear_alone_in_a_skill_list(self):
        self.assertEqual(extract_skills("React\n• Excel\n• Angular\n• pandas"),
                         ["angular", "microsoft excel", "pandas", "react"])

    def test_negated_experience_or_requirements(self):
        for text in [
            "No Python experience.", "No prior experience with Python.",
            "I am not proficient in Python.", "Python is not required.",
            "Python experience isn't required.", "I don't know Python.",
            "Never worked with Python.",
        ]:
            with self.subTest(text=text):
                self.assertNotIn("python", extract_skills(text))

    def test_negation_is_bounded_and_not_only_is_positive(self):
        self.assertEqual(extract_skills("No Java experience, but Python skills."), ["python"])
        self.assertEqual(extract_skills("Not only Python but also SQL."), ["python", "sql"])

    def test_results_and_evidence_are_deterministic(self):
        first = extract_skill_evidence(JOB, source="job_description")
        self.assertEqual(first, extract_skill_evidence(JOB, source="job_description"))
        self.assertEqual(list(first), sorted(first))
        self.assertIn("customer support", first["customer support"].phrases)


class ApiTests(unittest.TestCase):
    def setUp(self):
        self.client = app.test_client()

    def post(self, job, resume):
        return self.client.post('/extract_skills', json={"job_description": job, "resume": resume})

    def test_existing_response_fields_and_explainable_matches(self):
        response = self.post(JOB, RESUME)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total_required_skills_in_job_description"], 17)
        self.assertEqual(data["total_matching_skills_in_resume"], 6)
        self.assertEqual(data["total_missing_skills_in_resume"], 11)
        self.assertEqual(data["resume_score_in_percentage"], 35)
        self.assertEqual(data["resume_status"], "Average")
        for skill in data["skills"]:
            self.assertTrue(skill["job_description_evidence"])
            self.assertEqual(bool(skill["resume_evidence"]), skill["is_available_in_resume"])

    def test_no_recognized_job_skills_is_safe_and_explained(self):
        response = self.post("Toronto, January, Silvie, patents", RESUME)
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["skills"], [])
        self.assertEqual(data["total_required_skills_in_job_description"], 0)
        self.assertEqual(data["resume_score_in_percentage"], 0)
        self.assertIn("warning", data)

    def test_no_matching_resume_skills_is_safe(self):
        response = self.post("Python and SQL skills", "Toronto, January")
        self.assertEqual(response.status_code, 200)
        data = response.get_json()
        self.assertEqual(data["total_missing_skills_in_resume"], 2)
        self.assertEqual(data["total_matching_skills_in_resume"], 0)

    def test_complete_match_is_100_percent(self):
        data = self.post("Customer support and Python", "Customer service and Python").get_json()
        self.assertEqual(data["resume_score_in_percentage"], 100)
        self.assertEqual(data["resume_status"], "Best")
        self.assertEqual(data["comma_separated_missing_skills"], "")

    def test_non_object_and_invalid_field_types_return_400(self):
        for payload in [[], None, "text", 42, {},
                        {"job_description": None, "resume": RESUME},
                        {"job_description": ["Python"], "resume": RESUME},
                        {"job_description": "Python", "resume": 123}]:
            with self.subTest(payload=payload):
                self.assertEqual(self.client.post('/extract_skills', json=payload).status_code, 400)

    def test_empty_inputs_return_400(self):
        self.assertEqual(self.post("  ", RESUME).status_code, 400)
        self.assertEqual(self.post(JOB, "  ").status_code, 400)

    def test_malformed_json_and_wrong_content_type_return_400(self):
        self.assertEqual(self.client.post('/extract_skills', data='{', content_type='application/json').status_code, 400)
        self.assertEqual(self.client.post('/extract_skills', data='text').status_code, 400)

    def test_health_and_existing_cors_remain_available(self):
        self.assertEqual(self.client.get('/health').get_json(), {"status": "ok"})
        response = self.client.options('/extract_skills', headers={
            "Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'http://localhost:5173')


if __name__ == '__main__':
    unittest.main()
