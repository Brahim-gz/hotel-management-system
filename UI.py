import re
from datetime import datetime, date
from tkinter import *
from tkinter.messagebox import showinfo, showerror, askyesno
from tkinter.ttk import Treeview

from DBInteraction import *

# Database connection
db = sqlite3.connect("hotel_management.db")

db.execute('CREATE TABLE IF NOT EXISTS Room (id INTEGER PRIMARY KEY AUTOINCREMENT, number INTEGER UNIQUE, price_per_night FLOAT)')

db.execute("CREATE TABLE IF NOT EXISTS Client (id INTEGER PRIMARY KEY AUTOINCREMENT, last_name TEXT, first_name TEXT, email TEXT UNIQUE, phone TEXT, registration_date DATE)")

db.execute("CREATE TABLE IF NOT EXISTS Reservation (id INTEGER PRIMARY KEY AUTOINCREMENT, check_in_date DATE, check_out_date DATE, room_id INTEGER, client_id INTEGER, FOREIGN KEY(room_id) REFERENCES Room(id) ON DELETE CASCADE, FOREIGN KEY(client_id) REFERENCES Client(id) ON DELETE CASCADE)")

def search(entity_type):
    for widget in form.winfo_children():
        widget.destroy()
    for widget in body.winfo_children():
        widget.destroy()
    body.config(bg="white", bd=0)

    if entity_type == 'CH':
        form.config(bg="#ffc971")
        room_label = Label(form, text="Room Number: ", font=("Comic Sans MS", 10), width=20, bg="#ffc971")
        room_entry = Entry(form, textvariable=StringVar(), width=50)
        room_label.grid(row=0, column=0, pady=12, sticky='w')
        room_entry.grid(row=0, column=1, padx=10, pady=15, sticky='sw')
    else:
        form.config(bg="#a2d6f9")
        email_label = Label(form, text="Client Email: ", font=("Comic Sans MS", 10), width=20, bg="#a2d6f9")
        email_entry = Entry(form, textvariable=StringVar(), width=50)
        email_label.grid(row=0, column=0, pady=12, sticky='w')
        email_entry.grid(row=0, column=1, padx=10, pady=15, sticky='sw')

    validate_button = Button(form, text="Validate", bg="#25a244", fg="white", font=("Comic Sans MS", 10), width=20,
                             command=lambda: validate(entity_type, email_entry.get() if entity_type == 'CL' else room_entry.get()))
    validate_button.grid(row=0, column=2, columnspan=2, padx=20, pady=10, sticky='se')

