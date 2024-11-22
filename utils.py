# import sqlite3
# import pandas as pd

# def setup_database():
#     conn = sqlite3.connect('heladb.db')

#     # Load Caseload Data
#     caseload_file = r'C:\Users\JohnFarmer\OneDrive - RESQ Plus Pty Ltd\Desktop\compliance\REPORTING CMPL\Hela\SUB052 - CDP Job Seeker Caseload19112024.csv'
#     caseload_data = pd.read_csv(caseload_file)
#     caseload_data.to_sql('cdp_caseload', conn, if_exists='replace', index=False)

#     print("Database setup complete!")
#     conn.close()

import sqlite3
import pandas as pd
def setup_database():
    conn = sqlite3.connect('heladb.db')

    # Load Caseload Data
    caseload_file = r'/home/klea/Documents/Deven/Hela/SUB052 - CDP Job Seeker Caseload19112024.csv'
    caseload_data = pd.read_csv(caseload_file)
    caseload_data.to_sql('cdp_caseload', conn, if_exists='replace', index=False)

    # Load JSCI Data
    jsci_file = r'/home/klea/Documents/Deven/Hela/SUB051 - CDP Job Seeker General-19112024.csv'
    jsci_data = pd.read_csv(jsci_file)
    jsci_data.to_sql('jsci_table', conn, if_exists='replace', index=False)

    print("Database setup complete!")
    conn.close()

