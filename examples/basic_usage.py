"""Minimal text analysis example."""

from ats_optimizer import ATSOptimizer


optimizer = ATSOptimizer()
result = optimizer.analyze(
    resume="Python developer with PostgreSQL experience",
    job_description="We need Python, SQL, PostgreSQL, and Docker skills.",
)

print(result.score)
print(result.matched_skills)
print(result.missing_skills)
print(result.to_dict())

