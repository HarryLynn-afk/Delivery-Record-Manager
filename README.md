# Delivery Service Management System

## Overview
This project is a **Delivery Service Management System** implemented in Python. It allows users to manage delivery orders, including adding new deliveries, searching, updating, and deleting records. The system stores data in a CSV file and provides user-friendly display formatting using the `PrettyTable` library.

## Features
- Add new delivery orders with automatic Order ID and Tracking Number generation.
- Validate phone numbers and email addresses.
- Store delivery records in a CSV file.
- Display all delivery records with pagination and sorting options.
- Search for a delivery by Full Name or Order ID.
- Update delivery information.
- Delete a delivery record.
- Display the total number of deliveries.
- User-friendly menu-driven interface.

## Technologies Used
- Python
- CSV for data storage
- `PrettyTable` for tabular data display
- Regular expressions for input validation
- `random` for generating unique Order IDs and Tracking Numbers

## Installation
### Prerequisites
Ensure you have **Python 3** installed on your system. You also need to install the required dependencies.

pip install prettytable

### Clone the Repository

git clone https://github.com/yourusername/delivery-service.git
cd delivery-service

## Usage
Run the application by executing the following command:

python delivery_service.py

You will be presented with the main menu where you can choose different actions.

## Project Structure
```
 delivery-service/
│--  delivery_service.py  # Main program file
│--  delivery_data.csv    # Data storage file
│--  README.md            # Project documentation
```

## How It Works
1. **Add a New Delivery**
   - The system prompts the user for delivery details.
   - Validates phone number and email format.
   - Saves the data in `delivery_data.csv`.
2. **View All Deliveries**
   - Displays all records in a table format with pagination.
   - Sort by Date, Name, or Delivery Status.
3. **Search for a Delivery**
   - Allows searching by Full Name or Order ID.
4. **Update a Delivery**
   - Edit details of an existing delivery.
5. **Delete a Delivery**
   - Remove a record by entering the Order ID.
6. **Display Total Deliveries**
   - Shows the total number of recorded deliveries.

## Example Usage
### Adding a New Delivery
```
Enter Full Name: John Doe
Enter Phone Number: 0812345678
Enter Email: john.doe@example.com
Enter Delivery Address: 123 Street, Bangkok
Enter City: Bangkok
Enter Postal Code: 10100
Enter Product Name: Laptop
Enter Quantity: 1
Enter Payment Method (e.g., Credit Card, Cash): Cash
```
### Searching for a Delivery
```
Enter Full Name or Order ID to search: OD12345
```
### Deleting a Delivery
```
Enter Order ID to delete: OD12345
Record with Order ID OD12345 deleted successfully.
```

## Contributions
Contributions are welcome! Feel free to submit a pull request or open an issue.

## License
This project is licensed under the **MIT License**.

## Author
[Your Name](https://github.com/yourusername)

