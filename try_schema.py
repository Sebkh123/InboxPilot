from app.schemas import JobPosting
p = JobPosting.model_validate_json(open("samples/expected/posting_01.json", encoding="utf-8").read())
print(p)