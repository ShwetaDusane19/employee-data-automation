import pandas as pd
import numpy as np
import random
from datetime import datetime, timedelta
import os

# Configurations
NUM_RECORDS = 500
departments = ['Engineering', 'Data Analytics', 'HR', 'Marketing', 'Finance', 'Sales']
first_names = ['Aarav', 'Ananya', 'Rohan', 'Priya', 'Vikram', 'Neha', 'Siddharth', 'Kavya', 'Amit', 'Sneha', 'Rajesh', 'Pooja']
last_names = ['Sharma', 'Verma', 'Patel', 'Nair', 'Singh', 'Kulkarni', 'Joshi', 'Deshmukh', 'Gupta', 'Rao']

data = []

for i in range(1, NUM_RECORDS + 1):
    emp_id = f"E{1000 + i}"
    fname = random.choice(first_names)
    lname = random.choice(last_names)
    dept = random.choice(departments)
    
    # Inject dirty formatting (extra spaces)
    if random.random() < 0.15:
        fname = f"  {fname} "
        dept = f" {dept}  "
        
    # Inject bad email or missing email
    if random.random() < 0.05:
        email = f"{fname.strip().lower()}.{lname.lower()}invalid.com" # Missing @
    elif random.random() < 0.05:
        email = np.nan # Missing email
    else:
        email = f"{fname.strip().lower()}.{lname.lower()}@company.com"
        
    # Joining date variations
    start_date = datetime(2018, 1, 1)
    random_days = random.randint(0, 2500)
    join_dt = start_date + timedelta(days=random_days)
    
    if random.random() < 0.10:
        joining_date = join_dt.strftime("%d/%m/%Y") # DD/MM/YYYY format
    else:
        joining_date = join_dt.strftime("%Y-%m-%d") # YYYY-MM-DD standard
        
    # Salary & bad salary flags
    if random.random() < 0.04:
        base_salary = -random.randint(30000, 80000) # Invalid negative salary
    else:
        base_salary = random.randint(45000, 150000)
        
    data.append({
        'emp_id': emp_id,
        'first_name': fname,
        'last_name': lname,
        'email': email,
        'department': dept,
        'joining_date': joining_date,
        'base_salary': base_salary
    })

df = pd.DataFrame(data)

# Inject Duplicates (~5% duplicated rows)
duplicates = df.sample(frac=0.05, random_state=42)
df = pd.concat([df, duplicates], ignore_index=True)

# Shuffle dataset
df = df.sample(frac=1, random_state=42).reset_index(drop=True)

# Save to data/raw directory
os.makedirs("data/raw",exist_ok=True)
df.to_csv("data/raw/employees_raw.csv", index=False)
print(f"Successfully generated {len(df)} realistic employee records in 'data/raw/employees_raw.csv'!")