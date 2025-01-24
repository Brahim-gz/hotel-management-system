class Reservation:
    def __init__(self, check_in_date, check_out_date, room, client):
        self.check_in_date = check_in_date  # The date the client checks in
        self.check_out_date = check_out_date  # The date the client checks out
        self.room = room  # The room associated with the reservation
        self.client = client  # The client who made the reservation

    def get_check_out_date(self):
        return self.check_out_date