import pyodbc
from util.db_property_util import DBPropertyUtil
from exception.DatabaseConnectionException import DatabaseConnectionException

class DBConnUtil:
    @staticmethod
    def get_connection():
        connection_string = DBPropertyUtil.get_connection_string()
        try:
            connection = pyodbc.connect(connection_string)
            return connection
        except DatabaseConnectionException as e:
            print(f"Connection error: {e}")
            return None
