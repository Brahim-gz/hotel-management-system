import sqlite3

from Room import Room
from Client import Client
from Reservation import Reservation

# Connect to the SQLite database
db = sqlite3.connect("hotel_management.db")


def add_room(room):
    #Add a room to the database.
    cursor = db.execute(
        "INSERT INTO Room(number, price_per_night) VALUES (?, ?)",
        (room.number, room.price_per_night),
    )
    db.commit()
    return cursor.lastrowid


def get_rooms():
    #Retrieve all rooms.
    cursor = db.execute("SELECT * FROM Room ")
    rooms = []
    for row in cursor:
        rooms.append(row)
    return rooms


def add_client(client):
    #Add a client to the database.
    cursor = db.execute(
        "INSERT INTO Client(first_name, last_name, email, phone, registration_date) VALUES (?, ?, ?, ?, ?)",
        (client.first_name, client.last_name, client.email, client.phone, client.registration_date),
    )
    db.commit()
    return cursor.lastrowid


def add_reservation(reservation):
    #Add a reservation to the database.
    cursor = db.execute(
        "INSERT INTO Reservation(check_in_date, check_out_date, room_id, client_id) VALUES (?, ?, ?, ?)",
        (reservation.check_in_date, reservation.check_out_date, reservation.room.id, reservation.client.id),
    )
    db.commit()
    return cursor.lastrowid


def book_room(check_in, check_out, room_number, email):
    """
    Make a reservation for a specific room and client using their email.
    """
    cursor = db.execute("SELECT * FROM Room WHERE number = ?", (room_number,))
    room_id = cursor.fetchone()[0]

    cursor = db.execute("SELECT * FROM Client WHERE email = ?", (email,))
    client_id = cursor.fetchone()[0]

    # check if there is a reservation between these dates.
    cursor = db.execute(
        """                 
        SELECT 1 
        FROM Reservation
        WHERE room_id = ? 
        AND ( ? BETWEEN check_in_date AND check_out_date
        OR ? BETWEEN check_in_date AND check_out_date
        OR ? IN(check_in_date, check_out_date)
        OR ? IN(check_in_date, check_out_date)
        OR ( check_in_date > ? 
        AND check_out_date < ?))
        """,
        (room_id,check_in,check_out,check_in,check_out,check_in,check_out)
    )
    if cursor.fetchone():
        return False

    room = Room()
    room.set_id(room_id)

    client = Client()
    client.set_id(client_id)

    reservation = Reservation(check_in, check_out, room, client)
    add_reservation(reservation)
    db.commit()
    return True

def search_client(email):
    #Search for a client by their email.
    cursor = db.execute("SELECT * FROM Client WHERE email = ?", (email,))
    row = cursor.fetchone()
    if not row:
        return None

    client = Client(row[1], row[2], email, row[4], row[5])

    res_cursor = db.execute(
        "SELECT check_in_date, check_out_date, number "
        "FROM Reservation, Room "
        "WHERE Reservation.room_id = Room.id AND client_id = ?;",
        (row[0],),
    )
    for res in res_cursor:
        client.reservations.append(Reservation(res[0], res[1], Room(res[2]), client))

    return client


def search_room(number):
    #Search for a room by its number.
    cursor = db.execute(
        """
        SELECT 
            r.id, 
            r.price_per_night,
            CASE 
                WHEN EXISTS (
                    SELECT 1 
                    FROM Reservation
                    WHERE room_id = r.number 
                    AND CURRENT_DATE BETWEEN check_in_date AND check_out_date
                ) THEN 'occupied' 
                ELSE 'available' 
            END AS status
        FROM Room r
        WHERE r.number = ?
        """,
        (number,)
    )
    row = cursor.fetchone()
    if not row:
        return None

    room = Room(number, row[1],row[2])
    room.set_id(row[0])

    res_cursor = db.execute(
        "SELECT check_in_date, check_out_date, first_name, last_name "
        "FROM Reservation, Client "
        "WHERE Reservation.client_id = Client.id AND room_id = ?;",
        (row[0],),
    )
    for res in res_cursor:
        room.reservations.append(Reservation(res[0], res[1], room, Client(res[2], res[3])))

    return room


def delete_room(number):
    #Delete a room from the database using its number.
    db.execute('DELETE FROM Room WHERE number = ?', (number,))
    db.commit()


def delete_client(email):
    #Delete a client from the database using their email.
    db.execute("DELETE FROM Client WHERE email = ?", (email,))
    db.commit()