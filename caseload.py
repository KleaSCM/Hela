import sqlite3
import pandas as pd
from datetime import datetime, timedelta

def search_clients(location):
    conn = sqlite3.connect('heladb.db')
    query = """
        SELECT 
            JOB_SEEKER_ID,
            FIRST_GIVEN_NAME,
            FAMILY_NAME,
            SITE_NAME,
            NEXT_DIARY_APPOINTMENT_DATE,
            MANAGED_BY,
            LAST_DIARY_APPOINTMENT_RESULT,
            LAST_DIARY_APPOINTMENT_CONSULTANT,
            LAST_DIARY_APPOINTMENT_DATE
        FROM cdp_caseload
        WHERE SITE_NAME LIKE ?
          AND (NEXT_DIARY_APPOINTMENT_DATE IS NULL OR NEXT_DIARY_APPOINTMENT_DATE = '')
          AND CDP_PLACEMENT_STATUS = 'Commenced'
          AND ALLOWANCE_RATE_TYPE != 'Nil Rate'
    """
    results = pd.read_sql_query(query, conn, params=(f"%{location}%",))
    conn.close()
    return results

def search_pending_jps(location):
    conn = sqlite3.connect('heladb.db')
    query = """
        SELECT 
            JOB_SEEKER_ID,
            FIRST_GIVEN_NAME,
            FAMILY_NAME,
            COMMUNITY_NAME,
            CDP_PLACEMENT_STATUS,
            MANAGED_BY,
            JOB_PLAN_SIGNED_DATE,
            CLIENT_NOTE
        FROM cdp_caseload
        WHERE SITE_NAME LIKE ?
          AND JOB_PLAN_STATUS IN ('No Job Plan', '*', 'Job Plan Pending')
          AND CDP_PLACEMENT_STATUS IN ('Commenced', 'Suspended')
    """
    results = pd.read_sql_query(query, conn, params=(f"%{location}%",))
    conn.close()
    return results

def search_resumes(location):
    conn = sqlite3.connect('heladb.db')
    query = """
        SELECT 
            CDP_REGION_NAME,
            JOB_SEEKER_ID,
            COMMUNITY_NAME,
            CDP_PLACEMENT_STATUS,
            MANAGED_BY,
            JOB_PLAN_SIGNED_DATE,
            JOB_PLAN_STATUS,
            RESUME_COMPLETED_DATE,
            RESUME_LAST_UPDATE_DATE,
            CLIENT_NOTE
        FROM cdp_caseload
        WHERE SITE_NAME LIKE ?
    """
    results = pd.read_sql_query(query, conn, params=(f"%{location}%",))
    conn.close()

    six_months_ago = datetime.now() - timedelta(days=6 * 30)
    results['RESUME_LAST_UPDATE_DATE'] = pd.to_datetime(results['RESUME_LAST_UPDATE_DATE'], errors='coerce')
    filtered_results = results[
        (results['RESUME_LAST_UPDATE_DATE'].notna()) &
        (results['RESUME_LAST_UPDATE_DATE'] < six_months_ago)
    ]
    return filtered_results
