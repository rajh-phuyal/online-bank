from Database import Connector

class UserTable(Connector):
    def __init__(self) -> None:
        super().__init__()
        super().connect()

    # Search for all users in costumer table for login  
    def check_cred(self,card_number, hashed_pin):
        cmd = 'SELECT * FROM  customer'
        self.cursor.execute(cmd)
        data = self.cursor.fetchall()
        for i in range(len(data)):
            if card_number in data[i]:
                if hashed_pin in data[i]:
                    return True, data[i] # returns true and a tuple with the user data
        return False, 'to_balance' # the condition needs a tuple 

    # checks the receiver's card number and name
    def check_receiver(self, card_number):
        cmd = "SELECT * FROM customer WHERE card_number = {}".format(card_number)
        self.cursor.execute(cmd)
        p_data = self.cursor.fetchall()
        if card_number in p_data[0]:
                return True, p_data[0][1], p_data[0][0] # returns true, user_id and name of the receiver 
        else:
            return False, 'to_balance', 'to_balance' # the condition needs a tuple 

    # get the transactions of current´user
    def get_transactions(self, USER_ID):
        cmd = 'SELECT * FROM transactions WHERE user_id = {}'.format(USER_ID)
        self.cursor.execute(cmd)
        data = self.cursor.fetchall()
        return data

    #saves a transaction
    def save_transaction(self, user_id, name, amount, date, time, discription, type):
        cmd = 'INSERT INTO transactions(user_id, name, amount, date, time, discription, type) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(cmd, (user_id, name, amount, date, time, discription, type))
        self.conn.commit()

    # also saves the transaction for the receiver
    def save_receiver_transaction(self, receiver_id, name, amount, date, time, discription, type):
        cmd = 'INSERT INTO transactions(user_id, name, amount, date, time, discription, type) VALUES(%s, %s, %s, %s, %s, %s, %s)'
        self.cursor.execute(cmd, (receiver_id, name, amount, date, time, discription, type))
        self.conn.commit()

    # updates the amounts of both the sender and receiver
    def update_amounts(self, user_id, user_amount, receiver_card, plus_amount):
        cmd1 = "UPDATE customer SET balance = {} WHERE id = {}".format(user_amount, user_id)
        self.cursor.execute(cmd1)
        self.conn.commit()

        # this is to update the amount of the receiver
        cmd = "SELECT balance FROM customer WHERE card_number = {}".format(receiver_card)
        self.cursor.execute(cmd)
        p_data = self.cursor.fetchall()
        curr_amount = p_data[0][0] # taking the amount of receiver to add the received amount
        receiver_amount = curr_amount + plus_amount
        cmd2 = "UPDATE customer SET balance = {} WHERE card_number = {}".format(receiver_amount, receiver_card)
        self.cursor.execute(cmd2)
        self.conn.commit()
