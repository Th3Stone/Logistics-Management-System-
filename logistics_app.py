# -*- coding: utf-8 -*-
"""
Created on Fri Aug 01 09:28:53 2025

@author: Jose Piedrahita 
"""

CURRENT_DAY = 11
CURRENT_MONTH = 8
CURRENT_YEAR = 2025

AU_STATES = ["NSW", "QLD", "VIC", "SA", "WA", "TAS", "ACT", "NT"]

class Vehicle:
    def __init__(self, vehicle_id, vehicle_type, capacity):
        self.vehicle_id = vehicle_id  
        self.vehicle_type = vehicle_type  
        self.capacity = capacity  
        self.available = True 

    def __str__(self):
        avail = "Available" if self.available else "Assigned"
        return f"{self.vehicle_id}\t{self.vehicle_type}\t{self.capacity} kg\t{avail}"

class Customer:
    def __init__(self, customer_id, name, dob, address, phone, email):
        self.customer_id = customer_id  
        self.name = name
        self.dob = dob  
        self.address = address
        self.phone = phone
        self.email = email

    def __str__(self):
        return f"{self.customer_id}\t{self.name}\t{self.address}\t{self.phone} / {self.email}"

class Shipment:
    def __init__(self, shipment_id, origin, destination, weight, vehicle_id, customer_id):
        self.shipment_id = shipment_id  
        self.origin = origin
        self.destination = destination
        self.weight = weight  
        self.vehicle_id = vehicle_id
        self.customer_id = customer_id
        self.status = "In transit" 
        self.delivery_date = None  
        self.delivery_time = None

    def __str__(self):
        dd = self.delivery_date if self.delivery_date else ""
        dt = self.delivery_time if self.delivery_time else ""
        return (f"{self.shipment_id}\t{self.origin}\t{self.destination}\t"
                f"{self.weight} kg\t{self.vehicle_id}\t{self.status}\t{dd} {dt}")

# Lists
fleet = []       
customers = []   
shipments = []    


# Validations for inputs
def valid_id_format(identifier):
    if not identifier:
        return False
    id_up = identifier.strip()
    return id_up.isalnum() and 3 <= len(id_up) <= 10

def valid_vehicle_capacity(cap_str):
    if not cap_str.isdigit():
        return False
    return int(cap_str) > 0

def valid_weight_numeric(w_str):
    try:
        w = float(w_str)
        return w > 0
    except:
        return False

def parse_int_safe(s):
    try:
        return int(s)
    except:
        return None

def valid_dob(dob_str):
    parts = dob_str.split("/")
    if len(parts) != 3:
        return False
    d, m, y = parts
    if not (d.isdigit() and m.isdigit() and y.isdigit() and len(y) == 4):
        return False
    day = int(d); month = int(m); year = int(y)
    if not (1 <= day <= 31 and 1 <= month <= 12 and 1900 <= year <= CURRENT_YEAR):
        return False
    if month == 2 and day > 29:
        return False
    age = CURRENT_YEAR - year
    if (month, day) > (CURRENT_MONTH, CURRENT_DAY):
        age -= 1
    return age >= 18

def valid_au_address(addr):
    if not addr or ", Australia" not in addr:
        return False
    tokens = addr.replace(",", " ").split()
    has_postcode = any(t.isdigit() and len(t) == 4 for t in tokens)
    has_state = any((" " + s + " ") in (" " + addr + " ") or ("," + s + ",") in addr or ("," + s + " ") in addr for s in AU_STATES)
    return has_postcode and has_state

def valid_phone(phone):
    return phone.isdigit() and len(phone) == 10

def valid_email(email):
    if "@" not in email:
        return False
    at_index = email.index("@")
    return "." in email[at_index+1:]

def valid_date_ddmmyyyy(date_str):
    parts = date_str.split("/")
    if len(parts) != 3:
        return False
    d, m, y = parts
    if not (d.isdigit() and m.isdigit() and y.isdigit() and len(y) == 4):
        return False
    day = int(d); month = int(m); year = int(y)
    if not (1 <= day <= 31 and 1 <= month <= 12):
        return False
    return True

def valid_time_hhmm(time_str):
    parts = time_str.split(":")
    if len(parts) != 2:
        return False
    hh, mm = parts
    if not (hh.isdigit() and mm.isdigit() and len(hh) <= 2 and len(mm) == 2):
        return False
    h = int(hh); m = int(mm)
    return 0 <= h <= 23 and 0 <= m <= 59

# Fleet Management menu

