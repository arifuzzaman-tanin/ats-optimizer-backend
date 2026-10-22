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
L3HARRIS_JOB = Path(__file__).with_name("fixtures").joinpath(
    "l3harris_software_engineer.txt"
).read_text(encoding="utf-8")
NETBRAIN_JOB = Path(__file__).with_name("fixtures").joinpath(
    "netbrain_senior_software_engineer.txt"
).read_text(encoding="utf-8")
BETTINGJOBS_JOB = Path(__file__).with_name("fixtures").joinpath(
    "bettingjobs_senior_software_engineer.txt"
).read_text(encoding="utf-8")
BLUEHOST_AI_BACKEND_JOB = Path(__file__).with_name("fixtures").joinpath(
    "bluehost_ai_backend_engineer.txt"
).read_text(encoding="utf-8")
REAL_TIME_PAYMENTS_JOB = Path(__file__).with_name("fixtures").joinpath(
    "real_time_payments_developer.txt"
).read_text(encoding="utf-8")
PROMACH_CLOUD_ARCHITECT_JOB = Path(__file__).with_name("fixtures").joinpath(
    "promach_cloud_architect_engineer.txt"
).read_text(encoding="utf-8")
MULTI_TENANT_SAAS_CLOUD_ARCHITECT_JOB = Path(__file__).with_name("fixtures").joinpath(
    "multi_tenant_saas_cloud_architect.txt"
).read_text(encoding="utf-8")
AQUATIC_INFORMATICS_JOB = Path(__file__).with_name("fixtures").joinpath(
    "aquatic_informatics_senior_software_engineer.txt"
).read_text(encoding="utf-8")
CORITY_JOB = Path(__file__).with_name("fixtures").joinpath(
    "cority_senior_software_engineer.txt"
).read_text(encoding="utf-8")
LOGISENSE_JOB = Path(__file__).with_name("fixtures").joinpath(
    "logisense_software_developer.txt"
).read_text(encoding="utf-8")
AUTOSCOUT24_JOB = Path(__file__).with_name("fixtures").joinpath(
    "autoscout24_senior_software_engineer.txt"
).read_text(encoding="utf-8")
MAINTAINX_BACKEND_PLATFORM_JOB = Path(__file__).with_name("fixtures").joinpath(
    "maintainx_backend_platform_engineer.txt"
).read_text(encoding="utf-8")
MAGNET_FORENSICS_JOB = Path(__file__).with_name("fixtures").joinpath(
    "magnet_forensics_software_engineer.txt"
).read_text(encoding="utf-8")
AZURE_INTEGRATION_JOB = Path(__file__).with_name("fixtures").joinpath(
    "azure_integration_developer.txt"
).read_text(encoding="utf-8")
ALBERTA_FULL_STACK_JOB = Path(__file__).with_name("fixtures").joinpath(
    "alberta_full_stack_developer.txt"
).read_text(encoding="utf-8")
REMARCABLE_FULL_STACK_JOB = Path(__file__).with_name("fixtures").joinpath(
    "remarcable_full_stack_software_engineer.txt"
).read_text(encoding="utf-8")

DOTNET_SOLUTIONS_ARCHITECT_JOB = """
Position Summary
Lead architecture strategy and solution architecture for enterprise-scale .NET
applications, guiding multiple engineering teams through technical roadmaps and
architectural decisions. Define architecture frameworks, architectural
standards, and engineering best practices.

Responsibilities
Modernize legacy applications into cloud-native solutions in Microsoft Azure.
Build distributed systems with microservices, APIs, API design, and
event-driven architecture. Lead cloud migration planning, CI/CD, DevOps,
automated testing, production support rotations, and incident management.
Partner with product, engineering, and implementation teams in Agile and Scrum.
Provide architectural leadership and technical oversight to multiple teams.
Champion AI-first development using GitHub Copilot, Claude, and Cursor. Build
agentic customer-facing applications using Azure AI Foundry and Open AI, with
orchestration, RAG, retrieval grounding, and MCP server design.

Qualifications
Experience with .NET, Azure architecture, software design patterns, and
enterprise SaaS products. Financial services, insurance, annuity, and wealth
management platforms are relevant domains. Strong communication and stakeholder
management skills.

Benefits
Unlimited PTO and subsidized healthcare.
"""

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

BALLYS_QA_JOB = """
About the role
Own and evolve the test strategy and partner with Engineers, Product Managers,
and stakeholders to build and approve smart, risk-based test plans. Lead
end-to-end quality efforts and build dashboards, metrics, and KPIs to measure
quality and release health. Improve QA processes, tools, and frameworks.
Support testing, troubleshooting, bug triage, prioritization, and defect
management, with leadership, coaching, and continuous improvement.

Role requirements
Deep understanding of QA methodologies: Unit, API, UI, Integration,
Performance, and E2E testing. Experience with CI/CD pipelines such as Jenkins,
GitLab CI/CD, and GoCD. Experience testing both web and mobile applications.
Turn business requirements into clear, testable scenarios. Excellent
communication, stakeholder influence, ownership, analytical and
problem-solving skills, and cross-functional collaboration.
"""