def validate(entity_type, arg):
    search(entity_type)
    bg_color = "#ffc971" if entity_type == 'CH' else "#a2d6f9"
    body.config(bg=bg_color, bd=5)

    if not arg:
        msg = Label(body, text=f"No {'email' if entity_type == 'CL' else 'room number'} was entered", font=("Comic Sans MS", 15), bg=bg_color)
        msg.pack()
    elif (entity_type == 'CL' and not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', arg)) or (entity_type == 'CH' and not is_integer(arg)):
        msg = Label(body, text=f"Enter a valid {'email' if entity_type == 'CL' else 'room number'}", font=("Comic Sans MS", 15), bg=bg_color)
        msg.pack()
    else:
        if entity_type == 'CL':
            entity = search_client(arg)
        elif is_integer(arg):
            entity = search_room(int(arg))
        else:
            showerror("Error", "Enter valid information.")
            entity = None
        if entity:
            if entity_type == 'CH' and entity.reservations:
                if entity.status == 'occupied':
                    # Find the checkout date for the current reservation
                    latest_checkout = max(
                        datetime.strptime(reservation.check_out_date, "%Y-%m-%d").date()
                        for reservation in entity.reservations
                        if datetime.strptime(reservation.check_in_date, "%Y-%m-%d").date() <= datetime.now().date() <= datetime.strptime(reservation.check_out_date, "%Y-%m-%d").date()
                    )
                    entity.set_status(f'occupied until {latest_checkout}')
                else:
                    # Find the next check-in date for the room
                    next_checkin = [
                        datetime.strptime(reservation.check_in_date, "%Y-%m-%d").date()
                        for reservation in entity.reservations
                        if datetime.strptime(reservation.check_in_date, "%Y-%m-%d").date() > datetime.now().date()
                    ]
                    entity.set_status(f'available until {min(next_checkin)}'if next_checkin else "available")
            info_frame = Frame(body, bd=0, pady=20, padx=10, bg=bg_color)
            info_frame.pack(side=TOP, fill=X)
            entity_info = Label(info_frame, text=entity.display(), font=("Comic Sans MS", 12), anchor='w', bg=bg_color)
            entity_info.grid(row=0, column=0, rowspan=2, padx=10, sticky='w')

            delete_button = Button(info_frame, text="Delete", background="#ef233c", font=("Comic Sans MS", 10), fg="white", width=15,
                                   command=lambda: delete(entity_type, arg), pady=7)
            delete_button.grid(row=0, column=1, padx=20, sticky='ne')
            info_frame.grid_columnconfigure(0, weight=1)

            if entity.reservations:
                table = Treeview(body, columns=('check_in_date', 'check_out_date', 'room_number' if entity_type == 'CL' else 'client'), show='headings')
                table.heading('check_in_date', text='Arrival Date')
                table.heading('check_out_date', text='Departure Date')
                if entity_type == 'CL':
                    table.heading('room_number', text='Room Number')
                else:
                    table.heading('client', text='Client')
                table.pack(fill=X, padx=20)
                for res in entity.reservations:
                    table.insert(parent='', index=0, values=(res.check_in_date, res.check_out_date,
                                                             res.room.number if entity_type == 'CL' else res.client.last_name.upper() + ' ' + res.client.first_name.upper()))
            else:
                msg = Label(body, text=f"This {'client' if entity_type == 'CL' else 'room'} has no reservations.", font=("Comic Sans MS", 15), bg=bg_color, fg="white")
                msg.pack()
        else:
            msg = Label(body, text=f"No {'client with this email' if entity_type == 'CL' else 'room with this number'} found", font=("Comic Sans MS", 15), bg=bg_color)
            msg.pack()

def delete(entity_type, arg):
    if entity_type == 'CL':
        response = askyesno("Warning!", "Do you really want to delete this client?")
        if response:
            delete_client(arg)
            search(entity_type)
    else:
        response = askyesno("Warning!", "Do you really want to delete this room?")
        if response:
            delete_room(arg)
            search(entity_type)

def is_integer(string):
    try:
        int(string)
        return True
    except ValueError:
        return False

def ajout(entity_type):
    for widget in form.winfo_children():
        widget.destroy()
    for widget in body.winfo_children():
        widget.destroy()
    body.config(bg="white", bd=0)

    if entity_type == 'CL':  # Adding a client
        form.config(bg="#a2d6f9")

        email_label = Label(form, text="New Client Email: ", font=("Comic Sans MS", 10), width=55, anchor='w', bg="#a2d6f9")
        email_entry = Entry(form, textvariable=StringVar(), width=70)
        email_label.pack(pady=5)
        email_entry.pack(pady=5)

        last_name_label = Label(form, text="Last Name: ", font=("Comic Sans MS", 10), width=55, anchor='w', bg="#a2d6f9")
        last_name_entry = Entry(form, textvariable=StringVar(), width=70)
        last_name_label.pack(pady=5)
        last_name_entry.pack(pady=5)

        first_name_label = Label(form, text="First Name: ", font=("Comic Sans MS", 10), width=55, anchor='w', bg="#a2d6f9")
        first_name_entry = Entry(form, textvariable=StringVar(), width=70)
        first_name_label.pack(pady=5)
        first_name_entry.pack(pady=5)

        phone_label = Label(form, text="Phone Number: ", font=("Comic Sans MS", 10), width=55, anchor='w', bg="#a2d6f9")
        phone_entry = Entry(form, textvariable=StringVar(), width=70)
        phone_label.pack(pady=5)
        phone_entry.pack(pady=5)

        add_button = Button(form, text="Add Client", bg="#25a244", fg="white", font=("Comic Sans MS", 10), width=30,
                            command=lambda: add_cl(email_entry.get(), last_name_entry.get(), first_name_entry.get(), phone_entry.get()))
        add_button.pack(pady=20)

    else:  # Adding a room
        form.config(bg="#ffc971")

        number_label = Label(form, text="New Room Number: ", font=("Comic Sans MS", 10), width=55, bg="#ffc971", anchor='w')
        number_entry = Entry(form, textvariable=StringVar(), width=70)
        number_label.pack(pady=5)
        number_entry.pack(pady=5)

        price_label = Label(form, text="Price per Night (in DH): ", font=("Comic Sans MS", 10), width=55, bg="#ffc971", anchor='w')
        price_entry = Entry(form, textvariable=StringVar(), width=70)
        price_label.pack(pady=5)
        price_entry.pack(pady=5)

        add_button = Button(form, text="Add Room", bg="#25a244", fg="white", font=("Comic Sans MS", 10), width=30,
                            command=lambda: add_ch(number_entry.get(), price_entry.get()))
        add_button.pack(pady=20)


def add_cl(email, last_name, first_name, phone):
    if not email or not last_name or not first_name or not phone:
        showerror("Error", "Some fields are missing.")
    elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email) or \
            not re.match(r'^[a-zA-Z]+$', last_name) or \
            not re.match(r'^[a-zA-Z]+$', first_name) or \
            not re.match(r'^[\s0-9+-]+$', phone):
        showerror("Error", "Enter valid information.")
    else:
        client = Client(last_name.lower().strip(), first_name.lower().strip(), email.strip(), phone.strip())
        try:
            add_client(client)
            showinfo('Success', 'The new client has been added successfully.')
        except sqlite3.IntegrityError:
            showerror("Error", f"A client with the email {email} already exists.")
        ajout('CL')

