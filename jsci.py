import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def search_incomplete_jsci(location):
    """
    Search for JSCIs in the given location where JSCI_LAST_UPDATE_DATE is greater than 6 months old.
    """
    conn = sqlite3.connect('heladb.db')
    query = """
        SELECT 
            DISABILITY_DESCRIPTION_4,
            DISABILITY_DESCRIPTION_3,
            DISABILITY_DESCRIPTION_2,
            DISABILITY_DESCRIPTION_1,
            JSCI_SPECIAL_NEEDS,
            JSCI_DETAILS_PERSONAL_FACTORS,
            JSCI_STATUS,
            JSCI_LAST_UPDATE_USER_ID,
            JSCI_LAST_UPDATE_DATE,
            COMMUNITY_NAME,
            DATE_OF_BIRTH,
            SURNAME,
            FIRST_NAME,
            JOB_SEEKER_ID,
            RJCP_REGION_NAME
        FROM jsci_table
        WHERE COMMUNITY_NAME LIKE ?
    """
    results = pd.read_sql_query(query, conn, params=(f"%{location}%",))
    conn.close()

    # Define the six-month threshold
    six_months_ago = datetime.now() - timedelta(days=6 * 30)

    # Filter for rows with JSCI_LAST_UPDATE_DATE older than six months
    results['JSCI_LAST_UPDATE_DATE'] = pd.to_datetime(
        results['JSCI_LAST_UPDATE_DATE'], errors='coerce'
    )
    filtered_results = results[
        (results['JSCI_LAST_UPDATE_DATE'].notna()) &  # Exclude invalid dates
        (results['JSCI_LAST_UPDATE_DATE'] < six_months_ago)  # Older than six months
    ]

    return filtered_results
