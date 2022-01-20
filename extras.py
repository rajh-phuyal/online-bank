import datetime
import tkinter as tk
from tkinter import ttk

# creats a mini window
def mini_window(text, fg_color, bg_color):
	mini = tk.Tk()
	mini.geometry('210x90')
	mini.title('Bank of 10D')
	mini.resizable(width=False, height=False)
	mini.iconbitmap('images/bank.ico')
	mini.config(bg='black')

	text_label = tk.Label(mini, text=text)
	text_label.grid(row=0, column=0, sticky='new', columnspan=3, padx=6, pady=3)
	text_label.config(font=('Ariel', 15, 'bold'), fg=fg_color, bg=bg_color)

	def func_quit():
		mini.destroy()

	ok_button = ttk.Button(mini, text='OK', style = 'W.TButton', command=func_quit)
	ok_button.grid(row=1, column=1, padx=6, pady=3)

	mini.mainloop()

# reverses the list given from transaction to display the most recent at the top
def reverse_list(data):
		rev_list = []
		_rev = -1
		try:
			while _rev < len(data):
				rev_list.append(data[_rev])
				_rev -= 1
		except IndexError:
			pass
		return rev_list

# makes the list in a string format to enter in the textbox
def conv_to_str(data):
	final_list = []
	_increment = 1
	space = ' '
	send_space = space*18
	receive_space = space*15
	for line in data:
		if _increment <= 15: # to only display 15 recent transactions
			try:
				_type = line[7].strip('\n')
				if _type == 'received':
					correct_space = receive_space
				else:
					correct_space = send_space
				text = f"{space*15} {_increment}  |  {_type}  |  {line[4]}  |  {line[5]}  |  {line[2]} |  €{line[3]} | {correct_space}Discription : {line[6]}"
				final_list.append(text)
				_increment += 1
			except IndexError:
				pass
	return final_list