INVESCO_SENIOR_QE_JOB = """
About the role
Senior Software Quality Engineer for the Finance domain. Lead complex test
strategies, improve automation maturity, and mentor junior analysts.

Responsibilities
Expertise in Test Planning & Strategy, Tests Design, Test Environment Setup,
Test Data Setup, Defect Management & Configuration Management. Experience with
Microsoft SQL, Snowflake, and Postgres databases, including creating stored
procedures, views, and tables. Test Master Data Management systems and execute
tests against large data sets. Perform root cause analysis and use the Unix
command line. Use AWS S3, Secrets Manager, and AWS cost models. Monitor
application logs, prepare detailed status reports, and follow the Bug Life
Cycle. Validate backend data and use AutoSys, Airflow, and Stonebranch UAC.
Apply Python, Agile methodology, daily Test Metrics, and postproduction release
checkout. Test automation experience and knowledge of Alteryx, Informatica,
DBT, and Bit Bucket are advantageous.

Requirements
Software quality assurance and software testing experience. Financial services
or Asset Management industry experience is preferred. Oracle Fusion Cloud ERP
and EPM experience.
"""

KUMARAN_AI_AUTOMATION_JOB = """
About the job
About Us
Kumaran Systems builds AI-enabled enterprise systems.

Key Responsibilities
Develop and maintain robust UI automation frameworks using Selenium with Java.
Design and execute functional, regression, and end-to-end automated tests.
Integrate automation suites with CI/CD pipelines using Jenkins, GitHub Actions,
Azure DevOps, or similar tools. Leverage AI/GenAI tools and coding assistants
such as GitHub Copilot to accelerate test creation, script generation,
debugging, and test analysis. Explore and implement AI-driven testing
approaches, including test-case generation, defect analysis, and automation
optimization. Participate in framework design, code reviews, debugging, and
continuous improvement of automation solutions. Work closely with developers,
QA engineers, and business teams in Agile environments.

Required Skills
6+ years of QA Automation experience. Strong Selenium + Java automation
experience. Hands-on Playwright experience. Good knowledge of API testing,
SQL, Git, and CI/CD. Experience with Jenkins / Azure DevOps / GitHub Actions.
Exposure to GenAI/AI tools for software development and QA. Strong
problem-solving, analytical, and communication skills.
"""

ROBOTICS_FULL_STACK_JOB = """
About the job
Senior Full Stack Developer supporting advanced robotics and space operations technology.

What You'll Do
Design and develop web-based ground control software, simulators and testing tools
supporting robotic systems. Lead complex software/subsystem design and implementation.
Build scalable, maintainable and testable full-stack applications. Participate in
software integration, automated testing and troubleshooting. Conduct technical design
and code reviews. Mentor junior developers and provide technical guidance. Help
establish and improve development standards, tools and processes.

What You Must Have
Full-stack development experience on Windows and/or Linux. Angular, C# / ASP.NET Core,
JavaScript, ReactJS, HTML/CSS and .NET. Relational and NoSQL databases, including
SQL/MSSQL/PostgreSQL, Entity Framework, LINQ, MongoDB/Couchbase and Redis. Automated
software testing, Agile development, technical leadership and communication skills.

Nice to Have
Storybook, SignalR, Playwright, NUnit, TDD/ATDD/BDD, CI/build automation, Python or Lua.
"""

SMART_FACTORY_JOB = """
About the role
The senior full-stack developer builds cloud-native applications for connected
manufacturing operations.

Required skills
Full-stack application development, cloud architecture, React.js, TypeScript,
Node.js, API development, HTML and CSS. REST-based service-oriented architecture
and microservices. Relational and NoSQL databases, data integrations, cloud
services and cloud migrations. Containers and container lifecycle management,
DevOps practices, CI/CD, serverless technologies, monitoring and management,
security and networking concepts, and storage and analytics technologies.

Our stack
React and TypeScript; Node.js, Python, .NET/C#; AWS and Microsoft Azure; Databricks.

Preferred experience
Databricks, MQTT, Kafka, industrial IoT / Industry 4.0, event-driven architectures,
Azure Active Directory / Microsoft Entra ID, OAuth 2.0, Infrastructure-as-a-Service,
Platform-as-a-Service, Software-as-a-Service, Function-as-a-Service, JavaScript,
C#, Python, C++, the Cloud Shared Responsibility Model, and manufacturing
technology environments.

Responsibilities
Develop IoT-enabled manufacturing applications for production monitoring, quality
inspection, and factory digitization. Design, document, and unit test cloud-based
applications. Use GitHub and Confluence, troubleshoot production issues, monitor
application performance, guide architecture and design decisions, provide technical
direction, mentor junior developers, and manage source control.
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

SENIOR_CUSTOMER_CENTERED_DOTNET_JOB = """
Duties and Responsibilities
Apply Customer-Centered Design and Customer-Centered Problem Solving. Build
customer-centered full-stack applications with C#, .NET, SQL Server,
Blazor, Visual Studio, RESTful and SOAP APIs. Apply secure coding, privacy,
vulnerability remediation, dependency management, and appropriate access
controls throughout the SDLC. Use AI agents for spec-driven development (SDD),
reusable AI skill building, prompt engineering, code generation, automated code
review, test generation, documentation support, and ticket triage.

