import random

KEYWORDS_POOL = [
    "salary", "bonus", "tax", "employee",
    "department", "finance", "hr", "manager"
]


def generate_record(i):
    # random number of keywords (1 to 3)
    keywords = random.sample(KEYWORDS_POOL, random.randint(1, 3))

    salary = random.randint(30000, 150000)

    return {
        "id": f"user_{i}",
        "keywords": keywords,
        "text": f"Employee Salary: {salary}"
    }


def generate_dataset(size):
    return [generate_record(i) for i in range(size)]