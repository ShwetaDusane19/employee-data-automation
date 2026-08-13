import pandas as pd
import numpy as np
import os

def process_employee_data(input_path, clean_output_path, exception_output_path):
    print("🚀 Starting Data Processing Pipeline...")
    
    # 1. Ingest Raw Data
    df = pd.read_csv(input_path)
    initial_total = len(df)
    print(f"📥 Loaded {initial_total} raw records.")

    # 2. String Hygiene: Strip leading/trailing whitespaces
    string_cols = df.select_dtypes(include=['object']).columns
    for col in string_cols:
        df[col] = df[col].astype(str).str.strip()

    # 3. Handle Duplicates
    # Identify duplicate rows based on emp_id before dropping them
    duplicate_mask = df.duplicated(subset=['emp_id'], keep='first')
    duplicates_df = df[duplicate_mask].copy()
    duplicates_df['issue_reason'] = "Duplicate Employee ID"
    
    # Keep only primary records
    df_dedup = df.drop_duplicates(subset=['emp_id'], keep='first').copy()
    print(f"🧹 Removed {len(duplicates_df)} duplicate records.")

    # 4. Standardise Date Format
    df_dedup['joining_date'] = pd.to_datetime(df_dedup['joining_date'], dayfirst=True, errors='coerce')

    # 5. Business Validation Rules
    exceptions = []
    valid_indices = []

    for idx, row in df_dedup.iterrows():
        reasons = []
        
        # Rule A: Base Salary Validation
        try:
            salary = float(row['base_salary'])
            if salary <= 0:
                reasons.append("Invalid Base Salary (<= 0)")
        except (ValueError, TypeError):
            reasons.append("Non-numeric Salary")

        # Rule B: Email Format & Null Check
        email_str = str(row['email'])
        if pd.isna(row['email']) or email_str == 'nan' or '@' not in email_str or not email_str.endswith('.com'):
            reasons.append("Missing or Invalid Email Format")

        # Rule C: Joining Date Validity Check
        if pd.isna(row['joining_date']):
            reasons.append("Unparseable Joining Date")

        # Route to Valid or Exception
        if reasons:
            row_dict = row.to_dict()
            row_dict['issue_reason'] = " | ".join(reasons)
            exceptions.append(row_dict)
        else:
            valid_indices.append(idx)

    # 6. Build Final DataFrames
    df_clean = df_dedup.loc[valid_indices].copy()
    
    # Combine first_name and last_name for reporting readiness
    df_clean['full_name'] = df_clean['first_name'] + " " + df_clean['last_name']
    
    # Combine rule-based exceptions with structural duplicate records
    df_exceptions = pd.DataFrame(exceptions)
    if not duplicates_df.empty:
        df_exceptions = pd.concat([df_exceptions, duplicates_df], ignore_index=True)

    # Ensure output directory exists
    os.makedirs(os.path.dirname(clean_output_path), exist_ok=True)

    # 7. Save Cleaned & Exception Datasets
    df_clean.to_csv(clean_output_path, index=False)
    df_exceptions.to_csv(exception_output_path, index=False)

    print("\n✅ --- Processing Summary ---")
    print(f"Total Rows Processed : {initial_total}")
    print(f"Valid Clean Records  : {len(df_clean)}")
    print(f"Exception Records    : {len(df_exceptions)}")
    print(f"📁 Clean Data Saved  : {clean_output_path}")
    print(f"📁 Exceptions Saved  : {exception_output_path}")

if __name__ == "__main__":
    RAW_FILE = "data/raw/employees_raw.csv"
    CLEAN_FILE = "data/output/employees_clean.csv"
    EXCEPTION_FILE = "data/output/employees_exceptions.csv"
    
    process_employee_data(RAW_FILE, CLEAN_FILE, EXCEPTION_FILE)