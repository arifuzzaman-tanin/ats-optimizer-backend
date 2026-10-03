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

VITAA_JOB = """
About the job
ViTAA is a medical-device software company developing AI-powered medical-image
analysis technology. We need a primary developer for federated single sign-on
and an edge connector that retrieves imaging studies from hospital PACS.

What you'll work on
Federated authentication as a relying party: per-tenant identity provider
configuration, just-in-time provisioning, session and token lifetime, and
tenant isolation. Implement SAML 2.0 and OpenID Connect (OIDC) against Microsoft
Entra ID and Okta, and diagnose a federation failure. Migrate authentication
without a service interruption.
The edge connector must be reliable and includes DICOM and DICOMweb ingest (AE titles,
query/retrieve, storage and transfer syntaxes), store-and-forward,
back-pressure, and observability. Integrate third-party open-source DICOM
software outside .NET. The deployment surface includes TLS, proxies, NAT, DNS,
firewall rules, IP allowlists, logs and packet captures.
Packaging and installation includes image builds, configuration, the upgrade
path, software versioning, and a runbook the hospital IT team will follow.

Requirements
Professional backend software engineering and production .NET. Experience with
on-premise agents, installed services, appliances or embedded systems. Docker
and container packaging. Networking fundamentals sufficient to diagnose TLS
and proxy failures from logs and packet captures. Rigour and attention to
detail. Own implementation, testing, and packaging; customer implementations
cover technical discovery, site readiness, configuration, validation and
go-live while working across engineering, product, cybersecurity, hospital IT,
quality and regulatory affairs.

Nice to have
DICOM or DICOMweb and PACS or VNA. Any of fo-dicom, Orthanc or dcm4che. Any of
Auth0, WorkOS, Okta, Entra ID, Keycloak or Cognito. F# or another functional or
statically-typed language. Regulated software delivery with design controls,
verification evidence, medical-device standards (ISO 13485, IEC 62304 and ISO
14971), health data privacy, or a safety-critical discipline. Services on AWS,
CI pipelines, and supporting customers directly during production incidents.

Our stack
F# on .NET, PostgreSQL and AWS, with continuous integration in GitLab. The work
runs under a quality management system (QMS), software lifecycle and risk
management. Documentation and verification and validation evidence are needed.
"""

