class Room:
    def __init__(self, number=0, price_per_night=0, status="Available"):
        self.number = number  # Room number
        self.price_per_night = price_per_night  # Price per night
        self.status = status  # Current status of the room (e.g., available, occupied)
        self.reservations = []  # List to store reservations for this room

    def set_id(self, room_id):
        self.id = room_id

    def set_status(self, status):
        self.status = status

    def display(self):
        floor_info = (
            f"on the floor {self.number // 10}" if self.number >= 10 else "on the ground floor"
        )
        return (
            f"The room number is {self.number} {floor_info}.\n\n"
            f"One night costs {self.price_per_night} DH.\n\n"
            f"It is currently {self.status}.\n\n\n"
        )
