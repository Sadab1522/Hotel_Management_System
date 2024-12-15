import tkinter as tk
from tkinter import ttk, messagebox


# Room and Subclasses
class Room:
    def __init__(self, room_number, price_per_night, is_available=True):
        self.room_number = room_number
        self.price_per_night = price_per_night
        self.is_available = is_available

    def book(self):
        if self.is_available:
            self.is_available = False
            return True
        return False

    def vacate(self):
        if not self.is_available:
            self.is_available = True
            return True
        return False

    def details(self):
        return f"Room {self.room_number} - ${self.price_per_night}/night"


class SingleRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, price_per_night=100)


class DoubleRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, price_per_night=150)


class SuiteRoom(Room):
    def __init__(self, room_number):
        super().__init__(room_number, price_per_night=300)


class Hotel:
    def __init__(self, name):
        self.name = name
        self.rooms = []

    def add_room(self, room):
        self.rooms.append(room)

    def view_available_rooms(self):
        return [room.details() for room in self.rooms if room.is_available]

    def book_room(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                if room.book():
                    return f"Room {room_number} successfully booked."
                else:
                    return f"Room {room_number} is already booked."
        return f"Room {room_number} not found."

    def vacate_room(self, room_number):
        for room in self.rooms:
            if room.room_number == room_number:
                if room.vacate():
                    return f"Room {room_number} successfully vacated."
                else:
                    return f"Room {room_number} is not occupied."
        return f"Room {room_number} not found."

    def get_occupied_rooms(self):
        return [room.details() for room in self.rooms if not room.is_available]

    def search_rooms(self, min_price, max_price, room_type=None):
        rooms_in_range = [
            room.details()
            for room in self.rooms
            if min_price <= room.price_per_night <= max_price and room.is_available
               and (room_type is None or isinstance(room, globals().get(room_type + "Room")))
        ]
        return rooms_in_range


class HotelApp:
    def __init__(self, root, hotel):
        self.hotel = hotel
        self.root = root
        self.root.title("Hotel Management System")
        self.root.geometry("800x600")
        self.root.configure(bg="#e0f7fa")

        # Title Label
        self.title_label = tk.Label(
            root,
            text="Welcome to Hotel Diu Inn",
            font=("Helvetica", 24, "bold"),
            bg="#00796b",
            fg="white",
            padx=10,
            pady=10,
        )
        self.title_label.pack(fill=tk.X)

        # Buttons Frame
        buttons_frame = tk.Frame(root, bg="#004d40")
        buttons_frame.pack(expand=True, fill=tk.BOTH, padx=20, pady=20)

        button_style = {
            "font": ("Helvetica", 14),
            "bg": "#26a69a",
            "fg": "white",
            "activebackground": "#004d40",
            "activeforeground": "white",
            "relief": tk.RAISED,
            "borderwidth": 2,
        }

        tk.Button(buttons_frame, text="View Available Rooms", command=self.view_available_rooms, **button_style).pack(
            fill=tk.X, pady=10, padx=20
        )
        tk.Button(buttons_frame, text="Book a Room", command=self.book_room, **button_style).pack(
            fill=tk.X, pady=10, padx=20
        )
        tk.Button(buttons_frame, text="Vacate a Room", command=self.vacate_room, **button_style).pack(
            fill=tk.X, pady=10, padx=20
        )
        tk.Button(buttons_frame, text="Search Rooms", command=self.search_rooms, **button_style).pack(
            fill=tk.X, pady=10, padx=20
        )
        tk.Button(buttons_frame, text="Exit", command=root.quit, **button_style).pack(fill=tk.X, pady=10, padx=20)

        self.input_window = None  # Initialize input_window as an attribute

    def view_available_rooms(self):
        rooms = self.hotel.view_available_rooms()
        self.show_custom_window("Available Rooms", "\n".join(rooms) if rooms else "No rooms available at the moment.")

    def book_room(self):
        # Show the available rooms in a scrollable list when the user clicks "Book a Room"
        available_rooms = self.hotel.view_available_rooms()
        if not available_rooms:
            self.show_custom_window("Booking Error", "No rooms are available to book.")
            return

        # Create a top-level window for booking
        top = tk.Toplevel(self.root)
        top.title("Available Rooms")
        top.geometry("600x500")  # Increased window size to fit everything comfortably
        top.configure(bg="#00796b")

        # Title Label for the booking window
        title_label = tk.Label(top, text="Select a Room to Book", font=("Helvetica", 16, "bold"), bg="#00796b",
                               fg="white")
        title_label.pack(pady=10)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(top)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display available rooms
        room_listbox = tk.Listbox(top, selectmode=tk.SINGLE, height=10, width=40, font=("Helvetica", 12), bg="#e0f7fa",
                                  fg="black", selectbackground="#004d40")
        room_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Add available rooms to the listbox
        for room in available_rooms:
            room_listbox.insert(tk.END, room)

        room_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=room_listbox.yview)

        # Add a button to confirm the booking
        def confirm_booking():
            selected_room = room_listbox.curselection()
            if selected_room:
                room_details = room_listbox.get(selected_room)
                room_number = int(room_details.split()[1])  # Extract the room number from the string
                message = self.hotel.book_room(room_number)
                self.show_custom_window("Booking Result", message)
                top.destroy()  # Close the booking window after booking
            else:
                self.show_custom_window("Booking Error", "Please select a room to book.")

        # Add the confirm booking button with styled colors, placed below the listbox
        confirm_button = tk.Button(top, text="Confirm Booking", command=confirm_booking, font=("Helvetica", 14),
                                   bg="#26a69a", fg="white", activebackground="#004d40", relief=tk.RAISED)
        confirm_button.pack(pady=10, side=tk.BOTTOM)

    def vacate_room(self):
        occupied_rooms = self.hotel.get_occupied_rooms()
        if not occupied_rooms:
            self.show_custom_window("Vacate Error", "No rooms are currently occupied.")
            return

        # Create a top-level window for vacating a room
        top = tk.Toplevel(self.root)
        top.title("Occupied Rooms")
        top.geometry("600x500")  # Increased window size for occupied room list
        top.configure(bg="#00796b")

        # Title Label for the vacate window
        title_label = tk.Label(top, text="Select a Room to Vacate", font=("Helvetica", 16, "bold"), bg="#00796b",
                               fg="white")
        title_label.pack(pady=10)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(top)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display occupied rooms
        room_listbox = tk.Listbox(top, selectmode=tk.SINGLE, height=10, width=40, font=("Helvetica", 12), bg="#e0f7fa",
                                  fg="black", selectbackground="#004d40")
        room_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Add occupied rooms to the listbox
        for room in occupied_rooms:
            room_listbox.insert(tk.END, room)

        room_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=room_listbox.yview)

        # Add a button to confirm vacating the room
        def confirm_vacate():
            selected_room = room_listbox.curselection()
            if selected_room:
                room_details = room_listbox.get(selected_room)
                room_number = int(room_details.split()[1])  # Extract the room number from the string
                message = self.hotel.vacate_room(room_number)
                self.show_custom_window("Vacating Result", message)
                top.destroy()  # Close the vacate window after vacating
            else:
                self.show_custom_window("Vacate Error", "Please select a room to vacate.")

        # Add the confirm vacate button with styled colors, placed below the listbox
        vacate_button = tk.Button(top, text="Confirm Vacate", command=confirm_vacate, font=("Helvetica", 14),
                                  bg="#26a69a", fg="white", activebackground="#004d40", relief=tk.RAISED)
        vacate_button.pack(pady=10, side=tk.BOTTOM)

    def search_rooms(self):
        while True:
            try:
                min_price = self.get_input("Enter Minimum Price (or leave blank to exit):")
                if not min_price:
                    break
                min_price = int(min_price)

                max_price = self.get_input("Enter Maximum Price:")
                if not max_price:
                    break
                max_price = int(max_price)

                if min_price > max_price:
                    self.show_custom_window("Error", "Minimum price cannot be greater than maximum price.")
                    continue

                room_type = self.get_room_type()
                if room_type is None:
                    break

                rooms = self.hotel.search_rooms(min_price, max_price, room_type)
                if not rooms:
                    self.show_custom_window("Search Results", "No rooms match your criteria.")
                else:
                    self.show_search_results_and_book(rooms)
                break  # Ensure the loop exits after the search is completed
            except ValueError:
                self.show_custom_window("Error", "Invalid input. Please enter numeric values for prices.")

    def show_search_results_and_book(self, rooms):
        # Create a top-level window to show search results
        top = tk.Toplevel(self.root)
        top.title("Search Results")
        top.geometry("600x500")
        top.configure(bg="#00796b")

        title_label = tk.Label(top, text="Available Rooms for Your Search", font=("Helvetica", 16, "bold"),
                               bg="#00796b", fg="white")
        title_label.pack(pady=10)

        # Create a scrollbar
        scrollbar = tk.Scrollbar(top)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

        # Create a listbox to display search results
        room_listbox = tk.Listbox(top, selectmode=tk.SINGLE, height=10, width=40, font=("Helvetica", 12), bg="#e0f7fa",
                                  fg="black", selectbackground="#004d40")
        room_listbox.pack(side=tk.LEFT, fill=tk.BOTH, padx=10, pady=10)

        # Add rooms to the listbox
        for room in rooms:
            room_listbox.insert(tk.END, room)

        room_listbox.config(yscrollcommand=scrollbar.set)
        scrollbar.config(command=room_listbox.yview)

        # Add a button to confirm booking
        def confirm_booking_from_search():
            selected_room = room_listbox.curselection()
            if selected_room:
                room_details = room_listbox.get(selected_room)
                room_number = int(room_details.split()[1])  # Extract the room number from the string
                message = self.hotel.book_room(room_number)
                self.show_custom_window("Booking Result", message)
                top.destroy()  # Close the search results window after booking
            else:
                self.show_custom_window("Booking Error", "Please select a room to book.")

        confirm_button = tk.Button(top, text="Confirm Booking", command=confirm_booking_from_search,
                                   font=("Helvetica", 14), bg="#26a69a", fg="white", activebackground="#004d40",
                                   relief=tk.RAISED)
        confirm_button.pack(pady=10, side=tk.BOTTOM)

    def get_input(self, prompt):
        return self.show_input_window(prompt)

    def get_room_type(self):
        room_types = {"1": "Single", "2": "Double", "3": "Suite", "4": None}
        choice = self.show_input_window(
            "1. Single\n2. Double\n3. Suite\n4. Any", title="Room Type Selection"
        )
        return room_types.get(choice)

    def show_input_window(self, prompt, title="Enter Information"):
        if self.input_window and self.input_window.winfo_exists():
            return None

        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("400x200")
        top.configure(bg="#00796b")
        self.input_window = top

        label = tk.Label(top, text=prompt, font=("Helvetica", 14), bg="#00796b", fg="white", padx=10, pady=10)
        label.pack(pady=20)

        input_field = tk.Entry(top, font=("Helvetica", 14), bd=2, relief=tk.SUNKEN)
        input_field.pack(pady=10, padx=20, fill=tk.X)
        input_field.focus()

        result = []

        def submit_input(event=None):
            result.append(input_field.get())
            top.destroy()

        input_field.bind("<Return>", submit_input)

        submit_button = tk.Button(top, text="Submit", command=submit_input, font=("Helvetica", 12), bg="#26a69a",
                                  fg="white")
        submit_button.pack(pady=10)

        top.wait_window()
        return result[0] if result else None

    def show_custom_window(self, title, message):
        top = tk.Toplevel(self.root)
        top.title(title)
        top.geometry("300x150")
        top.configure(bg="#00796b")

        label = tk.Label(top, text=message, font=("Helvetica", 12), bg="#00796b", fg="white", padx=10, pady=10)
        label.pack(pady=30)

        close_button = tk.Button(top, text="Close", command=top.destroy, font=("Helvetica", 12), bg="#26a69a",
                                 fg="white")
        close_button.pack(pady=10)


def main():
    hotel = Hotel("Diu Inn")
    for i in range(1, 6):
        hotel.add_room(SingleRoom(i))
    for i in range(6, 11):
        hotel.add_room(DoubleRoom(i))
    for i in range(11, 16):
        hotel.add_room(SuiteRoom(i))

    root = tk.Tk()
    app = HotelApp(root, hotel)
    root.mainloop()


if __name__ == "__main__":
    main()
