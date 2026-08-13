# Employee Data Automation & Reporting System

A Python-based data engineering and processing solution designed to ingest raw employee CSV datasets, perform data cleaning and business rule validation, route exceptions, load structured records into MySQL, and generate automated management reports.

## 📌 Project Overview & Features
- **Data Cleaning & Standardization:** Handles whitespace stripping, duplicate detection, date parsing, and full name synthesis using Pandas.
- **Business Rule Validation:** Automatically flags invalid salaries (`<= 0`), missing/malformed email addresses, and duplicate records.
- **Relational Storage:** Ingests cleaned datasets and logs validation exception records directly into MySQL using SQLAlchemy and PyMySQL.
- **Automated Reporting:** Exports styled Excel management reports complete with KPI metrics and department payroll summaries.

## 📁 Repository Structure
```text
├── DATA/
│   ├── raw/                  # Incoming raw employee CSVs
│   └── output/               # Output clean files & reports
├── clean_and_validate.py     # Python cleaning & validation engine
├── db_loader.py              # MySQL ingestion script
├── generate_report.py        # Excel report generator script
├── schema.sql                # MySQL DDL table schema     
├── .gitignore                # Git exclusion configuration
└── README.md                 # Project documentation
