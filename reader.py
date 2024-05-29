import pandas as pd
from ScheduleReader.employee import Employee


class ScheduleReader:
    def __init__(self):
        self.df = pd.read_excel('Schedule.xlsx', sheet_name='Sheet1', engine='openpyxl')
        self.employees = []
        self.add_employees()

    def add_employees(self):
        curr_position = ""
        for index, row in self.df.iterrows():
            if row[0] == 'CART ATTENDANTS' or row[0] == 'BEV CART ATTENDANTS' or row[0] == 'STARTERS/MARSHALS' or row[
                0] == 'GOLF SHOP':
                curr_position = row[0]
            elif not pd.isna(row[0]):
                curr_employee = Employee(row[0], row[1], curr_position)
                for i, column in enumerate(row[2:]):
                    if not pd.isna(column):
                        date = self.df.columns[2 + i]  # Get the corresponding date from column headers
                        formatted_date = date.strftime('%B %d, %Y')
                        curr_employee.add_shift(f"\tDate: {formatted_date}, Shift: {column}")
                self.employees.append(curr_employee)

    def get_shifts_by_employee(self, employee_name):
        for employee in self.employees:
            if employee_name == employee.name:
                return employee

    def get_shifts_by_position(self, position):
        return_employees = []
        for employee in self.employees:
            if employee.position == position:
                return_employees.append(employee)
        return return_employees

    def get_all_employees(self):
        return self.employees