def add_vehicle_menu():
    print("\nAdd a vehicle")
    vid = input("Enter Vehicle ID (e.g., V001): ").strip().upper()
    if not valid_id_format(vid):
        print("Invalid Vehicle ID. Must be alphanumeric and 3-10 chars.")
        return
    if any(v.vehicle_id == vid for v in fleet):
        print("Vehicle ID already exists.")
        return
    vtype = input("Enter Vehicle Type (e.g., Truck, Van, Car): ").strip()
    cap_str = input("Enter Vehicle Capacity (kg) (positive integer): ").strip()
    if not valid_vehicle_capacity(cap_str):
        print("Invalid capacity. Must be a positive integer.")
        return
    capacity = int(cap_str)
    fleet.append(Vehicle(vid, vtype, capacity))
    print(f"Vehicle {vid} added successfully.")

def update_vehicle_menu():
    print("\nUpdate vehicle information")
    vid = input("Enter Vehicle ID to update: ").strip().upper()
    found = None
    for v in fleet:
        if v.vehicle_id == vid:
            found = v
            break
    if not found:
        print("Vehicle ID not found.")
        return
    vtype = input(f"Enter new Vehicle Type (current: {found.vehicle_type}): ").strip()
    cap_str = input(f"Enter new Vehicle Capacity (kg) (current: {found.capacity}): ").strip()
    if not valid_vehicle_capacity(cap_str):
        print("Invalid capacity. Must be a positive integer.")
        return
    found.vehicle_type = vtype
    found.capacity = int(cap_str)
    print(f"Vehicle {vid} updated successfully.")

def remove_vehicle_menu():
    print("\nRemove a vehicle")
    vid = input("Enter Vehicle ID to remove: ").strip().upper()
    for i, v in enumerate(fleet):
        if v.vehicle_id == vid:
            confirm = input(f"Are you sure you want to delete {vid}? (Y/N): ").strip().lower()
            if confirm == "y":
                fleet.pop(i)
                print(f"Vehicle {vid} removed.")
            else:
                print("Deletion cancelled.")
            return
    print("Vehicle ID not found.")

def view_vehicles_menu():
    print("\nView all vehicles")
    if not fleet:
        print("No vehicles in fleet.")
    else:
        print("VehicleID\tType\tCapacity\tStatus")
        for v in fleet:
            print(v)
    while True:
        cmd = input("Type 'exit' to return to Fleet Management Menu: ").strip().lower()
        if cmd == "exit":
            break

def fleet_management_menu():
    while True:
        print("\nFleet Management Menu:")
        print("1. Add a vehicle")
        print("2. Update vehicle information")
        print("3. Remove a vehicle")
        print("4. View all vehicles")
        print("5. Quit fleet management")
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_vehicle_menu()
        elif choice == "2":
            update_vehicle_menu()
        elif choice == "3":
            remove_vehicle_menu()
        elif choice == "4":
            view_vehicles_menu()
        elif choice == "5":
            break
        else:
            print("Invalid option. Choose 1-5.")

# Customer Management menu

def add_customer_menu():
    print("\nAdd a customer")
    cid = input("Enter unique Customer ID (e.g., ABC123): ").strip().upper()
    if not valid_id_format(cid):
        print("Invalid Customer ID. Must be alphanumeric and 3-10 chars.")
        return
    if any(c.customer_id == cid for c in customers):
        print("Customer ID already exists.")
        return
    name = input("Enter Name: ").strip()
    dob = input("Enter DOB (DD/MM/YYYY): ").strip()
    if not valid_dob(dob):
        print("Invalid DOB format or customer is under 18.")
        return
    address = input("Enter Address (include state and 4-digit postcode, end with ', Australia'): ").strip()
    if not valid_au_address(address):
        print("Invalid Australian address. Must include state and 4-digit postcode and end with ', Australia'.")
        return
    phone = input("Enter Phone (04XXXXXXXX): ").strip()
    if not valid_phone(phone):
        print("Invalid phone format.")
        return
    email = input("Enter Email: ").strip()
    if not valid_email(email):
        print("Invalid email format.")
        return
    customers.append(Customer(cid, name, dob, address, phone, email))
    print(f"Customer {cid} added successfully.")

