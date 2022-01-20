import tkinter as tk 
from tkinter import ttk
import os
import hashlib
from extras import *
from UserTable import UserTable

# main window
root = tk.Tk()
root.geometry('700x509')
root.title('Global Bank')
root.resizable(width=False, height=False)
root.iconbitmap('bank.ico')

def backgroung_img(img_name):
	'''displays dinamic images'''
	global bg_img
	bg_img = tk.Label(root)
	bg_img.grid(row=2, column=0, rowspan=15, columnspan=10)
	bg_img.img = tk.PhotoImage(file=img_name)
	bg_img.config(image=bg_img.img)
backgroung_img('gradient.gif')

def top_label(text, fg_color, bg_color):
	'''displays a title text'''
	global main_label
	main_label = tk.Label(root, text=text)
	main_label.grid(row=0, column=0, sticky='new', columnspan=10)
	main_label.config(font=('Ariel', 25, 'bold'), fg=fg_color, bg=bg_color)
top_label('Online banking', 'white', '#33cc00')

# style for the buttons
style = ttk.Style()
style.configure('W.TButton', font =('calibri', 15, 'bold'),foreground = 'black', background='grey')


def display_err_msg(text, _frame):
	'''displayes an error msg when using conditions'''
	error_msg = tk.Label(_frame, text=text)
	error_msg.grid(row=5, column=0, padx=2, pady=2,columnspan=6, sticky='ews')
	error_msg.config(font=('Courier', 11, 'bold'), fg='Red', bg='black')


#creating a instance of database obj
sqluser = UserTable()

class User:
	'''defined the user with all their data'''
	def __init__(self, data):
		self.dbid = data[0]
		self.card_number = data[2]
		self.hashed_pin = data[3]
		self.name = data[1]
		self.amount = data[4]
		self.phone = data[5]
		self.address = data[6]

# login function
def login_user():
	# username and password (labels)
	login_frame = tk.LabelFrame(root, text='login', fg='white', bg='green', padx=6, pady=6)
	login_frame.grid(row=3, column=2, pady=60, columnspan=6)

	card_number_frame = tk.LabelFrame(login_frame, text='Enter the card number', padx=2, pady=2, fg='white', bg='black')
	card_number_frame.grid(row=0, column=0, pady=5, columnspan=3)

	card_number_entry = tk.Entry(card_number_frame, width=30)
	card_number_entry.config(font=('Ariel', 12))
	card_number_entry.grid(row=0, column=0, ipadx=5, ipady=4)

	pin_frame =  tk.LabelFrame(login_frame, text='Enter the pin', padx=3, pady=2, fg='white', bg='black')
	pin_frame.grid(row=1, column=0, columnspan=3, pady=5)

	pin_entry = tk.Entry(pin_frame, width=30, fg='green')
	pin_entry.config(show='*', font=(20))
	pin_entry.grid(row=0, column=0, ipadx=5, ipady=6)

	def check_credentials(card_number, pin):
		'''this function checks the entered card number and pin'''
		global current_user # creating a user object to store needed data
		if card_number != '' and pin != '':
			if len(card_number) == 16:
				hashed_pin = hashlib.sha256(pin.encode('utf-8')).hexdigest() # the 4 digit pin is hashed and stored 
				_data = sqluser.check_cred(card_number, hashed_pin) # this checks the cardnumber and pin from the database
				if _data[0]: # a tuple is retuned
					login_frame.grid_forget()
					backgroung_img('grey.gif')
					current_user = User(_data[1])
					options()
				else:
					display_err_msg('Incorrect Username or password!', login_frame)
			else:
				display_err_msg('Incorrect Username or password!', login_frame)
		else:
			display_err_msg('Fields cannot be empty!', login_frame)

	s_button = ttk.Button(login_frame, text='SUBMIT', style='W.TButton', command=lambda:check_credentials(card_number_entry.get(), pin_entry.get()))
	s_button.grid(row=4, column=1, padx=2)


def options():
	'''this function is for after the login, provides 3 functions with buttons at the top'''
	backgroung_img('grey.gif')
	top_label('User Account', 'white', '#2A8000')

	def redirect(func_name):
		if func_name == 'info':
			acc_info()
		if func_name == 'transfer':
			transfer()
		if func_name == 'trans_his':
			transaction_history()
	
	# frame that holds the buttons
	global choose_options_frame
	choose_options_frame = tk.LabelFrame(root, fg='white', bg='#b30000', padx=3, pady=2)
	choose_options_frame.grid(row=2, column=1, pady=5, padx=12, columnspan=8)

	b1 = ttk.Button(choose_options_frame, text='Acc Info', style = 'W.TButton', command=lambda:redirect('info'))
	b2 = ttk.Button(choose_options_frame, text='Transfer', style = 'W.TButton', command=lambda:redirect('transfer'))
	b3 = ttk.Button(choose_options_frame, text='History', style = 'W.TButton', command=lambda:redirect('trans_his'))

	b1.grid(row=0, column=0, padx=5)
	b2.grid(row=0, column=1, padx=10)
	b3.grid(row=0, column=2, pady=5)

	global welcome_frame
	welcome_frame = tk.LabelFrame(root, bg='white', padx=3, pady=2, width=50)
	welcome_frame.grid(row=4, column=1, columnspan=8)

	welcome_label = tk.Label(welcome_frame, text='Welcome back , ' + current_user.name)
	welcome_label.grid(row=0, column=0, columnspan=8)
	welcome_label.config(font=('Ariel', 25, 'bold'), fg='black', bg='white')

