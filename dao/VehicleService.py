from entity.IVehicleService import IVehicleService
from entity.Vehicle import Vehicle
from util.DBConnection import get_connection
from exception.VehicleNotFoundException import VehicleNotFoundException
from exception.InvalidInputException import InvalidInputException


class VehicleService(IVehicleService):
    def __init__(self):
        pass

    def authenticate_name(self, name):
        if name.isalpha():
            return True
        else:
            raise InvalidInputException("Enter Correct Details...")

    def add_vehicle(self):
        conn = get_connection()
        cursor = conn.cursor()
        vehicle = Vehicle()
        try:
            model = input("Enter Model of Vehicle: ")
            if self.authenticate_name(model):
                vehicle.set_model(model)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        
        try:
            make = input("Enter Make of Vehicle: ")
            if self.authenticate_name(make):
                vehicle.set_make(make)
        except InvalidInputException as e:
            print(f'Invalid Input: {e}')
            return
        
        vehicle.set_year(int(input("Enter Year of Vehicle: ")))
        vehicle.set_color(input("Enter Color of Vehicle: "))
        vehicle.set_registration_number(input("Enter Registration Number of Vehicle: "))
        availability_input = input("Is Vehicle Available? (yes/no): ").lower()
        if availability_input in ['yes', 'no']:
            vehicle.set_availability(availability_input)
        else:
            raise InvalidInputException("Availability must be 'yes' or 'no'.")
        vehicle.set_daily_rate(float(input("Enter Daily Rate of Vehicle: ")))

        data = (vehicle.get_model(), vehicle.get_make(), vehicle.get_year(), vehicle.get_color(),
                vehicle.get_registration_number(), vehicle.get_availability(), vehicle.get_daily_rate())

        insert_query = '''
        INSERT INTO Vehicle (Model, Make, Year, Color, RegistrationNumber, Availability, DailyRate)
        VALUES (?, ?, ?, ?, ?, ?, ?);
        '''
        
        try:
            cursor.execute(insert_query, data)
            conn.commit()
            print("Vehicle added successfully...")
        except Exception as e:
            print(f"Error adding vehicle: {e}")

        finally:
            cursor.close()
            conn.close()


    def update_vehicle(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            self.select_vehicle()
            vehicle_id = int(input("Enter VehicleID to be updated: "))
            query = "SELECT VehicleID FROM Vehicle WHERE VehicleID = ?;"
            cursor.execute(query, (vehicle_id,))
            record = cursor.fetchone()
            if record:
                vehicle = Vehicle()
                try:
                    model = input("Enter Model of Vehicle: ")
                    if self.authenticate_name(model):
                        vehicle.set_model(model)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return
                
                try:
                    make = input("Enter Make of Vehicle: ")
                    if self.authenticate_name(make):
                        vehicle.set_make(make)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return
                
                vehicle.set_year(int(input("Enter Year: ")))
                vehicle.set_color(input("Enter Color: "))
                vehicle.set_registration_number(input("Enter Registration Number: "))
                availability_input = input("Is Vehicle Available? (yes/no): ").lower()
                if availability_input in ['yes', 'no']:
                    vehicle.set_availability(availability_input)
                else:
                    raise InvalidInputException("Availability must be 'yes' or 'no'.")
                vehicle.set_daily_rate(float(input("Enter Daily Rate: ")))

                update_str = '''
                    UPDATE Vehicle SET Model=?, Make=?, Year=?, Color=?, RegistrationNumber=?, Availability=?,
                    DailyRate=? WHERE VehicleID=?;
                '''
                data = (vehicle.get_model(), vehicle.get_make(), vehicle.get_year(), vehicle.get_color(),
                        vehicle.get_registration_number(), vehicle.get_availability(), vehicle.get_daily_rate(), vehicle_id)
                
                cursor.execute(update_str, data)
                conn.commit()
                print("Vehicle Updated Successfully...")
            else:
                raise VehicleNotFoundException("Invalid VehicleID...")
        except VehicleNotFoundException as e:
            print(f"Vehicle Updation Failed: {e}")
        
        finally:
            cursor.close()
            conn.close()

    def remove_vehicle(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            vehicle_id = int(input("Enter VehicleID to be deleted: "))
            query = "SELECT VehicleID FROM Vehicle WHERE VehicleID = ?;"
            cursor.execute(query, (vehicle_id,))
            record = cursor.fetchone()
            if record:
                delete_str = "DELETE FROM Vehicle WHERE VehicleID = ?;"
                cursor.execute(delete_str, (vehicle_id,))
                conn.commit()
                print("Vehicle Deleted Successfully...")
            else:
                raise VehicleNotFoundException("Invalid VehicleID...")
        except VehicleNotFoundException as e:
            print(f"Vehicle Removal Failed: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_vehicle_by_id(self):
        conn = get_connection()
        cursor = conn.cursor()
        try:
            vehicle_id = int(input("Enter VehicleID to get details: "))
            vehicle_str = "SELECT * FROM Vehicle WHERE VehicleID = ?;"
            cursor.execute(vehicle_str, (vehicle_id,))
            record = cursor.fetchone()
            if record:
                print()
                print("...............Vehicle Details for VehicleID: ", vehicle_id, "...............")
                print(record)
                print()
            else:
                raise VehicleNotFoundException("Invalid VehicleID...")
        except VehicleNotFoundException as e:
            print(f"Vehicle Not Found: {e}")
        finally:
            cursor.close()
            conn.close()

    def get_available_vehicles(self):
        conn = get_connection()
        cursor = conn.cursor()
        vehicle_str = '''
            SELECT * FROM Vehicle v 
            LEFT JOIN Reservation r ON v.VehicleID = r.VehicleID 
            WHERE r.EndDate < GETDATE() OR r.EndDate IS NULL;
        '''
        cursor.execute(vehicle_str)
        records = cursor.fetchall()
        print()
        print("...............Available Vehicles...............")
        if records:
            for i in records:
                print(i)
            print()
        else:
            print("No available vehicles found.")

    def select_vehicle(self):
        conn = get_connection()
        cursor = conn.cursor()
        select_str = 'SELECT * FROM Vehicle;'
        cursor.execute(select_str)
        records = cursor.fetchall()
        print()
        print("...............Records in Vehicle Table...............")
        if records:
            for i in records:
                print(i)
            print()
        else:
            print("No records found.")





'''
class VehicleService(IVehicleService):
    def __init__(self, vehicle_repository):
        self.vehicle_repository = vehicle_repository

    def get_vehicle_by_id(self, vehicle_id):
        return self.vehicle_repository.get_vehicle_by_id(vehicle_id)

    def get_available_vehicles(self):
        return self.vehicle_repository.get_available_vehicles()

    def add_vehicle(self, vehicle):
        return self.vehicle_repository.add_vehicle(vehicle)

    def update_vehicle(self, vehicle_id, new_vehicle_data):
        return self.vehicle_repository.update_vehicle(vehicle_id, new_vehicle_data)

    def remove_vehicle(self, vehicle_id):
        return self.vehicle_repository.remove_vehicle(vehicle_id)
'''
