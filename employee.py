class Employee:

    def __init__(self, name, phone_number, position):
        self.name = name
        self.phone_number = phone_number
        self.position = position
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)

    def __str__(self):
        return_string = f"Name: {self.name}, Phone Number: {self.phone_number}\n"
        if len(self.shifts) == 0:
            return_string += "\tNo shifts\n"
        else:
            for shift in self.shifts:
                return_string += f"{shift} \n"
        return return_string
