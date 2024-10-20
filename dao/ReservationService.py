from datetime import datetime
from entity.IReservationService import IReservationService
from entity.Reservation import Reservation
from util.db_conn_util import get_connection
from exception.ReservationException import ReservationException
from exception.InvalidInputException import InvalidInputException

class ReservationService(IReservationService):
    def __init__(self):
        super().__init__()

    def is_vehicle_reserved(self, vehicle_id, start_date):
        
        select_query = "SELECT TOP 1 * FROM Reservation WHERE VehicleID = ? AND EndDate > ? ORDER BY EndDate DESC;"
        conn = get_connection()
        cursor = conn.cursor()
        cursor.execute(select_query, (vehicle_id, start_date))
        result = cursor.fetchall()
        conn.close()
        return bool(result)

    def authenticate_id(self, id):
        if id.isdigit():
            return True
        else:
            raise InvalidInputException("Enter Correct Id...")

    def create_reservation(self):
        try:
            reservation = Reservation()
            try:
                customer_id = input("Enter customerID: ")
                if self.authenticate_id(customer_id):
                    reservation.set_customer_id(customer_id)
            except InvalidInputException as e:
                print(f'Invalid Input: {e}')
            try:
                vehicle_id = input("Enter VehicleID: ")
                if self.authenticate_id(vehicle_id):
                    reservation.set_vehicle_id(vehicle_id)
            except InvalidInputException as e:
                print(f'Invalid Input: {e}')
            start_date_str = input("Enter Start Date {YYYY-MM-DD}: ")
            end_date_str = input("Enter End Date {YYYY-MM-DD}: ")

            start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
            if end_date < start_date:
                raise ValueError("End date cannot be earlier than the start date.")
            reservation.set_start_date(start_date)
            reservation.set_end_date(end_date)
            status = input("Enter Status ('pending', 'confirmed', 'completed'): ").lower()

            if status not in ('pending', 'confirmed', 'completed'):
                raise InvalidInputException("Status must be 'pending', 'confirmed', or 'completed'.")
            reservation.set_status(status)

            conn = get_connection()
            cursor = conn.cursor()
            daily_query = "SELECT DailyRate FROM Vehicle WHERE VehicleID = ?;"
            cursor.execute(daily_query, (reservation.get_vehicle_id(),))
            daily_rate = cursor.fetchone()[0]
            reservation.set_daily_rate(daily_rate)
            total_cost = float(reservation.calculate_total_cost())

            if self.is_vehicle_reserved(reservation.get_vehicle_id(), reservation.get_start_date()):
                raise ReservationException("Vehicle is already reserved")

            insert_query = '''
                INSERT INTO Reservation (CustomerID, VehicleID, StartDate, EndDate, TotalCost, Status)
                VALUES (?, ?, ?, ?, ?, ?);
            '''
            cursor.execute(insert_query, (
                reservation.get_customer_id(),
                reservation.get_vehicle_id(),
                reservation.get_start_date(),
                reservation.get_end_date(),
                total_cost,
                reservation.get_status()
            ))
            conn.commit()
            print("Reservation created successfully..")
            conn.close()
        except ReservationException as e:
            print(f"Reservation Failed: {e}")

    def update_reservation(self):
        try:
            self.select_reservation()
            reservation_id = int(input("Enter ReservationID to be updated: "))
            query = "SELECT ReservationID FROM Reservation WHERE ReservationID = ?"
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (reservation_id,))
            record = cursor.fetchone()
            if record:
                reservation = Reservation()
                try:
                    customer_id = input("Enter customerID: ")
                    if self.authenticate_id(customer_id):
                        reservation.set_customer_id(customer_id)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return
                try:
                    vehicle_id = input("Enter VehicleID: ")
                    if self.authenticate_id(vehicle_id):
                        reservation.set_vehicle_id(vehicle_id)
                except InvalidInputException as e:
                    print(f'Invalid Input: {e}')
                    return

                start_date_str = input("Enter Start Date {YYYY-MM-DD}: ")
                end_date_str = input("Enter End Date {YYYY-MM-DD}: ")
                start_date = datetime.strptime(start_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                end_date = datetime.strptime(end_date_str, '%Y-%m-%d').strftime('%Y-%m-%d')
                reservation.set_start_date(start_date)
                reservation.set_end_date(end_date)
                reservation.set_status(input("Enter Status ('pending', 'confirmed', 'completed'): "))

                daily_query = "SELECT DailyRate FROM Vehicle WHERE VehicleID = ?;"
                cursor.execute(daily_query, (reservation.get_vehicle_id(),))
                daily_rate = cursor.fetchone()[0]
                reservation.set_daily_rate(daily_rate)
                total_cost = float(reservation.calculate_total_cost())

                update_str = '''
                    UPDATE Reservation SET CustomerID = ?, VehicleID = ?, StartDate = ?, EndDate = ?, TotalCost = ?, Status = ?
                    WHERE ReservationID = ?;
                '''
                cursor.execute(update_str, (
                    reservation.get_customer_id(),
                    reservation.get_vehicle_id(),
                    reservation.get_start_date(),
                    reservation.get_end_date(),
                    total_cost,
                    reservation.get_status(),
                    reservation_id
                ))
                conn.commit()
                print("Reservation Updated Successfully...")
                conn.close()
            else:
                raise ReservationException("Invalid ReservationID...")
        except ReservationException as e:
            print(f"Reservation Update Failed: {e}")

    def cancel_reservation(self):
        try:
            reservation_id = int(input("Enter ReservationID to be canceled: "))
            query = "SELECT ReservationID FROM Reservation WHERE ReservationID = ?"
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (reservation_id,))
            record = cursor.fetchone()
            if record:
                delete_str = "DELETE FROM Reservation WHERE ReservationID = ?;"
                cursor.execute(delete_str, (reservation_id,))
                conn.commit()
                print("Reservation Canceled Successfully...")
                conn.close()
            else:
                raise ReservationException("Invalid ReservationID...")
        except ReservationException as e:
            print(f"Reservation Cancellation Failed: {e}")

    def get_reservation_by_id(self):
        try:
            reservation_id = int(input("Enter ReservationID to get details: "))
            query = "SELECT ReservationID FROM Reservation WHERE ReservationID = ?;"
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (reservation_id,))
            record = cursor.fetchone()
            if record:
                reservation_str = "SELECT * FROM Reservation WHERE ReservationID = ?;"
                cursor.execute(reservation_str, (reservation_id,))
                records = cursor.fetchall()
                print()
                print("...............Reservation Details for ReservationID: ", reservation_id, "...............")
                for i in records:
                    print(i)
                print()
                conn.commit()
                conn.close()
            else:
                raise ReservationException("Invalid ReservationID...")
        except ReservationException as e:
            print(f"Reservation Exception: {e}")

    def get_reservations_by_customer_id(self):
        try:
            customer_id = int(input("Enter customerID to get reservations: "))
            query = "SELECT CustomerID FROM Reservation WHERE CustomerID = ?;"
            conn = get_connection()
            cursor = conn.cursor()
            cursor.execute(query, (customer_id,))
            record = cursor.fetchall()
            if record:
                reservation_str = "SELECT * FROM Reservation WHERE CustomerID = ?;"
                cursor.execute(reservation_str, (customer_id,))
                records = cursor.fetchall()
                print()
                print("...............Reservations for customerID:", customer_id, "...............")
                for i in records:
                    print(i)
                print()
                conn.commit()
                conn.close()
            else:
                raise ReservationException("Invalid customerID...")
        except ReservationException as e:
            print(f"Reservation Exception: {e}")

    def select_reservation(self):
        conn = get_connection()
        cursor = conn.cursor()
        select_str = 'SELECT * FROM Reservation;'
        cursor.execute(select_str)
        records = cursor.fetchall()
        print()
        print("...............Records in Reservation Table...............")
        for i in records:
            print(i)
        print()
        conn.close()

