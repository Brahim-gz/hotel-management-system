from datetime import datetime


class Client:
    def __init__(self, first_name='', last_name='', email='', phone='', registration_date=None):
        self.first_name = first_name  # Client's first name
        self.last_name = last_name  # Client's last name
        self.email = email  # Client's email address
        self.phone = phone  # Client's phone number
        self.registration_date = registration_date if registration_date else datetime.now().strftime("%d-%m-%Y")
        self.reservations = []  # List to store reservations made by the client

    def set_id(self, client_id):
        self.id = client_id

    def get_id(self):
        return self.id

    def display(self):
        return (
            f"Client's full name: {self.first_name.upper()} {self.last_name.upper()}\n\n"
            f"Email: {self.email}\n\n"
            f"Phone: {self.phone}\n\n"
            f"Registered on: {self.registration_date}\n\n\n"
        )

