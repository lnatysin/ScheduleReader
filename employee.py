class Employee:

    def __init__(self, name, phone_number, position):
        self.name = name
        self.phone_number = phone_number
        self.position = position
        self.shifts = []

    def add_shift(self, shift):
        self.shifts.append(shift)

    def __str__(self):
        return f"Employee: {self.name}, Position: {self.position}"