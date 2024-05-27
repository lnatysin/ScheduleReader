import pandas as pd
from datetime import datetime

# Read the Excel file
df = pd.read_excel('Schedule.xlsx', sheet_name='Sheet1', engine='openpyxl')

# Iterate through rows
for index, row in df.iterrows():
    if not pd.isna(row[0]):  # Check if 'Name' column is not NaN
        if row[0] == 'CART ATTENDANTS' or row[0] == 'BEV CART ATTENDANTS' or row[0] == 'STARTERS/MARSHALS' or row[0] == 'GOLF SHOP':
            print('Position:', row[0])
        else:
            print('Name:', row[0])
            print('Phone Number:', row[1])
            for i, column in enumerate(row[2:]):
                if not pd.isna(column):
                    date = df.columns[2 + i]  # Get the corresponding date from column headers
                    formatted_date = date.strftime('%B %d, %Y')
                    print(f"\tDate: {formatted_date}, Shift: {column}")