def update_customer_menu():
    print("\nUpdate customer information")
    cid = input("Enter Customer ID to update: ").strip().upper()
    target = None
    for i, c in enumerate(customers):
        if c.customer_id == cid:
            target = customers[i]
            break
    if not target:
        print("Customer ID not found.")
        return

    name = input(f"Enter new Name (current: {target.name}): ").strip()
    if not name:
        name = target.name

    attempts = 0
    while attempts < 3:
        dob = input(f"Enter new DOB DD/MM/YYYY (current: {target.dob}): ").strip()
        if dob == "":
            dob = target.dob
            break
        if valid_dob(dob):
            break
        else:
            attempts += 1
            print(f"Invalid DOB or under 18. Attempts left: {3 - attempts}")
    if attempts >= 3 and not valid_dob(dob):
        print("Failed to update DOB after 3 attempts.")
        return

    attempts = 0
    while attempts < 3:
        address = input(f"Enter new Address (current: {target.address}): ").strip()
        if address == "":
            address = target.address
            break
        if valid_au_address(address):
            break
        else:
            attempts += 1
            print(f"Invalid Australian address. Attempts left: {3 - attempts}")
    if attempts >= 3 and not valid_au_address(address):
        print("Failed to update Address after 3 attempts.")
        return

    attempts = 0
    while attempts < 3:
        phone = input(f"Enter new Phone (current: {target.phone}): ").strip()
        if phone == "":
            phone = target.phone
            break
        if valid_phone(phone):
            break
        else:
            attempts += 1
            print(f"Invalid phone. Attempts left: {3 - attempts}")
    if attempts >= 3 and not valid_phone(phone):
        print("Failed to update Phone after 3 attempts.")
        return

    attempts = 0
    while attempts < 3:
        email = input(f"Enter new Email (current: {target.email}): ").strip()
        if email == "":
            email = target.email
            break
        if valid_email(email):
            break
        else:
            attempts += 1
            print(f"Invalid email. Attempts left: {3 - attempts}")
    if attempts >= 3 and not valid_email(email):
        print("Failed to update Email after 3 attempts.")
        return

    target.name = name
    target.dob = dob
    target.address = address
    target.phone = phone
    target.email = email
    print(f"Customer {cid} updated successfully.")

def remove_customer_menu():
    print("\nRemove a customer")
    cid = input("Enter Customer ID to remove: ").strip().upper()
    for i, c in enumerate(customers):
        if c.customer_id == cid:
            confirm = input(f"Are you sure you want to delete customer {cid}? (Y/N): ").strip().lower()
            if confirm == "y":
                customers.pop(i)
                print(f"Customer {cid} removed.")
            else:
                print("Deletion cancelled.")
            return
    print("Customer ID not found.")

def view_customers_menu():
    print("\nAll customers")
    if not customers:
        print("No customers found.")
        return
    print("CustomerID\tName\tAddress\tContact")
    for c in customers:
        print(c)

def view_customer_shipments_menu():
    print("\nView a customer's shipments")
    cid = input("Enter Customer ID: ").strip().upper()
    cust_exists = any(c.customer_id == cid for c in customers)
    if not cust_exists:
        print("Customer ID not found.")
        return
    found_shipments = [s for s in shipments if s.customer_id == cid]
    if not found_shipments:
        print("No shipments found for this customer.")
        return
    print("ShipmentID\tOrigin\tDestination\tWeight\tVehicleID\tStatus\tDeliveryDate Time")
    for s in found_shipments:
        dd = s.delivery_date if s.delivery_date else ""
        dt = s.delivery_time if s.delivery_time else ""
        print(f"{s.shipment_id}\t{s.origin}\t{s.destination}\t{s.weight} kg\t{s.vehicle_id}\t{s.status}\t{dd} {dt}")

def customer_management_menu():
    while True:
        print("\nCustomer Management Menu:")
        print("1. Add a customer")
        print("2. Update customer information")
        print("3. Remove a customer")
        print("4. View all customers")
        print("5. View a customer's shipments")
        print("6. Quit customer management")
        choice = input("Select an option: ").strip()
        if choice == "1":
            add_customer_menu()
        elif choice == "2":
            update_customer_menu()
        elif choice == "3":
            remove_customer_menu()
        elif choice == "4":
            view_customers_menu()
        elif choice == "5":
            view_customer_shipments_menu()
        elif choice == "6":
            break
        else:
            print("Invalid option. Choose 1-6.")

# Shipment Management mwnu

def create_shipment_menu():
    print("\nCreate a new shipment")
    sid = input("Enter Shipment ID (e.g., S123): ").strip().upper()
    if not valid_id_format(sid):
        print("Invalid Shipment ID. Must be alphanumeric and 3-10 chars.")
        return
    if any(s.shipment_id == sid for s in shipments):
        print("Shipment ID already exists.")
        return
    origin = input("Enter Origin (e.g., Sydney, NSW, Australia): ").strip()
    destination = input("Enter Destination (e.g., Melbourne, VIC, Australia): ").strip()
    weight_str = input("Enter Weight (kg): ").strip()
    if not valid_weight_numeric(weight_str):
        print("Invalid weight. Must be a positive number.")
        return
    weight = float(weight_str)

    available_vehicles = [v for v in fleet if v.available]
    if not available_vehicles:
        print("No available vehicles in fleet.")
        return
    print("Available Vehicles:")
    print("VehicleID\tType\tCapacity")
    for v in available_vehicles:
        print(f"{v.vehicle_id}\t{v.vehicle_type}\t{v.capacity} kg")
    vehicle_id = input("Select a Vehicle ID from the list: ").strip().upper()
    vehicle_obj = None
    for v in available_vehicles:
        if v.vehicle_id == vehicle_id:
            vehicle_obj = v
            break
    if not vehicle_obj:
        print("Invalid or unavailable Vehicle ID.")
        return

    customer_id = input("Enter Customer ID: ").strip().upper()
    if not any(c.customer_id == customer_id for c in customers):
        print("Customer ID not found.")
        return

    shipments.append(Shipment(sid, origin, destination, weight, vehicle_id, customer_id))
    vehicle_obj.available = False
    print(f"Shipment {sid} created successfully and vehicle {vehicle_id} assigned.")