def clear_frames():
	'''clears the frames when another function is called'''
	try:
		info_frame.grid_forget()
	except NameError:
		pass
	try:
		transfer_frame.grid_forget()
	except NameError:
		pass
	try:
		transaction_frame.grid_forget()
	except NameError:
		pass
	try:
		welcome_frame.grid_forget()
	except NameError:
		pass
	try:
		proceed_frame.grid_forget()
	except NameError:
		pass

def acc_info():
	''' this function displays the bank and personal info of the current loged in user'''
	global info_frame
	clear_frames()

	info_frame = tk.LabelFrame(root, text='Account info', padx=2, pady=2, fg='black', bg='grey')
	info_frame.grid(row=3, column=2, pady=5, columnspan=6)

	bank_info_frame = tk.LabelFrame(info_frame, text='Bank Info', fg='white', bg='black', padx=5, pady=5, width=50)
	bank_info_frame.grid(row=0, column=0, pady=5, columnspan=6)

	acc_balance_label = tk.Label(bank_info_frame, text='Account balance : ' + '€' + str(current_user.amount) , fg='#1aff1a', bg='black')
	acc_balance_label.grid(row=0, column=0, pady=10, sticky='ew')
	acc_balance_label.config(font=('Ariel', 17, 'bold'))

	personal_info_frame = tk.LabelFrame(info_frame, text='Personal Info', fg='white', bg='black', padx=5, pady=5, width=50)
	personal_info_frame.grid(row=1, column=0, pady=5, columnspan=6)

	name_label = tk.Label(personal_info_frame, text=current_user.name, fg='white', bg='black')
	name_label.grid(row=0, column=0, pady=10, sticky='ew')
	name_label.config(font=('Ariel', 15, 'bold'))

	phone_label = tk.Label(personal_info_frame, text='Phone : ' + current_user.phone, fg='white', bg='black')
	phone_label.grid(row=1, column=0, pady=10, sticky='ew')
	phone_label.config(font=('Ariel', 15, 'bold'))

	address_label = tk.Label(personal_info_frame, text='Address : ' + current_user.address, fg='white', bg='black')
	address_label.grid(row=2, column=0, pady=10, sticky='ew')
	address_label.config(font=('Ariel', 10, 'bold'))

def proceed(receiver_id, name, acc_number, amount, discription, pin):
	''' this function displays the data entered in the transfer section to continue'''
	global proceed_frame
	clear_frames()

	proceed_frame = tk.LabelFrame(root, text='PROCEED', fg='white', bg='black', padx=12, pady=12)
	proceed_frame.grid(row=3, column=2, columnspan=6)

	name_frame = tk.LabelFrame(proceed_frame, text='To', fg='white', bg='black')
	name_frame.grid(row=0, column=0)

	name_label = tk.Label(name_frame, text=name)
	name_label.grid(row=0, column=0)
	name_label.config(font=('Ariel', 20))

	card_frame = tk.LabelFrame(proceed_frame, text='Card number', fg='white', bg='black')
	card_frame.grid(row=1, column=0)

	card_label = tk.Label(card_frame, text=acc_number)
	card_label.grid(row=0, column=0)
	card_label.config(font=('Ariel', 15))

	amount_frame = tk.LabelFrame(proceed_frame, text='Amount €', fg='white', bg='black')
	amount_frame.grid(row=2, column=0)

	amount_label = tk.Label(amount_frame, text=amount)
	amount_label.grid(row=0, column=0, sticky='ew')
	amount_label.config(font=('Ariel', 15))

	description_frame = tk.LabelFrame(proceed_frame, text='Description', fg='white', bg='black')
	description_frame.grid(row=3, column=0, pady=5)

	description_field = tk.Text(description_frame,  width=30, height=3)
	description_field.grid(row=0, column=0)
	description_field.insert(1.0, discription)
	description_field.config(state='disabled')
	description_field.config(font=('Ariel', 15))

	def proceeded():
		# this is to save the transaction with everything correct
		x = datetime.datetime.now()
		date = f'{x.day}-{x.month}-{x.year}'
		time = f'{x.strftime("%H")}:{x.strftime("%M")}'
		sqluser.save_transaction(current_user.dbid, name, amount, date, time, discription, 'sent')
		sqluser.save_receiver_transaction(receiver_id, current_user.name, amount, date, time, discription, 'received')

		# this is to update the amount of both the parties
		user_amount = current_user.amount - amount
		sqluser.update_amounts(current_user.dbid, user_amount, acc_number, amount)
		current_user.amount = user_amount
		clear_frames()
		mini_window('Transfer Successful', 'green', 'black')

	next_button = ttk.Button(proceed_frame, text='PROCEED', style = 'W.TButton',
	 command=proceeded).grid(row=4, column=0, pady=5)
	next_button = ttk.Button(proceed_frame, text='BACK', style = 'W.TButton',
	 command=transfer).grid(row=5, column=0)

