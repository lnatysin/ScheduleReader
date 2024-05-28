from ScheduleReader.reader import ScheduleReader

if __name__ == '__main__':
    reader = ScheduleReader()
    while True:
        user_choice = input(
            'How would you like to look up shifts?\n\tBy employee name type \'Name\'\n\tBy Position type \'Position\'\n\tAll Employees \'All\'\n\tTo exit \'Exit\'\nChoice: ')
        if user_choice == 'Name':
            employee_name = input('Please input the employee name: ')
            reader.get_shifts_by_employee(employee_name)
        elif user_choice == 'Position':
            position = input(
                'Please input the position type (GOLF SHOP, STARTERS/MARSHALS, CART ATTENDANTS, BEV CART ATTENDANTS): ')
            if position == 'CART ATTENDANTS' or position == 'BEV CART ATTENDANTS' or position == 'STARTERS/MARSHALS' or position == 'GOLF SHOP':
                reader.get_shifts_by_position(position)
        elif user_choice == 'All':
            for employee in reader.employees:
                print(employee)
        elif user_choice == 'Exit':
            break
        else:
            print('That is not an option :(')