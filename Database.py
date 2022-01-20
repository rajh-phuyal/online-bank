import mysql.connector

class Connector:
    def __init__(self):
        self.host = 'localhost'
        self.user = 'ONi'
        self.password = 'Trillions123'
        self.database = "User" 
        self.conn = None
        self.cursor = None

    def connect(self):
        self.conn = mysql.connector.connect(
           host = self.host,
           password = self.password, 
           user = self.user,
           database = self.database
        )
        self.cursor = self.conn.cursor()

    def close(self):
        self.conn.close()

