<a href="https://github.com/Brahim-gz/hotel-management-system/blob/main/LICENSE">
  <img align=right src="https://img.shields.io/github/license/Brahim-gz/hotel-management-system?style=flat" alt="License" />
</a>

<br/>
<br/>

# Hotel Management System

The **Hotel Management System** is a Python-based application designed to manage clients, rooms, and reservations in a hotel. It provides an intuitive graphical user interface (GUI) built using the `tkinter` library, making it easy for hotel staff to perform operations such as adding clients, managing rooms, and handling reservations efficiently.

This project was developed as part of the **Advanced Python Module** and demonstrates the use of object-oriented programming (OOP), database management with SQLite, and GUI development with `tkinter`.

## Features

- **Client Management**:
  - Add new clients with details such as name, email, phone number, and registration date.
  - Search for clients by email.
  - View client details and their reservation history.
  - Delete clients from the system.

- **Room Management**:
  - Add new rooms with room number and price per night.
  - Search for rooms by room number.
  - View room details, including status (available/occupied) and reservation history.
  - Delete rooms from the system.

- **Reservation Management**:
  - Reserve rooms for clients by specifying check-in and check-out dates.
  - Check room availability for specific dates.
  - View all reservations for a client or room.

- **User-Friendly Interface**:
  - Intuitive and responsive GUI for easy navigation.
  - Clear visual feedback for successful operations and error handling.

## Technologies Used

- **Python**: The core programming language used for development.
- **SQLite**: Lightweight database for storing client, room, and reservation data.
- **Tkinter**: Python's standard GUI library for building the application interface.

## Installation

### Prerequisites

- [Python (>=3.8)](https://www.python.org/downloads/) installed on your system.
- Basic knowledge of Python and SQLite.

### Steps to Run the Application

1. **Clone the Repository**:
   ```bash
   git clone https://github.com/your-username/hotel-management-system.git
   cd hotel-management-system
   ```

2. **Run the Application**:
   ```bash
   python UI.py
   ```

## Usage

💡The main screen provides options to manage **Clients** or **Rooms**.

💡Use the **Search**, **Add**, and **Reserve** buttons to perform operations.

💡Follow the on-screen instructions to input data and view results.

## Database Schema

The application uses an SQLite database (`hotel_management.db`) with the following tables:

- **Room**:
  - `id`: Primary key (auto-incremented).
  - `number`: Room number (unique).
  - `price_per_night`: Price per night for the room.

- **Client**:
  - `id`: Primary key (auto-incremented).
  - `first_name`: Client's first name.
  - `last_name`: Client's last name.
  - `email`: Client's email (unique).
  - `phone`: Client's phone number.
  - `registration_date`: Date of client registration.

- **Reservation**:
  - `id`: Primary key (auto-incremented).
  - `check_in_date`: Check-in date for the reservation.
  - `check_out_date`: Check-out date for the reservation.
  - `room_id`: Foreign key referencing the `Room` table.
  - `client_id`: Foreign key referencing the `Client` table.

---

<br/>
<p align=center><b>✨🏨Enjoy managing your hotel with this system! 🏨✨</b></p>