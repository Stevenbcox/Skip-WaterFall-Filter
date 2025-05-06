import os
import re
import pandas as pd
from datetime import datetime, timedelta


def filter_column_notna(df, column_name):
    before = len(df)
    df = df[df[column_name].notna()]
    return df


def filter_mil_status(df, column_name):
    df = df[df[column_name] != "Active"]
    return df


def filter_employer_name(df, column_name):
    df = df[df[column_name].isna()]
    return df


def closed_date(df, column_name):
    df = df[df[column_name].isna()]
    return df


def filter_forwarder_keywords(df, column_name):
    keywords_to_remove = [
        "Credit Acceptance Corporation",
        "City of Detroit - DAH Blight",
        "Cavalry SPV I, LLC",
        "DAH Dormant Blight Claims",
        "Cavalry Investments, LLC"
    ]
    pattern = '|'.join([re.escape(keyword) for keyword in keywords_to_remove])
    df = df[~df[column_name].str.contains(pattern, case=False, na=False)]
    return df


def main(input_file, min_balance_due):
    # Load the Excel file
    df = pd.read_excel(input_file, dtype=str)

    # Reverse the DataFrame to process from bottom to top
    df = df.iloc[::-1].reset_index(drop=True)

    # 1️⃣ Filter "OFN" to keep only six-digit numeric values
    df["OFN"] = df["OFN"].astype(str).str.strip()
    df = df[df["OFN"].str.match(r'^\d{6}$', na=False)]

    # 🔍 Remove rows with unwanted Forwarder Name keywords
    df = filter_forwarder_keywords(df, "Forwarder Name")

    # 2️⃣ Remove rows where "D1 DOB" is blank or debtor is older than 64 years
    dob_cutoff = datetime.today() - timedelta(days=23376)  # ~64 years
    df["D1 DOB"] = pd.to_datetime(df["D1 DOB"], errors='coerce')
    df = df[df["D1 DOB"].notna() & (df["D1 DOB"] > dob_cutoff)]

    # 3️⃣ Remove rows where "Last Payment Date" is within 6 months
    six_months_ago = datetime.today() - timedelta(days=180)
    df["Last Payment Date"] = pd.to_datetime(df["Last Payment Date"], errors='coerce')
    df = df[df["Last Payment Date"].isna() | (df["Last Payment Date"] < six_months_ago)]

    # 4️⃣ Remove rows where "D1 DOD" is not empty
    df = df[df["D1 DOD"].isna()]

    # 5️⃣ Filter out rows with empty critical columns
    columns_to_check = [
        "D1 Address", "D1 Last", "D1 First", "D1 City", "D1 Zip",
        "D1 Jmt Date", "D1 SSN", "Debtor 1 Name", "D1 State",
    ]
    for column in columns_to_check:
        df = filter_column_notna(df, column)

    # 6️⃣ Convert "Balance Due" to numeric, filter, then format
    if "Balance Due" in df.columns:
        df["Balance Due"] = df["Balance Due"].str.replace(r'[^0-9.-]', '', regex=True)
        df["Balance Due"] = pd.to_numeric(df["Balance Due"], errors="coerce")
        df = df[df["Balance Due"] >= min_balance_due]
        df["Balance Due"] = df["Balance Due"].apply(lambda x: f"${x:,.2f}" if pd.notna(x) else "")

    # 7️⃣ Remove rows where "D1 Mil Status" is 'Active'
    df = filter_mil_status(df, "D1 Mil Status")

    # 8️⃣ Remove rows where "D1 Employer Name RP" has data
    df = filter_employer_name(df, "D1 Employer Name RP")

    # 9️⃣ Remove rows where "Closed Date" is not empty
    df = closed_date(df, "Closed Date")

    # 🔟 Format all date columns to MM/DD/YYYY
    date_columns = [
        "D1 DOB", "Last Payment Date", "D1 Jmt Date", "D1 Bkcy Filed Date", "Closed Date", "Statute Date",
        "D1 Jmt Renewal Date", "D1 Emp Att Dt 2", "D1 Emp Att Dt 3", "D1 Bank Att 1", "D1 Mil Date",
        "D2 DOB", "D2 Jmt Date", "D2 Bkcy Filed Date", "D2 Jmt Renewal Date", "D2 Emp Att Dt 2",
    ]
    for col in date_columns:
        if col in df.columns:
            df[col] = pd.to_datetime(df[col], errors='coerce').dt.strftime('%m/%d/%Y')

    # Save the cleaned file in the same location as input
    output_path = os.path.join(os.path.dirname(input_file), "filtered_output.xlsx")
    df.to_excel(output_path, index=False)

    return output_path
