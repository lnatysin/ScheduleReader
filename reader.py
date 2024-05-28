import pandas as pd

from ScheduleReader.employee import Employee

class ScheduleReader:
    def __init__(self):
        self.df = pd.read_excel('Schedule.xlsx', sheet_name='Sheet1', engine='openpyxl')
        self.employees = []

    def add_employees(self):
        curr_position = ""
        for index, row in self.df.iterrows():
            if row[0] == 'CART ATTENDANTS' or row[0] == 'BEV CART ATTENDANTS' or row[0] == 'STARTERS/MARSHALS' or row[0] == 'GOLF SHOP':
                curr_position = row[0]
            elif not pd.isna(row[0]):
                curr_employee = Employee(row[0], row[1], curr_position)
                for i, column in enumerate(row[2:]):
                    if not pd.isna(column):
                        date = self.df.columns[2 + i]  # Get the corresponding date from column headers
                        formatted_date = date.strftime('%B %d, %Y')
                        curr_employee.add_shift(f"\tDate: {formatted_date}, Shift: {column}")

    def get_shifts_by_employee(self, employee_name):
        for index, row in self.df.iterrows():
            if employee_name == row[0]:
                print('Name:', row[0])
                print('Phone Number:', row[1])
                for i, column in enumerate(row[2:]):
                    if not pd.isna(column):
                        date = self.df.columns[2 + i]  # Get the corresponding date from column headers
                        formatted_date = date.strftime('%B %d, %Y')
                        print(f"\tDate: {formatted_date}, Shift: {column}")

    def get_shifts_by_position(self, position):
        inPosition = False
        for index, row in self.df.iterrows():
            if position == row[0]:
                inPosition = True
            elif row[0] == 'CART ATTENDANTS' or row[0] == 'BEV CART ATTENDANTS' or row[0] == 'STARTERS/MARSHALS' or row[
                0] == 'GOLF SHOP':
                inPosition = False
            elif inPosition:
                print('Name:', row[0])
                print('Phone Number:', row[1])
                for i, column in enumerate(row[2:]):
                    if not pd.isna(column):
                        date = self.df.columns[2 + i]  # Get the corresponding date from column headers
                        formatted_date = date.strftime('%B %d, %Y')
                        print(f"\tDate: {formatted_date}, Shift: {column}")


if __name__ == '__main__':
    reader = ScheduleReader()
    user_choice = input(
        'How would you like to look up shifts?\n\tBy employee name type \'Name\'\n\tBy Position type \'Position\'\nChoice: ')
    if user_choice == 'Name':
        employee_name = input('Please input the employee name: ')
        reader.get_shifts_by_employee(employee_name)
    elif user_choice == 'Position':
        position = input(
            'Please input the position type (GOLF SHOP, STARTERS/MARSHALS, CART ATTENDANTS, BEV CART ATTENDANTS): ')
        if position == 'CART ATTENDANTS' or position == 'BEV CART ATTENDANTS' or position == 'STARTERS/MARSHALS' or position == 'GOLF SHOP':
            reader.get_shifts_by_position(position)
    else:
        print('That is not an option :(')