# Paraphrased recurring requirements sampled from public LinkedIn, Indeed,
# Lever, Greenhouse and Ashby postings in October 2026.
PUBLIC_JOB_SAMPLES = {
    "data_engineering": (
        "Data engineering with AWS, Snowflake, dbt, Apache Airflow and Informatica IICS. "
        "Build ETL/ELT data pipelines and dimensional data models for a cloud data "
        "warehouse. Use Fivetran, Airbyte, Matillion or Dagster. Strong Python, SQL, "
        "Spark, PySpark, Databricks, Iceberg, Kafka, Terraform, Redshift and BigQuery. "
        "Implement data quality, data governance and RBAC.",
        {
            "airbyte", "amazon redshift", "amazon web services", "apache airflow",
            "apache iceberg", "apache kafka", "apache spark", "dagster",
            "data engineering", "data governance", "data modeling",
            "data pipeline development", "data quality", "data warehousing",
            "databricks", "dbt", "dimensional modeling", "elt", "etl", "fivetran",
            "google bigquery", "informatica iics", "matillion", "pyspark", "python",
            "role-based access control", "snowflake", "sql", "terraform",
        },
    ),
    "backend": (
        "Backend engineering with Python, FastAPI, REST APIs, GraphQL and gRPC. API "
        "design, caching, rate limiting, async I/O, safe concurrency, background "
        "processing, message brokers, retries, idempotency and dead-letter queues. "
        "Production observability includes logging, metrics, distributed tracing, "
        "Datadog and CloudWatch. Code reviews, OOP, dependency injection, RabbitMQ, "
        "Redis, Elasticsearch, SQS, SNS and EventBridge.",
        {
            "amazon cloudwatch", "amazon eventbridge", "amazon sns", "amazon sqs",
            "api development", "application metrics", "asynchronous programming",
            "backend software development", "background job processing", "caching",
            "code review", "concurrent programming", "datadog", "dead-letter queues",
            "dependency injection", "distributed tracing", "elasticsearch", "fastapi",
            "graphql", "grpc", "idempotency", "logging", "message queues",
            "object-oriented programming", "observability", "python", "rabbitmq",
            "rate limiting", "redis", "rest api", "retry handling",
        },
    ),
    "devops": (
        "AWS EC2, VPC, IAM, KMS, Terraform and CloudFormation. Kubernetes and Helm, "
        "Docker, Jenkins, GitHub Actions, Prometheus and Grafana. Bash scripting, "
        "secrets management, vulnerability scanning, ArgoCD, FluxCD, service mesh and "
        "cloud cost optimization.",
        {
            "amazon ec2", "amazon vpc", "amazon web services", "argocd",
            "aws cloudformation", "aws identity and access management",
            "aws key management service", "bash", "docker", "finops", "flux cd",
            "github actions", "grafana", "helm", "jenkins", "kubernetes",
            "prometheus", "secrets management", "service mesh", "terraform",
            "vulnerability management",
        },
    ),
    "support_frontend_ml": (
        "SaaS technical support with Zendesk, Salesforce Service Cloud and Zoho "
        "ticketing. Meet SLA targets and CSAT benchmarks; reproduce issues. React, "
        "Next.js, GraphQL, JWT, Jest, Redux, Webpack, npm, Yarn, ESLint, Sass CSS, "
        "LessCSS, responsive web design, WCAG, TailwindCSS, Storybook.js, TanStack "
        "Query, tRPC, React Native, Expo framework, WebRTC and Vercel. MLOps with "
        "scikit-learn, MLflow, LangChain, model training, model evaluation, model "
        "monitoring, responsible AI, feature engineering, XGBoost, LightGBM, Hugging "
        "Face, a model registry, model deployment, semantic search, vector databases, "
        "RAG and prompt engineering.",
        {
            "customer satisfaction", "eslint", "expo", "feature engineering",
            "graphql", "hugging face", "issue reproduction", "jest",
            "json web tokens", "langchain", "less css", "lightgbm",
            "machine learning deployment", "mlflow", "mlops", "model evaluation",
            "model monitoring", "model registry", "model training", "next.js", "npm",
            "prompt engineering", "react", "react native", "redux", "responsible ai",
            "responsive web design", "retrieval-augmented generation", "saas support",
            "salesforce service cloud", "sass", "scikit-learn", "semantic search",
            "service level management", "storybook", "tailwind css", "tanstack query",
            "trpc", "vector databases", "vercel", "web accessibility", "webpack",
            "webrtc", "xgboost", "yarn", "zendesk", "zoho desk",
        },
    ),
}

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

    def test_vitaa_job_extracts_healthcare_integration_and_delivery_skills(self):
        skills = set(extract_skills(VITAA_JOB, source="job_description"))
        expected = {
            ".net", "amazon cognito", "amazon web services", "artificial intelligence",
            "attention to detail", "auth0", "authentication troubleshooting",
            "backend software development", "backpressure", "ci/cd",
            "computer networking", "configuration management",
            "cross-functional collaboration", "customer onboarding", "cybersecurity",
            "data ingestion", "dcm4che", "deployment readiness", "deployment validation",
            "design controls", "dicom", "dicom query/retrieve", "dicom transfer syntax",
            "dicomweb", "docker", "docker image building", "domain name system",
            "embedded systems", "f#", "federated authentication", "firewall configuration",
            "fo-dicom", "functional programming", "gitlab", "go-live support",
            "health data privacy", "identity provider configuration", "iec 62304",
            "incident response", "ip allowlisting", "iso 13485", "iso 14971",
            "just-in-time provisioning", "keycloak", "log analysis", "logging",
            "medical device software", "medical image analysis", "microsoft entra id",
            "multi-tenant architecture", "network address translation",
            "network troubleshooting", "observability", "okta", "on-premises software",
            "openid connect", "open-source software", "orthanc", "ownership",
            "packet analysis", "pacs", "postgresql", "production support", "proxy servers",
            "quality management systems", "regulated software development",
            "regulatory compliance", "risk management", "runbook development",
            "safety-critical software", "saml", "session management", "single sign-on",
            "software development lifecycle", "software installation", "software packaging",
            "software reliability", "software testing", "software update management",
            "software version management", "statically typed programming",
            "store-and-forward", "systems integration", "technical discovery",
            "technical writing", "token management", "transport layer security",
            "vendor neutral archive", "verification and validation", "workos",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_public_job_market_samples_extract_recurring_skills(self):
        for role, (description, expected) in PUBLIC_JOB_SAMPLES.items():
            with self.subTest(role=role):
                skills = set(extract_skills(description, source="job_description"))
                self.assertTrue(expected.issubset(skills), expected - skills)

    def test_ambiguous_new_tool_names_still_require_technical_context(self):
        self.assertEqual(extract_skills(
            "The snowflake melted. We bought yarn at the expo and read a storybook. "
            "Use less paint and add a spark of creativity."
        ), [])

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
