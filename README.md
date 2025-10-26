This is a simple, command-line interface (CLI) application built with Python for managing the core operations of a small logistics or delivery business. It provides a menu-driven interface to handle vehicles, customers, shipments, and deliveries without requiring any external libraries.

✨ Features
The application is organized into four main management modules:

🚚 Fleet Management
Add a vehicle: Add new vehicles (e.g., Truck, Van) to the fleet with a unique ID and carrying capacity.

Update vehicle information: Modify the type and capacity of existing vehicles.

Remove a vehicle: Delete a vehicle from the fleet.

View all vehicles: Display a list of all vehicles in the fleet, including their ID, type, capacity, and current availability status (Available or Assigned).

👤 Customer Management
Add a customer: Register new customers with validation for their ID, date of birth (must be 18+), Australian address, phone number, and email.

Update customer information: Edit the details of an existing customer.

Remove a customer: Delete a customer's record.

View all customers: See a complete list of registered customers.

View a customer's shipments: Look up a specific customer by their ID and view their entire shipment history.

📦 Shipment Management
Create a new shipment: Log a new shipment by providing origin, destination, and weight. The system allows you to assign an available vehicle from the fleet and link the shipment to an existing customer.

Track a shipment: Check the current status of any shipment using its ID.

View all shipments: Get a comprehensive list of all shipments, both "In transit" and "Delivered".

✅ Delivery Management
Mark a shipment as delivered: Update a shipment's status to "Delivered" and record the delivery date and time.

Release vehicles: Marking a shipment as delivered automatically sets the assigned vehicle's status back to "Available", making it ready for a new shipment.

View delivery status: Check if a specific shipment has been delivered and, if so, view the delivery timestamp.