def track_shipment_menu():
    print("\nTrack a shipment")
    sid = input("Enter Shipment ID to track: ").strip().upper()
    for s in shipments:
        if s.shipment_id == sid:
            print(f"Shipment {sid} status: {s.status}")
            if s.status == "Delivered":
                print(f"Delivered on: {s.delivery_date} {s.delivery_time}")
            return
    print("Shipment ID not found.")

def view_all_shipments_menu():
    print("\nAll shipments")
    if not shipments:
        print("No shipments found.")
        return
    print("ShipmentID\tOrigin\tDestination\tWeight\tVehicleID\tStatus\tDeliveryDate Time")
    for s in shipments:
        dd = s.delivery_date if s.delivery_date else ""
        dt = s.delivery_time if s.delivery_time else ""
        print(f"{s.shipment_id}\t{s.origin}\t{s.destination}\t{s.weight} kg\t{s.vehicle_id}\t{s.status}\t{dd} {dt}")

def shipment_management_menu():
    while True:
        print("\nShipment Management Menu:")
        print("1. Create a new shipment")
        print("2. Track a shipment")
        print("3. View all shipments")
        print("4. Quit shipment management")
        choice = input("Select an option (3.1-3.4): ").strip()
        if choice == "1":
            create_shipment_menu()
        elif choice == "2":
            track_shipment_menu()
        elif choice == "3":
            view_all_shipments_menu()
        elif choice == "4":
            break
        else:
            print("Invalid option. Choose 3.1-3.4.")

#  Delivery Management
def mark_shipment_delivery_menu():
    print("\nMark Shipment delivery")
    sid = input("Enter Shipment ID to mark as delivered: ").strip().upper()
    target = None
    for s in shipments:
        if s.shipment_id == sid:
            target = s
            break
    if not target:
        print("Shipment ID not found.")
        return
    if target.status == "Delivered":
        print("Shipment already delivered.")
        return

 
    date_in = input("Enter delivery date (DD/MM/YYYY): ").strip()
    if not valid_date_ddmmyyyy(date_in):
        print("Invalid date format.")
        return
    time_in = input("Enter delivery time (HH:MM, 24-hour): ").strip()
    if not valid_time_hhmm(time_in):
        print("Invalid time format.")
        return

    target.status = "Delivered"
    target.delivery_date = date_in
    target.delivery_time = time_in

    for v in fleet:
        if v.vehicle_id == target.vehicle_id:
            v.available = True
            break

    print(f"Shipment {sid} marked as Delivered on {date_in} {time_in}.")

def view_delivery_status_menu():
    print("\nView delivery status for a shipment")
    sid = input("Enter Shipment ID: ").strip().upper()
    for s in shipments:
        if s.shipment_id == sid:
            if s.status == "Delivered":
                print(f"Shipment {sid} delivered on {s.delivery_date} at {s.delivery_time}.")
            else:
                print(f"Shipment {sid} has not been delivered yet. Current status: {s.status}")
            return
    print("Shipment ID not found.")

def delivery_management_menu():
    while True:
        print("\nDelivery Management Menu:")
        print("1. Mark Shipment delivery")
        print("2. View delivery status for a shipment")
        print("3. Quit delivery management")
        choice = input("Select an option (4.1-4.3): ").strip()
        if choice == "1":
            mark_shipment_delivery_menu()
        elif choice == "2":
            view_delivery_status_menu()
        elif choice == "3":
            break
        else:
            print("Invalid option. Choose 1-3.")

# Main Menu
def main_menu():
    while True:
        print("\nMain Menu:")
        print("1 Fleet Management")
        print("2 Customer Management")
        print("3 Shipment Management")
        print("4 Delivery Management")
        print("0 Quit")
        choice = input("Select an option: ").strip()
        if choice == "1":
            fleet_management_menu()
        elif choice == "2":
            customer_management_menu()
        elif choice == "3":
            shipment_management_menu()
        elif choice == "4":
            delivery_management_menu()
        elif choice == "0":
            print("Exiting program. Goodbye.")
            break
        else:
            print("Invalid option. Choose 0-4.")





if __name__ == "__main__":
    main_menu()


