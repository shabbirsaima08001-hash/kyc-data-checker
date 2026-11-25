"""KYC Data Checker
Reads a CSV of customers and checks the data quality.
Checks: missing data, age under 18, expired ID, wrong email, wrong ID number.
Output: a report in the terminal + report.csv
"""
import re
import sys
import pandas as pd
from datetime import date

REQUIRED = ["customer_id", "full_name", "date_of_birth", "email",
            "country", "id_number", "id_expiry_date"]
EMAIL_PATTERN = re.compile(r"^[\w.+-]+@[\w-]+\.[\w.-]+$")
ID_PATTERN = re.compile(r"^[A-Z]{2}\d{7}$")   # example format: 2 letters + 7 numbers
MIN_AGE = 18


def calculate_age(birth: date, today: date) -> int:
    return today.year - birth.year - ((today.month, today.day) < (birth.month, birth.day))


def check_customer(row: pd.Series, today: date) -> list:
    """Returns a list of problems for one customer."""
    problems = []

    # 1. Missing data
    for col in REQUIRED:
        value = row.get(col)
        if pd.isna(value) or str(value).strip() == "":
            problems.append(f"Missing {col}")

    # 2. Date of birth + age
    dob_text = row.get("date_of_birth")
    if pd.notna(dob_text) and str(dob_text).strip() != "":
        dob = pd.to_datetime(dob_text, errors="coerce")
        if pd.isna(dob):
            problems.append("Invalid date of birth format")
        elif calculate_age(dob.date(), today) < MIN_AGE:
            problems.append("Customer is under 18")

    # 3. ID expiry
    exp_text = row.get("id_expiry_date")
    if pd.notna(exp_text) and str(exp_text).strip() != "":
        exp = pd.to_datetime(exp_text, errors="coerce")
        if pd.isna(exp):
            problems.append("Invalid ID expiry date format")
        elif exp.date() < today:
            problems.append("ID document is expired")

    # 4. Email format
    email = row.get("email")
    if pd.notna(email) and str(email).strip() != "" and not EMAIL_PATTERN.match(str(email)):
        problems.append("Wrong email format")

    # 5. ID number format
    id_number = row.get("id_number")
    if pd.notna(id_number) and str(id_number).strip() != "" and not ID_PATTERN.match(str(id_number)):
        problems.append("Wrong ID number format")

    return problems


def main(path: str = "customers.csv") -> None:
    df = pd.read_csv(path, dtype=str)
    today = date.today()

    results = []
    for _, row in df.iterrows():
        problems = check_customer(row, today)
        results.append({
            "customer_id": row["customer_id"],
            "status": "FAIL" if problems else "PASS",
            "problems": "; ".join(problems),
        })

    report = pd.DataFrame(results)
    report.to_csv("report.csv", index=False)

    failed = report[report["status"] == "FAIL"]
    print("=" * 50)
    print("KYC DATA CHECK REPORT")
    print("=" * 50)
    print(f"Customers checked : {len(report)}")
    print(f"Passed            : {len(report) - len(failed)}")
    print(f"Failed            : {len(failed)}")
    print("-" * 50)
    for _, r in failed.iterrows():
        print(f"{r['customer_id']}: {r['problems']}")
    print("-" * 50)
    print("Full report saved in report.csv")


if __name__ == "__main__":
    main(sys.argv[1] if len(sys.argv) > 1 else "customers.csv")
