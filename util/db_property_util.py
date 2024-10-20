class DBPropertyUtil:
    @staticmethod
    def get_connection_string():
        return (
            'DRIVER={ODBC Driver 18 for SQL Server};'
            'SERVER=localhost,1433;'
            'DATABASE=CarConnect;' 
            'UID=SA;'  
            'PWD=dockerStrongPwd123;' 
            'TrustServerCertificate=yes;'  
        )