def add_ch(number, price):
    if not number or not price:
        showerror("Error", "Some fields are missing.")
    elif not is_integer(number) or not is_integer(price) or int(price) <= 0:
        showerror("Error", "Enter valid information.")
    else:
        room = Room(int(number), int(price))
        try:
            add_room(room)
            showinfo('Success', 'The new room has been added successfully.')
        except sqlite3.IntegrityError:
            showerror("Error", f"A room with the number {number} already exists.")
        ajout('CH')


def reserve_page():
    for widget in form.winfo_children():
        widget.destroy()
    for widget in body.winfo_children():
        widget.destroy()

    form.config(bg="#ffc971")
    body.config(bg="#ffc971", bd=5)

    email_label = Label(form, text="Client Email for Reservation: ", font=("Comic Sans MS", 10), width=40, bg="#ffc971")
    email_entry = Entry(form, textvariable=StringVar(), width=40)
    email_label.grid(row=0, column=0, pady=7, sticky='w')
    email_entry.grid(row=0, column=1, pady=7, padx=5, sticky='w')

    Label(form, text="Arrival Date: ", width=18, font=("Comic Sans MS", 10), bg="#ffc971").grid(row=1, column=0, pady=7, sticky='w')

    arrival_frame = Frame(form, bd=0, bg="#ffc971", width=48)
    arrival_frame.grid(row=2, column=0, columnspan=2)

    Label(arrival_frame, text=" Day |", font=("Comic Sans MS", 10), bg="#ffc971").grid(row=0, column=0, pady=7, sticky='w')
    arrival_day_entry = Entry(arrival_frame, textvariable=StringVar(), width=10)
    arrival_day_entry.grid(row=0, column=1, pady=7, sticky='w')

    Label(arrival_frame, text=" Month |", font=("Comic Sans MS", 10), bg="#ffc971").grid(row=0, column=2, pady=7, sticky='w')
    arrival_month_entry = Entry(arrival_frame, textvariable=StringVar(), width=10)
    arrival_month_entry.grid(row=0, column=3, pady=7, sticky='w')

    Label(arrival_frame, text=" Year |", font=("Comic Sans MS", 10), bg="#ffc971").grid(row=0, column=4, pady=7, sticky='w')
    arrival_year_entry = Entry(arrival_frame, textvariable=StringVar(), width=10)
    arrival_year_entry.grid(row=0, column=5, pady=7, sticky='w')

    Label(form, text="Departure Date: ", width=18, font=("Comic Sans MS", 10), bg="#ffc971").grid(row=3, column=0, pady=7, sticky='w')

    departure_frame = Frame(form, bd=0, bg="#ffc971", width=48)
    departure_frame.grid(row=4, column=0, columnspan=2)

    Label(departure_frame, text=" Day |", font=("Comic Sans MS", 10), bg="#ffc971").grid(row=0, column=0, pady=7, sticky='w')
    departure_day_entry = Entry(departure_frame, textvariable=StringVar(), width=10)
    departure_day_entry.grid(row=0, column=1, pady=7, sticky='w')

    Label(departure_frame, text=" Month |", font=("Comic Sans MS", 10), bg="#ffc971").grid(row=0, column=2, pady=7, sticky='w')
    departure_month_entry = Entry(departure_frame, textvariable=StringVar(), width=10)
    departure_month_entry.grid(row=0, column=3, pady=7, sticky='w')

    Label(departure_frame, text=" Year |", font=("Comic Sans MS", 10), bg="#ffc971").grid(row=0, column=4, pady=7, sticky='w')
    departure_year_entry = Entry(departure_frame, textvariable=StringVar(), width=10)
    departure_year_entry.grid(row=0, column=5, pady=7, sticky='w')

    rooms = get_rooms()

    if rooms:
        Label(body, text="Rooms", font=("Comic Sans MS", 12), bg="#ffc971").pack()
        table = Treeview(body, columns=('number', 'floor', 'price'), show='headings')
        table.heading('number', text='Room Number')
        table.heading('floor', text='Floor')
        table.heading('price', text='Price per Night (in DH)')
        table.pack(fill=X, expand=True, padx=20, pady=10)

        for room in rooms:
            table.insert(parent='', index=0, values=(room[1], room[1] // 10 if room[1] >= 10 else "Ground Floor", room[2]))
    else:
        Label(body, text="All rooms in the hotel are occupied", font=("Comic Sans MS", 12), bg="#ffc971").pack()

    reserve_button = Button(form, text="Reserve", background="#25a244", fg="white", font=("Comic Sans MS", 10), width=12, pady=7,
                            command=lambda: reserve_room(table, [arrival_day_entry.get(), arrival_month_entry.get(), arrival_year_entry.get()],
                                                        [departure_day_entry.get(), departure_month_entry.get(), departure_year_entry.get()], email_entry.get()) if rooms else None)
    reserve_button.grid(row=4, column=2, padx=10, pady=12)


def reserve_room(table, check_in_date, check_out_date, email):
    if not email or any(not item for item in check_in_date + check_out_date):
        showerror("Error", "Some fields are missing.")
    elif not re.match(r'^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$', email):
        showerror("Error", "Enter a valid email.")
    elif not re.match(r'^(0?[1-9]|[12][0-9]|3[01])$', check_in_date[0]) or \
            not re.match(r'^(0?[1-9]|[12][0-9]|3[01])$', check_out_date[0]) or \
            not re.match(r'^(0?[1-9]|1[012])$', check_in_date[1]) or \
            not re.match(r'^(0?[1-9]|1[012])$', check_out_date[1]) or \
            not re.match(r'^(20[0-5][0-9])$', check_in_date[2]) or \
            not re.match(r'^(20[0-5][0-9])$', check_out_date[2]):
        showerror("Error", "Enter valid dates.")
    elif date(int(check_out_date[2]), int(check_out_date[1]), int(check_out_date[0])) < date(int(check_in_date[2]), int(check_in_date[1]), int(check_in_date[0])):
        showerror("Error", "Enter a valid departure date.")
    else:
        selected_rooms = table.selection()
        if not selected_rooms:
            showerror("Error", "No room has been selected.")
        else:
            for room_id in selected_rooms:
                room_details = table.item(room_id)["values"]
                try:
                    book_room(date(int(check_in_date[2]), int(check_in_date[1]), int(check_in_date[0])),
                              date(int(check_out_date[2]), int(check_out_date[1]), int(check_out_date[0])),
                              room_details[0], email)
                    showinfo('Success', f'The room {room_details[0]} has been reserved successfully.')
                except Exception:
                    showerror("Error", "No client exists with this email.")
            reserve_page()
def gestion(entity_type):
    for widget in Nav.winfo_children():
        widget.destroy()

    search_button = Button(Nav, text="Search", background="#adb5bd", font=("Comic Sans MS", 10),
                           width=50 if entity_type == 'CL' else 33,
                           command=lambda: search(entity_type))
    search_button.grid(column=0, row=0, sticky='sw')

    if entity_type == 'CH':
        reserve_button = Button(Nav, text="Reserve", background="#adb5bd", font=("Comic Sans MS", 10),
                                width=33, command=reserve_page)
        reserve_button.grid(column=1, row=0, sticky='sw')

    add_button = Button(Nav, text="Add", background="#adb5bd", font=("Comic Sans MS", 10),
                        width=50 if entity_type == 'CL' else 33,
                        command=lambda: ajout(entity_type))
    add_button.grid(column=1 if entity_type == 'CL' else 2, row=0, sticky='sw')

    search(entity_type)

    back_button = Button(footer, text="<<<", background="#adb5bd", font=("Comic Sans MS", 10), width=100, command=home)
    back_button.grid(row=0, column=0, sticky='n')


def home():
    for widget in Nav.winfo_children():
        widget.destroy()
    for widget in form.winfo_children():
        widget.destroy()
    for widget in body.winfo_children():
        widget.destroy()
    for widget in footer.winfo_children():
        widget.destroy()

    room_button = Button(Nav, text="ROOMS", background="#d8973c", font=("courrier", 30, "bold"),
                         fg="White", width=17, height=100, command=lambda: gestion('CH'))
    room_button.pack(side=RIGHT)

    client_button = Button(Nav, text="CLIENTS", background="#1282a2", font=("courrier", 30, "bold"),
                           fg="White", width=17, height=100, command=lambda: gestion('CL'))
    client_button.pack(side=LEFT)

# GUI setup
window = Tk()
window.title("Hotel Manager")
window.geometry("800x800")
window.resizable(False, True)
window.config(bg="white")

Nav = Frame(window, width=100)
Nav.pack(side=TOP)
form = Frame(window, bd=5, relief=GROOVE, pady=20, padx=20)
form.pack(side=TOP, fill=X, padx=25, pady=25)
body = Frame(window, bd=0, relief=GROOVE, pady=20)
body.pack(side=TOP, fill=X, padx=25, pady=15)
footer = Frame(window, width=100)
footer.pack(side=BOTTOM, fill=X)

home()

window.mainloop()

db.commit()
db.close()