Design multi-tier and distributed application architecture with relational data
modeling and backward compatibility. Use query tuning and code optimization to
reduce API latency and accelerate data pipeline processing. Perform root-cause
analysis, work estimation, risk and dependency management, knowledge sharing,
mentoring, and formal or informal training.

Preferred Capabilities
Build Azure-native applications with CI/CD, security, monitoring, and
observability. Design ETL/ELT data pipelines, lakehouse and medallion
architecture with Snowflake or Databricks. Apply data mapping, data dictionaries,
and end-to-end data lineage. Manage image repositories and content tags, and
automatically validate media files.
"""


class ExtractionTests(unittest.TestCase):
    def test_anthropic_inference_role_extracts_inference_and_fleet_skills(self):
        job = """
        Build distributed systems that serve models through inference
        infrastructure. Develop intelligent request routing, load balancing,
        traffic management, autoscaling, and workload orchestration. Build
        production-grade deployment pipelines for releasing new models and
        provide machine learning systems with LLM inference optimization,
        batching, and caching strategies. Integrate AI accelerator platforms,
        analyze observability data, and manage multi-region deployments and
        geographic routing. Experience with Kubernetes, AWS, GCP, Azure, Python,
        and Rust.
        """
        skills = set(extract_skills(job, source="job_description"))
        expected = {
            "distributed systems", "inference systems", "request routing",
            "load balancing", "traffic management", "autoscaling",
            "workload orchestration", "model deployment pipelines",
            "machine learning systems", "llm inference optimization",
            "batch inference", "caching", "ai accelerators", "observability",
            "multi-region deployment", "geographic routing", "kubernetes",
            "amazon web services", "google cloud platform", "microsoft azure",
            "python", "rust",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_dotnet_solutions_architect_job_extracts_architecture_and_ai_skills(self):
        skills = set(extract_skills(
            DOTNET_SOLUTIONS_ARCHITECT_JOB, source="job_description"
        ))
        expected = {
            ".net", "agile", "ai-assisted software development", "annuity products",
            "api development", "automated testing", "azure ai foundry",
            "cloud migration", "cloud native", "claude", "ci/cd",
            "distributed systems", "devops", "event-driven architecture",
            "financial services", "github copilot", "incident response",
            "insurance", "leadership", "microservices", "microsoft azure",
            "model context protocol", "openai", "product roadmap planning",
            "production support", "retrieval-augmented generation", "scrum",
            "software architecture", "software as a service",
            "software design patterns", "stakeholder management",
            "technical standards", "wealth management",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)
        self.assertNotIn("unlimited pto", skills)

    def test_customer_centered_dotnet_job_extracts_ai_data_and_security_skills(self):
        skills = set(extract_skills(
            SENIOR_CUSTOMER_CENTERED_DOTNET_JOB, source="job_description"
        ))
        expected = {
            ".net", "access control", "ai agents", "ai skill development",
            "automated code review", "automated test generation", "backward compatibility",
            "blazor", "c#", "ci/cd", "cloud native", "code generation",
            "content tagging", "customer-centered design",
            "customer-centered problem solving", "data dictionary", "data lineage", "data mapping",
            "data pipeline development", "data privacy", "databricks",
            "dependency management", "distributed systems", "elt", "etl",
            "full stack development", "medallion architecture",
            "media asset management", "media validation", "microsoft azure",
            "microsoft sql server", "observability", "performance optimization",
            "prompt engineering", "query performance optimization", "rest api",
            "risk management", "root cause analysis", "snowflake", "soap",
            "software architecture", "software development lifecycle",
            "software project estimation", "spec-driven development",
            "technical mentoring", "technical writing", "ticket management",
            "visual studio", "vulnerability management",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_azure_integration_role_extracts_cloud_platform_and_delivery_skills(self):
        skills = set(extract_skills(AZURE_INTEGRATION_JOB, source="job_description"))
        expected = {
            ".net", "api development", "api security", "arm template", "azure devops",
            "bicep", "c#", "ci/cd", "cloud compliance", "cloud identity security",
            "cloud native", "cloud security", "data workflow orchestration",
            "distributed systems", "environment promotion", "event-driven architecture",
            "git", "infrastructure as code", "messaging systems", "microsoft azure",
            "microsoft azure api management", "microsoft azure application insights",
            "microsoft azure data factory", "microsoft azure event grid",
            "microsoft azure event hub", "microsoft azure functions",
            "microsoft azure log analytics", "microsoft azure logic apps",
            "microsoft azure monitor", "microsoft azure service bus",
            "microsoft azure web apps", "monitoring", "network security",
            "performance optimization",
            "production support", "release automation", "resilience engineering",
            "rest api", "root cause analysis", "software development",
            "software scalability", "source control", "terraform", "troubleshooting",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_alberta_full_stack_role_extracts_platform_delivery_and_design_skills(self):
        skills = set(extract_skills(ALBERTA_FULL_STACK_JOB, source="job_description"))
        expected = {
            ".net", "agile", "ai-assisted software development",
            "ai output validation", "application maintenance", "automation",
            "backend software development", "c#", "ci/cd", "cloud computing",
            "cloud services development", "computer science fundamentals",
            "cross-functional collaboration",
            "data privacy", "debugging", "defect management", "devops",
            "enterprise application development", "financial management systems",
            "frontend software development", "full stack development",
            "human-centered design", "incident response", "javascript", "nosql",
            "payment systems", "problem solving", "process improvement",
            "production support", "professional judgment", "react",
            "relational database operations", "relational databases",
            "requirements analysis", "service design", "software architecture",
            "software design patterns", "software development",
            "software development lifecycle", "software testing",
            "software maintainability", "software reliability",
            "software scalability", "sql", "stakeholder management", "teamwork",
            "technical communication", "technical standards", "troubleshooting",
            "vendor management",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_ambiguous_azure_integration_terms_require_cloud_context(self):
        skills = set(extract_skills(
            "He injured his arm near the service bus. The factory uses a paper data grid. "
            "A manager performs API management reviews."
        ))
        self.assertFalse({
            "arm template", "microsoft azure data factory", "microsoft azure event grid",
            "microsoft azure api management",
        } & skills)

    def test_l3harris_job_extracts_communications_system_skills(self):
        skills = set(extract_skills(L3HARRIS_JOB, source="job_description"))
        expected = {
            ".net core", "akka toolkit", "analytical skills", "angular", "asp.net",
            "asp.net signalr", "c#", "client-server architecture", "computer networking",
            "cqrs", "cross-functional collaboration", "debugging", "distributed computing",
            "distributed systems", "fault tolerance", "high availability", "http",
            "independent work", "message queues", "microservices", "military standards",
            "military systems", "mysql", "network protocols", "object-oriented programming",
            "organizational skills", "presentation skills", "problem solving", "rabbitmq",
            "real-time systems", "relational databases", "rest api", "snmp",
            "software architecture", "software design", "systems engineering",
            "systems integration", "technical communication", "technical demonstrations",
            "technical research", "transmission control protocol", "vue",
            "web application development", "websocket",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)
        self.assertNotIn("coaching", skills)
        self.assertNotIn("sales", skills)
        self.assertNotIn("high availability", extract_skills(
            "The hotel says that a room is highly available this week."
        ))

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

    def test_ballys_job_extracts_qa_strategy_delivery_and_tooling_skills(self):
        skills = set(extract_skills(BALLYS_QA_JOB, source="job_description"))
        expected = {
            "api testing", "bug triage", "ci/cd", "coaching", "communication",
            "cross-functional collaboration", "defect management", "end-to-end testing",
            "gocd", "jenkins", "key performance indicator",
            "leadership", "mobile application testing", "ownership", "performance testing",
            "prioritization", "problem solving", "process improvement", "quality metrics",
            "release quality management", "risk-based testing", "software testing",
            "system integration testing", "test case design", "test planning",
            "test strategy", "troubleshooting", "unit testing", "user interface testing",
            "web application testing",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_invesco_senior_qe_job_extracts_data_quality_and_workflow_skills(self):
        skills = set(extract_skills(INVESCO_SENIOR_QE_JOB, source="job_description"))
        expected = {
            "agile", "alteryx", "amazon s3", "amazon web services",
            "apache airflow", "asset management", "automated testing",
            "aws secrets manager", "bitbucket", "ca unicenter autosys job management",
            "configuration management", "data validation", "finops",
            "dbt", "defect lifecycle management", "defect management",
            "enterprise performance management", "enterprise resource planning",
            "financial services", "informatica", "large-scale data testing",
            "log analysis", "master data management", "microsoft sql server", "oracle fusion cloud",
            "postgresql", "python", "quality engineering", "quality metrics",
            "release validation", "root cause analysis", "snowflake",
            "software testing", "status reporting", "stonebranch universal automation center",
            "stored procedures", "technical mentoring", "test case design",
            "test data management", "test environment management", "test planning",
            "test strategy", "unix",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_kumaran_ai_automation_role_extracts_testing_and_ai_skills(self):
        skills = set(extract_skills(KUMARAN_AI_AUTOMATION_JOB, source="job_description"))
        expected = {
            "agile", "ai-driven testing", "api testing", "automated test generation",
            "automated testing", "azure devops", "ci/cd", "code review",
            "communication", "debugging", "defect analysis", "end-to-end testing",
            "functional testing", "git", "github actions", "github copilot", "java",
            "jenkins", "playwright", "problem solving", "process improvement",
            "regression testing", "selenium", "sql", "test analysis",
            "test automation frameworks", "test automation optimization",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_robotics_full_stack_role_extracts_domain_stack_and_methods(self):
        skills = set(extract_skills(ROBOTICS_FULL_STACK_JOB, source="job_description"))
        expected = {
            ".net", "acceptance test-driven development", "agile", "angular",
            "asp.net core", "asp.net signalr", "automated testing", "bdd",
            "build automation", "c#", "code review", "communication", "couchbase",
            "css", "entity framework", "full stack development",
            "ground control software", "html", "javascript", "leadership", "linq",
            "linux", "lua", "mongodb", "mssql", "nosql", "nunit", "playwright",
            "postgresql", "process improvement", "python", "react", "redis",
            "relational databases", "robotics", "simulation software development",
            "software design", "software maintainability", "software scalability",
            "space operations", "sql", "storybook", "systems integration",
            "technical mentoring", "test-driven development", "troubleshooting",
            "windows",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_smart_factory_job_extracts_cloud_iot_and_full_stack_skills(self):
        skills = set(extract_skills(SMART_FACTORY_JOB, source="job_description"))
        expected = {
            ".net", "amazon web services", "apache kafka", "api development",
            "c#", "c++", "ci/cd", "cloud migration",
            "cloud shared responsibility model", "cloud native",
            "cloud services development", "computer networking", "confluence",
            "container lifecycle management", "containerization", "css", "cybersecurity",
            "data analysis", "data storage", "databricks", "devops",
            "event-driven architecture", "full stack development",
            "function as a service", "github", "html", "iot", "javascript",
            "leadership", "microservices", "microsoft azure",
            "microsoft entra id", "monitoring", "mqtt", "node.js", "nosql",
            "oauth", "platform as a service", "public cloud architecture",
            "python", "react", "relational databases", "serverless",
            "service-oriented architecture", "smart manufacturing",
            "software architecture", "software as a service",
            "software development", "source control", "technical mentoring",
            "typescript", "unit test",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_netbrain_role_extracts_support_saas_dotnet_and_cs_skills(self):
        skills = set(extract_skills(NETBRAIN_JOB, source="job_description"))
        expected = {
            ".net", "ai-assisted software development", "algorithm design",
            "amazon cloudwatch", "amazon rds", "amazon sns", "amazon sqs",
            "amazon web services", "asp.net core", "aws lambda", "c#",
            "communication", "computer science fundamentals", "customer experience",
            "cross-functional collaboration", "customer issue resolution",
            "customer support", "data structures", "database schema design",
            "domain-driven design", "enterprise application development",
            "entity framework core", "file systems", "full stack development",
            "github copilot", "independent work", "memory optimization",
            "multi-tenant architecture", "multithreading", "object-oriented programming",
            "on-call support", "performance optimization", "postgresql",
            "product improvement", "production support",
            "product roadmap planning", "query performance optimization",
            "requirements analysis", "root cause analysis", "software architecture",
            "software as a service", "software design patterns", "software reliability",
            "software scalability", "software testing", "stakeholder management",
            "subject matter expertise", "technical investigation", "technical mentoring", "technical research",
            "troubleshooting", "usability",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_bettingjobs_role_extracts_real_time_dotnet_and_react_skills(self):
        skills = set(extract_skills(BETTINGJOBS_JOB, source="job_description"))
        expected = {
            ".net", ".net core", "amazon web services", "analytical skills",
            "angular", "apache kafka", "automated testing", "caching", "ci/cd",
            "cloud native", "code review", "concurrent programming", "conflict resolution",
            "containerization", "distributed systems", "grpc",
            "high-throughput systems", "independent work", "kubernetes",
            "leadership", "log analysis", "low-latency systems", "message queues",
            "microsoft azure", "monitoring", "observability", "opentelemetry",
            "optimistic ui updates", "performance optimization", "problem solving",
            "production support", "rabbitmq", "react", "real-time systems", "redis",
            "relational databases", "rest api", "risk management",
            "server-sent events", "software architecture", "software reliability",
            "software scalability", "technical mentoring", "typescript", "vue",
            "websocket",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_bluehost_role_extracts_ai_native_backend_and_governance_skills(self):
        skills = set(extract_skills(BLUEHOST_AI_BACKEND_JOB, source="job_description"))
        expected = {
            "a/b testing", "application metrics", "asynchronous programming", "chroma",
            "ci/cd", "code provenance", "code review",
            "cost-aware routing", "customer data privacy", "data modeling", "database migrations",
            "database schema design", "dependency injection", "distributed tracing",
            "fastapi", "gemini", "langchain", "large language models", "latency monitoring",
            "licensing compliance", "linting", "llm observability", "llm provider integration",
            "multi-agent orchestration", "openai",
            "orm", "pgvector", "prompt data governance", "python",
            "query performance optimization", "relational databases",
            "responsible ai", "sqlalchemy", "sqlmodel",
            "retrieval-augmented generation", "rest api", "semantic kernel",
            "software packaging", "structured logging", "type checking", "type hints",
            "vector databases", "vertical slice architecture", "websocket",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_real_time_payments_role_extracts_azure_and_payments_skills(self):
        skills = set(extract_skills(REAL_TIME_PAYMENTS_JOB, source="job_description"))
        expected = {
            ".net core", "api", "api development", "banking", "communication",
            "microsoft azure", "microsoft azure application insights",
            "microsoft azure cosmos db", "microsoft azure event hub",
            "microsoft azure functions", "microsoft azure key vault",
            "microsoft azure service bus", "payment systems", "redis", "sql",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_promach_role_extracts_cloud_architecture_and_manufacturing_skills(self):
        skills = set(extract_skills(PROMACH_CLOUD_ARCHITECT_JOB, source="job_description"))
        expected = {
            ".net", "backend software development", "ci/cd", "cloud infrastructure",
            "cloud native", "cloud operations", "cloud security",
            "cloud-agnostic architecture", "data flow design", "data ingestion",
            "data pipeline development", "database scalability", "database schema design",
            "decision-making under ambiguity", "distributed systems",
            "failure mode analysis", "high-volume data processing",
            "hybrid cloud integration", "industrial systems", "infrastructure as code",
            "iot", "manufacturing systems", "microsoft azure", "microsoft sql server",
            "monitoring", "multi-tenant architecture", "observability",
            "public cloud architecture", "query performance optimization",
            "resilience engineering", "service boundary design", "software architecture",
            "software as a service", "software maintainability", "software reliability",
            "software scalability", "storage architecture", "technical communication",
            "technical writing", "technology evaluation", "tenant data isolation",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_multi_tenant_saas_cloud_architect_extracts_strategy_and_build_skills(self):
        skills = set(extract_skills(
            MULTI_TENANT_SAAS_CLOUD_ARCHITECT_JOB, source="job_description"
        ))
        expected = {
            ".net", "amazon web services", "backend software development", "ci/cd",
            "cloud cost analysis", "cloud infrastructure", "cloud platform strategy",
            "cloud security", "customer discovery", "customer-facing reporting",
            "data flow design", "data ingestion", "data pipeline development",
            "database scalability", "database schema design", "distributed systems",
            "engineering team building", "failure mode analysis", "google cloud platform",
            "high-volume data processing", "hybrid cloud integration", "industrial systems",
            "infrastructure as code", "iot", "manufacturing systems", "microsoft azure",
            "microsoft sql server", "monitoring", "multi cloud strategy",
            "multi-tenant architecture", "on-premises software", "public cloud architecture",
            "query performance optimization", "resilience engineering",
            "service boundary design", "software architecture", "software as a service",
            "software maintainability", "software scalability", "storage architecture",
            "technology evaluation", "tenant data isolation",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_aquatic_informatics_role_extracts_predictive_ai_and_water_skills(self):
        skills = set(extract_skills(AQUATIC_INFORMATICS_JOB, source="job_description"))
        expected = {
            ".net", "agentic software development", "ai-assisted software development",
            "amazon web services", "angular", "artificial intelligence", "c#",
            "cloud native", "cloud operations", "cloud services development", "code review",
            "communication", "data science", "data-intensive applications",
            "database schema design", "development infrastructure", "digital twins",
            "end-to-end testing", "environmental science", "frontend software development",
            "industrial control systems", "iot", "large language model agents",
            "large language models", "machine learning", "microservices", "microsoft azure",
            "oracle", "ownership", "postgresql", "predictive analytics", "process improvement",
            "react", "responsible ai", "sensor anomaly detection", "software scalability",
            "sql", "system integration testing", "technical mentoring",
            "testing framework development", "time series analysis", "troubleshooting",
            "unit testing", "vue", "water treatment systems",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)
        self.assertNotIn("coaching", skills)
        self.assertNotIn("sales", skills)

    def test_cority_role_extracts_dotnet_ai_delivery_and_ehs_skills(self):
        skills = set(extract_skills(CORITY_JOB, source="job_description"))
        expected = {
            ".net", ".net core", ".net framework", "agile", "ai-assisted software development",
            "alerting", "amazon sqs", "amazon web services", "angular",
            "agentic ai frameworks", "apache kafka", "api development",
            "application metrics", "ci/cd", "claude", "code quality", "code review",
            "communication", "containerization", "css", "cursor", "dapper", "debugging",
            "decision-making under ambiguity", "distributed teams", "docker",
            "end-to-end software delivery",
            "entity framework", "environmental health and safety", "github copilot", "html",
            "initiative", "javascript", "large language models", "logging", "message queues",
            "microservices", "microsoft azure", "microsoft sql server", "model context protocol",
            "mongodb", "node.js", "nosql", "observability", "ownership", "postgresql",
            "process improvement", "python", "rabbitmq", "react", "relational databases",
            "requirements analysis",
            "retrieval-augmented generation", "scrum", "software development",
            "software development lifecycle", "software project estimation", "sustainability",
            "technical communication", "technical mentoring", "technical standards",
            "technical writing", "typescript", "vector databases",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)
        self.assertFalse({"go", "http", "see", "solid"} & skills)

    def test_logisense_role_extracts_billing_dotnet_delivery_and_ai_skills(self):
        skills = set(extract_skills(LOGISENSE_JOB, source="job_description"))
        expected = {
            ".net", "agile", "ai output validation", "amazon web services",
            "artificial intelligence", "automated testing",
            "billing and monetization platforms", "c#", "cloud computing",
            "code review", "cross-functional collaboration", "database schema design",
            "debugging", "dependency management", "design review",
            "end-to-end software delivery", "frontend frameworks", "functional testing",
            "initiative", "integration testing", "knowledge transfer",
            "microsoft sql server", "node.js", "ownership", "pair programming",
            "performance optimization", "performance profiling", "process improvement",
            "production support", "quality assurance collaboration",
            "query performance optimization", "regression testing", "requirements analysis",
            "requirements task decomposition", "rest api", "risk communication", "scrum",
            "software design", "software project estimation", "software reliability",
            "subscription billing", "t-sql", "technical communication", "technical debt",
            "technical decision-making", "technical mentoring", "unit testing",
            "usage-based billing",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_magnet_forensics_role_extracts_full_stack_cloud_and_forensics_skills(self):
        skills = set(extract_skills(MAGNET_FORENSICS_JOB, source="job_description"))
        expected = {
            ".net", "adaptability", "agentic ai frameworks",
            "ai-assisted software development", "amazon web services",
            "application security", "automated testing", "aws cdk", "azure devops",
            "backend software development", "c#", "claude", "cloud native",
            "code review", "communication", "component design", "containerization",
            "cross-functional collaboration", "css", "cursor", "data access",
            "debugging", "decision-making under ambiguity", "digital forensics",
            "distributed data stores", "distributed systems", "docker", "elasticsearch",
            "engineering team building", "full stack development", "git", "gitlab",
            "grafana", "graphql", "html", "infrastructure as code", "initiative",
            "jenkins", "jest", "kubernetes", "linux", "message-driven architecture",
            "monitoring", "natural language search", "observability", "opentelemetry",
            "performance optimization", "postgresql", "postgresql jsonb", "prometheus",
            "pytest", "python", "react", "redis", "regulated software development",
            "requirements analysis", "requirements task decomposition",
            "responsive web design", "rest api", "search indexing", "software architecture",
            "software as a service", "software maintainability", "software modularity",
            "software project estimation", "state management", "troubleshooting",
            "typescript", "web development", "xunit",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)
        self.assertFalse({"natural", "rest"} & skills)

    def test_remarcable_role_extracts_full_stack_database_and_integration_skills(self):
        skills = set(extract_skills(
            REMARCABLE_FULL_STACK_JOB, source="job_description"
        ))
        expected = {
            "ai-assisted software development", "angular", "api development",
            "asynchronous programming", "automated testing",
            "backend software development", "background job processing", "claude",
            "cloud infrastructure", "code generation", "code quality", "code review",
            "component design", "containerization", "cursor",
            "customer issue resolution", "data modeling", "data synchronization",
            "database indexing", "database normalization", "database schema design",
            "debugging", "django", "docker", "document data extraction",
            "email processing", "fastapi", "feature engineering", "flask",
            "frontend frameworks", "full stack development", "github copilot",
            "graphql", "mysql", "ocr", "orm", "ownership",
            "performance optimization", "postgresql", "production support", "python",
            "query performance optimization", "race condition debugging", "react",
            "relational databases", "rest api", "software architecture",
            "software as a service", "software deployment", "software reliability",
            "sql", "state management", "systems integration", "technical standards",
            "terraform", "troubleshooting", "unit testing", "vue", "webhooks",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_magnet_terms_do_not_promote_unrelated_natural_cdk_or_access_language(self):
        skills = set(extract_skills(
            "The natural environment is changing. Researchers studied CDK proteins "
            "in regulated markets. A customer submitted a data access request."
        ))
        self.assertFalse({
            "natural", "aws cdk", "regulated software development", "data access",
        } & skills)

    def test_autoscout24_role_extracts_transformation_risk_and_genai_skills(self):
        skills = set(extract_skills(AUTOSCOUT24_JOB, source="job_description"))
        expected = {
            ".net", ".net core", "agile", "ai-assisted software development",
            "artificial intelligence", "code quality", "code review",
            "cross-functional collaboration", "debugging", "developer productivity",
            "devops", "end-to-end software delivery", "fraud detection",
            "generative artificial intelligence", "leadership",
            "legacy system modernization", "next.js", "observability", "ownership",
            "performance engineering", "problem solving", "production operations",
            "react", "resilience engineering", "risk analysis", "software architecture",
            "software development lifecycle", "software maintainability",
            "software modularity", "software reliability", "software scalability",
            "software testability", "software testing", "system design",
            "technical debt", "technical decision-making", "technical mentoring",
            "typescript", "workflow automation",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)
        self.assertFalse({"focus", "set", "velocity", "development infrastructure",
                          "performance testing"} & skills)

    def test_autoscout24_terms_do_not_promote_unrelated_language(self):
        skills = set(extract_skills(
            "The set focused on velocity. The modularity theorem was discussed. "
            "They built systems that matter and reviewed a fraud news story."
        ))
        self.assertFalse({
            "focus", "set", "velocity", "software modularity",
            "development infrastructure", "fraud detection",
        } & skills)

    def test_logisense_domain_terms_do_not_match_generic_business_language(self):
        skills = set(extract_skills(
            "The subscription was renewed after usage increased. The team paired socks, "
            "reviewed a design, checked a bill, and discussed monetization."
        ))
        self.assertFalse({
            "usage-based billing", "subscription billing",
            "billing and monetization platforms", "pair programming", "design review",
        } & skills)

    def test_specialized_aquatic_terms_do_not_match_unrelated_words(self):
        skills = set(extract_skills(
            "The twins watched a television series and controlled the water. "
            "An agent predicted that the sensor would need treatment."
        ))
        self.assertFalse({
            "digital twins", "time series analysis", "industrial control systems",
            "water treatment systems", "large language model agents",
            "predictive analytics", "sensor anomaly detection",
        } & skills)

    def test_public_job_market_samples_extract_recurring_skills(self):
        for role, (description, expected) in PUBLIC_JOB_SAMPLES.items():
            with self.subTest(role=role):
                skills = set(extract_skills(description, source="job_description"))
                self.assertTrue(expected.issubset(skills), expected - skills)

    def test_maintainx_role_extracts_api_platform_and_integration_skills(self):
        skills = set(extract_skills(
            MAINTAINX_BACKEND_PLATFORM_JOB, source="job_description"
        ))
        expected = {
            "api development", "api error handling", "api filtering",
            "api key authentication", "api pagination", "api platforms",
            "api versioning", "application metrics", "authentication",
            "authorization", "automated onboarding", "backward compatibility",
            "batch processing", "bulk operations", "connector development",
            "contract testing", "credential management", "data migration",
            "data synchronization", "developer debugging tools",
            "developer documentation", "developer experience",
            "distributed systems", "distributed tracing",
            "environment configuration", "integration marketplaces",
            "integration platform as a service", "integration security",
            "least privilege", "logging", "oracle e-business suite",
            "quality gates", "release automation", "sap cloud platform",
            "sap ecc", "sdk development", "service level indicators",
            "service level objectives", "shared library development",
            "software auditability", "software operability",
            "software scaffolding", "token rotation", "tray.io", "webhooks",
            "workato", "zapier",
        }
        self.assertTrue(expected.issubset(skills), expected - skills)

    def test_maintainx_ambiguous_terms_require_technical_context(self):
        skills = set(extract_skills(
            "We filtered water, read a paginated book, carried a lunch tray, "
            "used scaffolding at a construction site, and inspected a batch of cookies."
        ))
        self.assertFalse({
            "api filtering", "api pagination", "batch processing",
            "software scaffolding", "tray.io",
        } & skills)

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
            "team, head, company, rate, care, member, engineering, reports. "
            "I can clarify how life can make us perform better on example.com."
        ), [])

    def test_work_progress_and_interview_words_are_not_skills(self):
        self.assertEqual(extract_skills(
            "I work on works in progress and prepare for an interview."
        ), [])

    def test_ready_win_wins_and_web_are_not_skills_without_technical_context(self):
        self.assertEqual(extract_skills(
            "We are ready to win. Our team wins by making the web better."
        ), [])
        self.assertEqual(extract_skills("Ready, win, wins, web"), [])

    def test_wins_networking_acronym_requires_network_context(self):
        self.assertIn(
            "wins",
            extract_skills("Maintained WINS servers for NetBIOS name resolution."),
        )

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
        skills = extract_skills("GitHub, JavaScripted, SQLAlchemy, Pythonic")
        self.assertEqual(skills, ["github", "sqlalchemy"])
        self.assertNotIn("javascript", skills)
        self.assertNotIn("python", skills)
        self.assertNotIn("sql", skills)

    def test_imported_skill_abbreviations_resolve_to_canonical_names(self):
        self.assertEqual(
            extract_skills("CQL, VHDL, SSMS, VSTS"),
            [
                "cassandra query language",
                "sql server management studio",
                "vhsic hardware description language",
                "visual studio team service",
            ],
        )

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
        return self.client.post('/extract_skills', json={
            "job_description": job,
            "resume": resume,
        })

    def test_existing_response_fields_and_explainable_matches(self):
        response = self.post(JOB, RESUME)
        self.assertEqual(response.status_code, 200)
        self.assertIn("ats-optimizer;dur=", response.headers["Server-Timing"])
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

    def test_oversized_request_returns_json_413(self):
        response = self.post("Python " * 100_000, RESUME)
        self.assertEqual(response.status_code, 413)
        self.assertEqual(response.get_json(), {"error": "Request body is too large"})

    def test_malformed_json_and_wrong_content_type_return_400(self):
        self.assertEqual(self.client.post('/extract_skills', data='{', content_type='application/json').status_code, 400)
        self.assertEqual(self.client.post('/extract_skills', data='text').status_code, 400)

    def test_health_and_cors_remain_available(self):
        self.assertEqual(self.client.get('/health').get_json(), {"status": "ok"})
        self.assertEqual(self.client.get('/access_key').status_code, 404)
        response = self.client.options('/extract_skills', headers={
            "Origin": "http://localhost:5173", "Access-Control-Request-Method": "POST",
        })
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.headers['Access-Control-Allow-Origin'], 'http://localhost:5173')
        self.assertEqual(response.headers['Access-Control-Allow-Credentials'], 'true')

if __name__ == '__main__':
    unittest.main()
