"""Makes a FAKE customer file (customers.csv) with some mistakes on purpose.
All data is fake. No real people."""
import random
import pandas as pd
from datetime import date, timedelta

random.seed(42)
first = ["Marco", "Giulia", "Ahmed", "Sara", "Luca", "Anna", "Ali", "Elena", "Paolo", "Fatima",
         "Chiara", "Omar", "Sofia", "Davide", "Maria", "Hassan", "Laura", "Andrea", "Nadia", "Bruno"]
last = ["Rossi", "Bianchi", "Khan", "Verdi", "Ferrari", "Russo", "Shah", "Conti", "Greco", "Ali"]
countries = ["IT", "IT", "IT", "DE", "FR", "PK", "ES"]

rows = []
for i in range(1, 41):
    name = f"{random.choice(first)} {random.choice(last)}"
    birth = date(1960, 1, 1) + timedelta(days=random.randint(0, 365 * 44))
    expiry = date.today() + timedelta(days=random.randint(-400, 1500))
    rows.append({
        "customer_id": f"C{i:04d}",
        "full_name": name,
        "date_of_birth": birth.isoformat(),
        "email": name.lower().replace(" ", ".") + "@example.com",
        "country": random.choice(countries),
        "id_number": "AB" + str(random.randint(1000000, 9999999)),
        "id_expiry_date": expiry.isoformat(),
    })

df = pd.DataFrame(rows)

# Put some mistakes on purpose, so the checker has something to find
df.loc[3, "email"] = "wrong-email.com"
df.loc[7, "full_name"] = ""
df.loc[11, "date_of_birth"] = (date.today() - timedelta(days=365 * 16)).isoformat()  # minor
df.loc[15, "id_number"] = "12"
df.loc[20, "country"] = ""
df.loc[25, "date_of_birth"] = "31-31-1990"
df.loc[30, "email"] = ""
df.loc[33, "id_expiry_date"] = ""

df.to_csv("customers.csv", index=False)
print("Created customers.csv with", len(df), "fake customers")
