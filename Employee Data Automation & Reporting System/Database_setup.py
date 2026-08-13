import pandas as pd
from sqlalchemy import create_engine
import os
from urllib.parse import quote_plus

# --- Database Configuration ---
DB_USER = "root"          # Replace with your MySQL username
DB_PASSWORD = quote_plus("Sql@2026")  # Replace with your MySQL password
DB_HOST = "localhost"
DB_PORT = "3306"
DB_NAME = "hr_analytics"

def load_to_mysql():
    print("🔌 Connecting to MySQL Database...")
    
    # 1. Create SQLAlchemy Engine
    # Format: mysql+pymysql://user:password@host:port/database
    connection_str = f"mysql+pymysql://{DB_USER}:{DB_PASSWORD}@{DB_HOST}:{DB_PORT}/{DB_NAME}"
    engine = create_engine(connection_str)

    # 2. File Paths
    clean_csv = "data/output/employees_clean.csv"
    exception_csv = "data/output/employees_exceptions.csv"

    # 3. Load & Ingest Clean Employees Data
    if os.path.exists(clean_csv):
        df_clean = pd.read_csv(clean_csv)
        # Ensure joining_date is formatted correctly for SQL DATE type
        df_clean['joining_date'] = pd.to_datetime(df_clean['joining_date']).dt.date
        
        df_clean.to_sql(
            name='clean_employees',
            con=engine,
            if_exists='replace',  # Replaces existing data for a fresh run
            index=False
        )
        print(f"✅ Successfully ingested {len(df_clean)} records into 'clean_employees' table.")
    else:
        print("❌ Error: Clean data file not found.")

    # 4. Load & Ingest Exception Records
    if os.path.exists(exception_csv):
        df_exceptions = pd.read_csv(exception_csv)
        
        # Select relevant columns that match data_exceptions schema
        cols_to_keep = ['emp_id', 'first_name', 'last_name', 'email', 'department', 'issue_reason']
        available_cols = [c for c in cols_to_keep if c in df_exceptions.columns]
        df_exceptions_filtered = df_exceptions[available_cols].copy()

        df_exceptions_filtered.to_sql(
            name='data_exceptions',
            con=engine,
            if_exists='append',  # Appends logs
            index=False
        )
        print(f"⚠️ Successfully logged {len(df_exceptions_filtered)} exception records into 'data_exceptions' table.")
    else:
        print("❌ Error: Exception log file not found.")

if __name__ == "__main__":
    load_to_mysql()