
# just to create a user object to hold the data
class User:
	def __init__(self):
		self.dbid = None
		self.card_number = None
		self.hashed_pin = None
		self.name = None
		self.amount = None
		self.phone = None
		self.address = None

	def assign_data(self, data):
		self.dbid = data[0]
		self.card_number = data[2]
		self.hashed_pin = data[3]
		self.name = data[1]
		self.amount = data[4]
		self.phone = data[5]
		self.address = data[6]





		
