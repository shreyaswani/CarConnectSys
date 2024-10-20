class Customer:
    def __init__(self, customer_id=None, first_name='', last_name='', email='',
                 phone_number='', address='', username='', password='', registration_date=''):
        self.__customer_id = customer_id
        self.__first_name = first_name
        self.__last_name = last_name
        self.__email = email
        self.__phone_number = phone_number
        self.__address = address
        self.__username = username
        self.__password = password
        self.__registration_date = registration_date


    def get_customer_id(self):
        return self.__customer_id

    def get_first_name(self):
        return self.__first_name

    def get_last_name(self):
        return self.__last_name

    def get_email(self):
        return self.__email

    def get_phone_number(self):
        return self.__phone_number

    def get_address(self):
        return self.__address

    def get_username(self):
        return self.__username

    def get_password(self):
        return self.__password

    def get_registration_date(self):
        return self.__registration_date



    def set_first_name(self, first_name):
        self.__first_name = first_name

    def set_last_name(self, last_name):
        self.__last_name = last_name

    def set_email(self, email):
        self.__email = email

    def set_phone_number(self, phone_number):
        self.__phone_number = phone_number

    def set_address(self, address):
        self.__address = address

    def set_username(self, username):
        self.__username = username

    def set_password(self, password):
        self.__password = password

    def set_registration_date(self, registration_date):
        self.__registration_date = registration_date


    def authenticate(self, password):
        return self.__password == password
