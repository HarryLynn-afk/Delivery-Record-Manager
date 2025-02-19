import datetime
import random
import csv
import os
import re
from prettytable import PrettyTable

# Delivery Service Class
class DeliveryService:
    def __init__(self, file_name):
        """
        Initialize the delivery service with a CSV file.
        """
        self.file_name = os.path.join(os.path.dirname(__file__), "delivery_data.csv")
        self.initialize_csv()

    def initialize_csv(self):
        """
        Create the CSV file with required headers if it does not exist.
        """
        try:
            if not os.path.exists(self.file_name):
               with open(self.file_name, "w", newline="") as file:
                  writer = csv.writer(file)
                  writer.writerow(["Date", "Order ID", "Full Name", "Phone", "Email", "Delivery Address",
                                   "City", "Postal Code", "Product Name", "Quantity", "Payment Method",
                                   "Transaction ID", "Tracking Number", "Delivery Status", "Amount"])
        except Exception as e:
            print(f"Error creating CSV file:{e}")
    @staticmethod
    def is_valid_phone(phone):
        """
        Validate a Thai phone number.
        """
        return re.fullmatch(r"^0[689]\d{8}$", phone) is not None

    @staticmethod
    def is_valid_email(email):
        """
        Validate email format.
        """
        return re.fullmatch(r"^[\w.-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$", email) is not None

    def read_csv(self):
        """
        Read data from the CSV file and validate row lengths.
        """
        try:
            with open(self.file_name, "r") as file:
                rows = list(csv.reader(file))
                # Validate each row against the header length
                valid_rows = [row for row in rows if len(row) == len(rows[0])]
                if len(valid_rows) != len(rows):
                    print("Warning: Some rows had incorrect lengths and were skipped.")
                return valid_rows
        except FileNotFoundError:
            return []

    def append_to_csv(self, row):
        """
        Append a new row to the CSV file.
        """
        with open(self.file_name, "a", newline="") as file:
            writer = csv.writer(file)
            writer.writerow(row)

    def add_new_delivery(self):
        """
        Add a new delivery record to the system.
        """
        today_date = datetime.date.today()
        order_id = f"OD{random.randint(10000, 99999)}"
        tracking_number = f"TN{random.randint(100000, 999999)}"

        # Collect user details
        full_name = input("Enter Full Name: ").strip()
        phone = self.prompt_valid_input("Enter Phone Number: ", self.is_valid_phone, "Invalid phone number.")
        email = self.prompt_valid_input("Enter Email: ", self.is_valid_email, "Invalid email address.")

        # Collect delivery details
        address = input("Enter Delivery Address: ").strip()
        city = input("Enter City: ").strip()
        postal_code = input("Enter Postal Code: ").strip()

        # Collect product details
        product_name = input("Enter Product Name: ").strip()
        quantity = self.prompt_positive_int("Enter Quantity: ")

        # Collect payment details
        payment_method = input("Enter Payment Method (e.g., Credit Card, Cash): ").strip()
        transaction_id = f"TX{random.randint(10000, 99999)}"

        # Calculate amount
        amount = 50 * quantity  # Flat rate of 50 THB per item

        # Append to file
        self.append_to_csv([today_date, order_id, full_name, phone, email, address, city, postal_code, 
                            product_name, quantity, payment_method, transaction_id, tracking_number, 
                            "Pending", amount])

        # Display receipt
        self.show_receipt(order_id)

    def show_receipt(self, order_id):
        """
        Display a receipt for a given order ID using PrettyTable.
        """
        rows = self.read_csv()
        for row in rows:
            if row[1] == order_id:
                table = PrettyTable(["Field", "Value"])
                headers = [
                    "Date", "Order ID", "Full Name", "Phone", "Email", 
                    "Delivery Address", "City", "Postal Code", "Product Name", 
                    "Quantity", "Payment Method", "Transaction ID", 
                    "Tracking Number", "Delivery Status", "Amount"
                ]
                for header, value in zip(headers, row):
                    table.add_row([header, value])
                print("\n--- Receipt ---")
                print(table)
                break

    @staticmethod
    def prompt_valid_input(prompt, validation_func, error_message):
        """
        Prompt user for input and validate using a given function.
        """
        while True:
            user_input = input(prompt).strip()
            if validation_func(user_input):
                return user_input
            print(error_message)

    @staticmethod
    def prompt_positive_int(prompt):
        """
        Prompt user for a positive integer input.
        """
        while True:
            try:
                value = int(input(prompt))
                if value > 0:
                    return value
                print("Value must be a positive integer.")
            except ValueError:
                print("Invalid input. Please enter a positive integer.")

    def display_all_information(self):
        """
        Display all delivery records in a paginated tabular format with sorting.
        """
        rows = self.read_csv()
        if len(rows) > 1:
            # Sorting options
            print("Sort by: 1-Date, 2-Name, 3-Status")
            sort_choice = input("Enter choice: ").strip()
            if sort_choice == "1":
                rows[1:] = sorted(rows[1:], key=lambda x: x[0])  # Sort by Date
            elif sort_choice == "2":
                rows[1:] = sorted(rows[1:], key=lambda x: x[2].lower())  # Sort by Full Name
            elif sort_choice == "3":
                rows[1:] = sorted(rows[1:], key=lambda x: x[13].lower())  # Sort by Delivery Status

            # Pagination
            page_size = 10
            total_pages = (len(rows) - 1 + page_size - 1) // page_size  # Calculate total pages
            current_page = 1

            while True:
                start = (current_page - 1) * page_size + 1
                end = start + page_size
                table = PrettyTable(rows[0])
                for row in rows[start:end]:
                    table.add_row(row)
                print(f"\n--- All Delivery Records (Page {current_page}/{total_pages}) ---")
                print(table)

                if current_page == total_pages:
                    break

                next_page = input("Press Enter for next page, or type 'exit' to stop: ").strip().lower()
                if next_page == 'exit':
                    break
                current_page += 1
        else:
            print("No data available.")

    def display_total_count(self):
        """
        Display the total number of delivery records.
        """
        rows = self.read_csv()
        count = len(rows) - 1  # Exclude header row
        print(f"\nTotal Deliveries: {count}")

    def search_delivery(self):
        """
        Search for a delivery by name or order ID.
        """
        search_term = input("Enter Full Name or Order ID to search: ").strip().lower()
        rows = self.read_csv()
        results = [row for row in rows if any(search_term in cell.lower() for cell in row)]

        if results:
            print("\n--- Search Results ---")
            table = PrettyTable(rows[0])
            for result in results:
                table.add_row(result)
            print(table)
        else:
            print("No matching records found.")

    def delete_delivery(self):
        """
        Delete a delivery record by order ID.
        """
        order_id = input("Enter Order ID to delete: ").strip()
        rows = self.read_csv()
        updated_rows = [rows[0]] + [row for row in rows[1:] if row[1] != order_id]

        if len(rows) != len(updated_rows):
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            print(f"Record with Order ID {order_id} deleted successfully.")
        else:
            print("Order ID not found.")

    def update_delivery(self):
        """
        Update delivery information by order ID.
        """
        order_id = input("Enter Order ID to update: ").strip()
        rows = self.read_csv()
        updated_rows = []
        updated = False

        for row in rows:
            if row[1] == order_id:
                print("\n--- Current Record ---")
                print(", ".join(row))

                print("\n--- Enter Updated Information ---")
                def update_field(prompt, current_value):
                    return input(f"{prompt} ({current_value}): ") or current_value

                full_name = update_field("Full Name", row[2])
                phone = update_field("Phone", row[3])
                email = update_field("Email", row[4])
                address = update_field("Delivery Address", row[5])
                city = update_field("City", row[6])
                postal_code = update_field("Postal Code", row[7])
                product_name = update_field("Product Name", row[8])
                quantity = update_field("Quantity", row[9])
                payment_method = update_field("Payment Method", row[10])
                delivery_status = update_field("Delivery Status", row[13])

                updated_row = [row[0], order_id, full_name, phone, email, address, city, postal_code,
                               product_name, quantity, payment_method, row[11], row[12], delivery_status, row[14]]
                updated_rows.append(updated_row)
                updated = True

                # Display updated receipt
                self.show_receipt(order_id)
            else:
                updated_rows.append(row)

        if updated:
            with open(self.file_name, "w", newline="") as file:
                writer = csv.writer(file)
                writer.writerows(updated_rows)
            print("Record updated successfully.")
        else:
            print("Order ID not found.")

def main():
    """
    Main function to run the delivery service application.
    """
    service = DeliveryService("delivery_data.csv")

    while True:
        print("\n--- Delivery Service Menu ---")
        print("1. Add New Delivery")
        print("2. Display All Deliveries")
        print("3. Display Total Deliveries")
        print("4. Search Delivery")
        print("5. Delete Delivery")
        print("6. Update Delivery")
        print("7. Exit")

        choice = input("Enter your choice: ").strip()

        if not choice.isdigit():
            print("Invalid input. Please enter a number.")
            continue

        choice = int(choice)

        try:
            if choice == 1:
                service.add_new_delivery()
            elif choice == 2:
                service.display_all_information()
            elif choice == 3:
                service.display_total_count()
            elif choice == 4:
                service.search_delivery()
            elif choice == 5:
                service.delete_delivery()
            elif choice == 6:
                service.update_delivery()
            elif choice == 7:
                print("Exiting the Delivery Service. Goodbye!")
                break
            else:
                print("Invalid choice. Please try again.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()