def transfer():
	'''this function is for transfer of balance from a person to another but not yet completed'''
	global transfer_frame
	clear_frames()

	transfer_frame = tk.LabelFrame(root, text='Transfer', fg='white', bg='black', padx=12, pady=12)
	transfer_frame.grid(row=3, column=2, columnspan=6)

	card_frame = tk.LabelFrame(transfer_frame, text='Card number', fg='white', bg='black')
	card_frame.grid(row=0, column=0)

	card_entry = tk.Entry(card_frame, width=30)
	card_entry.grid(row=0, column=0, ipady=5)
	card_entry.config(font=('Ariel', 12))

	amount_frame = tk.LabelFrame(transfer_frame, text='Amount €', fg='white', bg='black')
	amount_frame.grid(row=1, column=0)

	amount_entry = tk.Entry(amount_frame, width=30)
	amount_entry.grid(row=0, column=0, ipady=4, pady=5)
	amount_entry.config(font=('Ariel', 12))

	description_frame = tk.LabelFrame(transfer_frame, text='Description', fg='white', bg='black')
	description_frame.grid(row=2, column=0, pady=5)

	description_entry = tk.Text(description_frame, width=30, height=3)
	description_entry.grid(row=0, column=0)
	description_entry.config(font=('Ariel', 12))

	pin_frame = tk.LabelFrame(transfer_frame, text='Pin', fg='white', bg='black')
	pin_frame.grid(row=3, column=0)

	pin_entry = tk.Entry(pin_frame, width=20, fg='blue')
	pin_entry.grid(row=0, column=0, ipady=4, pady=3)
	pin_entry.config(font=('Ariel', 12), show='*')

	def check_entries(acc_number, amount, discription, pin): 
		# to check if the entered fields are correct
		print(discription)
		if discription != '' and acc_number != '' and amount != '' and pin != '':
				if acc_number.isdigit() and acc_number != current_user.card_number and len(acc_number) == 16: 
					check = sqluser.check_receiver(acc_number) # checks the receivers account
					if check[0]: # returns a tuple
						if amount.isdigit():
							amount = float(amount)
							if amount < float(current_user.amount) and  2000 >= amount >= 10 : # limiting the transfer amount
								_pin = hashlib.sha256(pin.encode()).hexdigest()
								if _pin == current_user.hashed_pin:
									clear_frames()
									proceed(check[2], check[1], acc_number, amount, discription, pin)
								else:
									display_err_msg('Incorrect pin!', transfer_frame)
							else:
								display_err_msg('Amount not permitted!', transfer_frame)
						else:
							display_err_msg('Invalid Amount!', transfer_frame)
					else:
						display_err_msg("Incorrect receiver's info ", transfer_frame)
				else:
					display_err_msg('Invalid card number!', transfer_frame)
		else:			
			display_err_msg('Fields cannot be empty!', transfer_frame)

	next_button = ttk.Button(transfer_frame, text='NEXT', style = 'W.TButton',
	 command= lambda:check_entries(card_entry.get(),amount_entry.get(),description_entry.get(1.0, 'end'), pin_entry.get()))
	next_button.grid(row=4, column=0, pady=7)

def transaction_history():
	'''it displayes the 15 most recent transactions'''
	global transaction_frame
	clear_frames()
	transaction_frame = tk.LabelFrame(root, fg='black', bg='grey', width=62, height=17)
	transaction_frame.grid(row=3, column=0, sticky='ews', padx=2, columnspan=10)

	data = sqluser.get_transactions(current_user.dbid)
	text = conv_to_str(reverse_list(data)) # imports from extras, reverses the list and make it in string format

	txtbox = tk.Text(transaction_frame, width=62, height=17)
	txtbox.grid(row=0, column=5, pady=2, padx=2)
	txtbox.config(font=('Ariel', 14, 'bold'), fg='#ccff33', bg='#000000')

	ll = '_'  # autoseperator in text widget is broken so using a line
	_index = 1.0
	for line in text:
		# enters the texts
		txtbox.insert(_index, line + '\n')
		_index += 1
		# than inserts a line in the text wiged
		txtbox.insert(_index, ll*62 + '\n')
		_index += 1
	txtbox.config(state='disabled')

def logout():
	'''this func logs out of the user account'''
	clear_frames()
	try:
		choose_options_frame.grid_forget()
	except NameError:
		pass
	backgroung_img('gradient.gif')
	top_label('Online banking', 'white', '#33cc00')
	login_user()

# creating a menu bar 
main_menubar = tk.Menu(root)
root.config(menu=main_menubar)

# have options
option_menu = tk.Menu(main_menubar, tearoff=0)
main_menubar.add_cascade(label='Option', menu=option_menu)

option_menu.add_command(label='Log-out', command=logout)

option_menu.add_command(label='Exit', command=root.quit)

login_user() # always starts with the login


root.mainloop()
