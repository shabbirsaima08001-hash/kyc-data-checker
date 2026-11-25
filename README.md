# KYC Data Checker

A small Python tool that checks customer data quality for **KYC (Know Your Customer)**.
Banks must check that customer data is complete and correct before they open an account. This tool does a simple version of that check.

## What it checks
- Missing data (name, date of birth, email, country, ID number, ID expiry date)
- Customer is under 18
- ID document is expired
- Wrong email format
- Wrong ID number format (example rule: 2 letters + 7 numbers)

## Tools
Python 3, pandas

## How to run
```bash
pip install -r requirements.txt
python generate_data.py     # makes fake customers.csv
python kyc_checker.py       # runs the checks and makes report.csv
```

## Example output
```
KYC DATA CHECK REPORT
Customers checked : 40
Passed            : 24
Failed            : 16
C0004: ID document is expired; Wrong email format
C0008: Missing full_name
C0012: Customer is under 18; ID document is expired
...
```

## Files
| File | What it does |
|---|---|
| `generate_data.py` | Makes fake customer data with some mistakes on purpose |
| `kyc_checker.py` | Main tool: runs the checks and writes the report |
| `customers.csv` | Fake data (no real people) |
| `report.csv` | Result of the check |

## Important
All data is **fake**. Never upload real customer data to GitHub.

## Ideas to improve
- Add more countries and ID formats
- Add a check for duplicate customers
- Add unit tests
