from entity.IAdminService import IAdminService
from entity.Admin import Admin
from util.DBConnection import get_connection
from exception.AdminNotFoundException import AdminNotFoundException
from exception.InvalidInputException import InvalidInputException


class AdminService(IAdminService):
    def __init__(self):
        super().__init__()

    def authenticate_admin_data(self, username, password):
        conn = get_connection()
        cursor = conn.cursor()
        select_query = "SELECT * FROM Admin WHERE Username = ?;"
        cursor.execute(select_query, (username,))
        admin_data = cursor.fetchone()
        if admin_data:
            admin = Admin(*admin_data)
            if admin.authenticate(password):
                print("Authentication successful!")
            else:
                raise AdminNotFoundException("Authentication failed-- Invalid password.")
        else:
            raise AdminNotFoundException("Authentication failed-- Invalid username.")
        cursor.close()
        conn.close()

    def authenticate_admin(self, name):
        if name.isalpha():
            return True
        else:
            raise InvalidInputException("Enter Correct Details...")

    def authenticate_phone(self, phone_number):
        if phone_number.isdigit() and len(phone_number) == 10:
            return True
        else:
            if len(phone_number) != 10:
                raise InvalidInputException("Enter 10 Digit PhoneNo")
            else:
                raise InvalidInputException("Enter Digits only...")

    def register_admin(self):
        admin = Admin()
        try:
            first_name = input("Enter First Name: ")
            if self.authenticate_admin(first_name):
                admin.set_first_name(first_name)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        try:
            last_name = input("Enter Last Name: ")
            if self.authenticate_admin(last_name):
                admin.set_last_name(last_name)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        admin.set_email(input("Enter Email: "))
        try:
            phone_number = input("Enter Phone Number: ")
            if self.authenticate_phone(phone_number):
                admin.set_phone_number(phone_number)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        admin.set_username(input("Enter Username: "))
        admin.set_password(input("Enter Password: "))
        admin.set_role(input("Enter Role (Super admin / fleet manager): "))
        admin.set_join_date(input("Enter Join Date (YYYY-MM-DD): "))

        conn = get_connection()
        cursor = conn.cursor()
        insert_query = '''
        INSERT INTO Admin (FirstName, LastName, Email, PhoneNumber, Username, Password, Role, JoinDate)
        OUTPUT INSERTED.AdminID VALUES (?, ?, ?, ?, ?, ?, ?, ?);
        '''
        cursor.execute(insert_query, (admin.get_first_name(), admin.get_last_name(), admin.get_email(),
                                      admin.get_phone_number(), admin.get_username(), admin.get_password(),
                                      admin.get_role(), admin.get_join_date()))
        admin_id = cursor.fetchone()[0]
        conn.commit()
        print(f"Admin registered successfully with AdminID: {admin_id}")
        cursor.close()
        conn.close()

    def update_admin(self):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        try:
            self.authenticate_admin_data(username, password)
        except AdminNotFoundException as e:
            print(e)
            return
        try:
            self.select_admin()
            admin_id = int(input("Enter AdminID to be updated: "))
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT AdminID FROM ADMIN WHERE AdminID = ?;"
            cursor.execute(query, (admin_id,))
            record = cursor.fetchone()
            if record:
                admin = Admin()
                try:
                    first_name = input("Enter First Name: ")
                    if self.authenticate_admin(first_name):
                        admin.set_first_name(first_name)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return
                try:
                    last_name = input("Enter Last Name: ")
                    if self.authenticate_admin(last_name):
                        admin.set_last_name(last_name)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return
                admin.set_email(input("Enter Email: "))
                try:
                    phone_number = input("Enter Phone Number: ")
                    if self.authenticate_phone(phone_number):
                        admin.set_phone_number(phone_number)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return
                admin.set_username(input("Enter Username: "))
                admin.set_password(input("Enter Password: "))
                admin.set_role(input("Enter Role (Super admin / fleet manager) : "))
                admin.set_join_date(input("Enter Join Date (YYYY-MM-DD): "))

                update_str = '''
                        UPDATE Admin SET FirstName = ?, LastName = ?, Email = ?, PhoneNumber = ?, 
                        Username = ?, Password = ?, Role = ?, JoinDate = ? WHERE AdminID = ?
                        '''
                cursor.execute(update_str, (admin.get_first_name(), admin.get_last_name(), admin.get_email(),
                                            admin.get_phone_number(), admin.get_username(), admin.get_password(),
                                            admin.get_role(), admin.get_join_date(), admin_id))
                conn.commit()
                print("Admin Updated Successfully...")
            else:
                raise AdminNotFoundException("AdminID not found in Database...")
        except AdminNotFoundException as e:
            print(f"Admin Updation Failed: {e}")
        finally:
            cursor.close()
            conn.close()

    def delete_admin(self):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        try:
            self.authenticate_admin_data(username, password)
        except AdminNotFoundException as e:
            print(e)
            return
        try:
            admin_id = int(input("Enter AdminID to be deleted: "))
            conn = get_connection()
            cursor = conn.cursor()
            query = "SELECT AdminID FROM ADMIN WHERE AdminID = ?;"
            cursor.execute(query, (admin_id,))
            record = cursor.fetchone()
            if record:
                delete_str = "DELETE FROM Admin WHERE AdminID = ?;"
                cursor.execute(delete_str, (admin_id,))
                conn.commit()
                print("Admin Deleted Successfully...")
            else:
                raise AdminNotFoundException("AdminID not found in Database...")
        except AdminNotFoundException as e:
            print(f"Admin Not Found: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_admin_by_id(self):
        try:
            admin_id = int(input("Enter AdminID to get details: "))
            conn = get_connection()
            cursor = conn.cursor()
            admin_str = "SELECT * FROM Admin WHERE AdminID = ?;"
            cursor.execute(admin_str, (admin_id,))
            record = cursor.fetchone()
            if record:
                print(f"\n...............Admin Details for AdminID: {admin_id}...............\n")
                print(record)
            else:
                raise AdminNotFoundException("AdminID not found in Database...")
        except AdminNotFoundException as e:
            print(f"Admin Not Found: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_admin_by_username(self):
        try:
            username = input("Enter Username to get details: ")
            conn = get_connection()
            cursor = conn.cursor()
            admin_str = "SELECT * FROM Admin WHERE Username = ?;"
            cursor.execute(admin_str, (username,))
            records = cursor.fetchall()
            if records:
                print(f"\n...............Admin Details for Username: {username}...............\n")
                for record in records:
                    print(record)
            else:
                raise AdminNotFoundException("Invalid Username...")
        except AdminNotFoundException as e:
            print(f'Admin Not Found: {e}')
        finally:
            cursor.close()
            conn.close()

    def select_admin(self):
        username = input("Enter Username: ")
        password = input("Enter Password: ")
        try:
            self.authenticate_admin_data(username, password)
        except AdminNotFoundException as e:
            print(e)
            return
        conn = get_connection()
        cursor = conn.cursor()
        select_str = 'SELECT * FROM Admin;'
        cursor.execute(select_str)
        records = cursor.fetchall()
        print("\n...............Records in Admin Table...............\n")
        for record in records:
            print(record)
        cursor.close()
        conn.close()
