# use of tabulate
from entity.ICustomerService import ICustomerService
from entity.Customer import Customer
from util.db_conn_util import get_connection
from exception.AuthenticationException import AuthenticationException
from exception.InvalidInputException import InvalidInputException

class CustomerService(ICustomerService):
    def __init__(self):
        pass

    def authenticate_customer_data(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "SELECT * FROM Customer WHERE Username = ?"
        cursor.execute(select_query, (username,))
        customer_data = cursor.fetchone()
        if customer_data:
            customer = Customer(*customer_data)
            if customer.authenticate(password):
                print("Authentication Successful!")
            else:
                raise AuthenticationException("Authentication failed-- Invalid password.")
        else:
            raise AuthenticationException("Authentication failed-- Invalid username.")
        cursor.close()
        conn.close()

    def authenticate_customer_(self, name):
        if name.isalpha():
            return True
        else:
            raise InvalidInputException("Enter Correct Details...")

    def authenticate_phone(self, phone_number):
        if phone_number.isalnum() and len(phone_number) == 10:
            return True
        else:
            if len(phone_number) != 10:
                raise InvalidInputException("Enter 10 Digit Phone Number.")
            else:
                raise InvalidInputException("Enter Digits only...")

    def register_customer(self):
        customer = Customer()
        try:
            first_name = input("Enter First Name of Customer: ")
            if self.authenticate_customer_(first_name):
                customer.set_first_name(first_name)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        try:
            last_name = input("Enter Last Name of Customer: ")
            if self.authenticate_customer_(last_name):
                customer.set_last_name(last_name)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        customer.set_email(input("Enter Email of Customer: "))
        try:
            phone_number = input("Enter Phone Number of Customer: ")
            if self.authenticate_phone(phone_number):
                customer.set_phone_number(phone_number)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        customer.set_address(input("Enter Address of Customer: "))
        customer.set_username(input("Enter Username of Customer: "))
        customer.set_password(input("Enter Password of Customer: "))
        customer.set_registration_date(input("Enter Registration Date {YYYY-MM-DD}: "))

        conn = get_connection()
        cursor = conn.cursor()
        insert_query = 'INSERT INTO Customer(FirstName, LastName, Email, PhoneNumber, Address, Username, Password, RegistrationDate) VALUES (?, ?, ?, ?, ?, ?, ?, ?)'
        try:
            cursor.execute(insert_query, (
                customer.get_first_name(), customer.get_last_name(), customer.get_email(),
                customer.get_phone_number(), customer.get_address(), customer.get_username(),
                customer.get_password(), customer.get_registration_date()
            ))
            conn.commit()
            print("Record inserted successfully.")
        except Exception as e:
            print(f"Error inserting record: {e}")
        finally:
            cursor.close()
            conn.close()

    def update_customer(self):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        try:
            self.authenticate_customer_data(username, password)
        except AuthenticationException as e:
            print(e)
            return
        conn = get_connection()
        cursor = conn.cursor()
        user_name = int(input("Enter Username to be updated: "))
        customer = Customer()
        try:
            first_name = input("Enter First Name of Customer: ")
            if self.authenticate_customer_(first_name):
                customer.set_first_name(first_name)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        try:
            last_name = input("Enter Last Name of Customer: ")
            if self.authenticate_customer_(last_name):
                customer.set_last_name(last_name)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        customer.set_email(input("Enter Email of Customer: "))
        try:
            phone_number = input("Enter Phone Number of Customer: ")
            if self.authenticate_phone(phone_number):
                customer.set_phone_number(phone_number)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        customer.set_address(input("Enter Address: "))

        update_query = 'UPDATE Customer SET FirstName = ?, LastName = ?, Email = ?, PhoneNumber = ?, Address = ? WHERE Username = ?'
        try:
            cursor.execute(update_query, (
                customer.get_first_name(), customer.get_last_name(), customer.get_email(),
                customer.get_phone_number(), customer.get_address(), user_name
            ))
            conn.commit()
            print("Record updated successfully.")
        except Exception as e:
            print(f"Error updating record: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_customer(self):
        user_name = int(input("Enter Username to be deleted: "))
        conn = get_connection()
        cursor = conn.cursor()
        try:
            select_query = "SELECT * FROM Customer WHERE Username = ?"
            cursor.execute(select_query, (user_name,))
            customer_data = cursor.fetchone()
            if customer_data:
                delete_query = "DELETE FROM Customer WHERE Username = ?"
                cursor.execute(delete_query, (user_name,))
                conn.commit()
                print("Record deleted successfully.")
            else:
                raise InvalidInputException("Username not found in Database.")
        except InvalidInputException as e:
            print(f"Customer Deletion Failed: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_customer_by_id(self):
        customer_id = int(input("Enter CustomerId to get details: "))
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "SELECT * FROM Customer WHERE CustomerID = ?"
        try:
            cursor.execute(select_query, (customer_id,))
            records = cursor.fetchall()
            if records:
                print(f"...............Customer Details for customerID: {customer_id}...............")
                for record in records:
                    print(record)
            else:
                raise InvalidInputException("CustomerID not found in Database.")
        except InvalidInputException as e:
            print(f"Customer Not Found: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_customer_by_username(self):
        username = input("Enter Username to get details: ")
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "SELECT * FROM Customer WHERE Username = ?"
        try:
            cursor.execute(select_query, (username,))
            records = cursor.fetchall()
            if records:
                print(f"...............Customer Details for Username: {username}...............")
                for record in records:
                    print(record)
            else:
                raise InvalidInputException("Invalid Username.")
        except InvalidInputException as e:
            print(f"Customer Not Found: {e}")
        finally:
            cursor.close()
            conn.close()

    def select_customers(self):
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "SELECT * FROM Customer"
        cursor.execute(select_query)
        records = cursor.fetchall()
        print("...............Records in Table...............")
        for record in records:
            print(record)
        cursor.close()
        conn.close()

