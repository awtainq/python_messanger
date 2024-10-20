from tkinter import *
from tkinter import messagebox
from interface import *
from database import DatabaseManager
from Messenger import Messenger

db=DatabaseManager('users.db')

class PasswordManger:
    def __init__(self):
        self.root = Tk()
        center_window(self.root, 900, 600)
        self.root.minsize(600, 250)
        self.root.configure(bg='#262626')
        self.root.title('Messenger')
        
        self.root.grid_rowconfigure(0, weight=4)
        self.root.grid_rowconfigure(6, weight=7)
        self.root.grid_columnconfigure(0, weight=3)
        self.root.grid_columnconfigure(2, weight=7)

        self.label = Label(self.root, text='Messenger', font=('Helvetica', 30), bg='#262626', fg='white')
        self.label.grid(row=0, column=0, pady=20, padx=20, sticky='nw')

        self.info_label = Label(self.root, text='Enter your username:', font=('Helvetica', 15), bg='#262626', fg='white')
        self.info_label.grid(row=1, column=1, pady=15, sticky='n')

        self.entry = Entry(self.root, font=('Helvetica', 15))
        self.entry.grid(row=2, column=1, pady=0, sticky='n')
        self.entry.focus_set()

        self.button = generate_buttton(self.root, text='Enter', command=self.check)
        self.button.grid(row=4, column=1, pady=15, sticky='n')
        
        self.password = Entry(self.root, font=('Helvetica', 15), show='*')
        self.in_button = generate_buttton(self.root, text='Sign in', command=self.in_)
        self.up_button = generate_buttton(self.root, text='Sign up', command=self.up_)
        self.back_button = generate_buttton(self.root, text='Back', command=self.back)
        
        self.root.bind("<Return>", lambda e: self.check())
    
    def check(self):
        if self.entry.get() != '':
            self.button.grid_forget()
            self.password.grid(row=3, column=1, pady=10, sticky='n')
            self.back_button.grid(row=5, column=1, sticky='n')
            self.password.focus_set()
            self.entry.config(state='readonly')
            self.info_label.config(text='Enter your password:')
            if db.check_name(self.entry.get()):
                self.root.bind("<Return>", lambda e: self.in_())
                self.in_button.grid(row=4, column=1, pady=5, sticky='n')
            else:
                self.root.bind("<Return>", lambda e: self.up_())
                self.up_button.grid(row=4, column=1, pady=5, sticky='n')
        else:
            messagebox.showerror("Error", "Empty field")
            return
    
    def in_(self):
        auth = db.sign_in(self.entry.get(), self.password.get())
        if auth is not None:
            user_id, username = auth
            self.open_messanger(user_id, username)
        else:
            messagebox.showerror("Error", "Incorrect password")
            return
        
    def up_(self):
        if len(self.password.get()) < 8:
            messagebox.showerror("Error", "Password must be at least 8 characters long")
            return
        user_id, username = db.sign_up(self.entry.get(), self.password.get())
        self.open_messanger(user_id, username)
        
    def open_messanger(self, user_id, username):
        self.root.destroy()
        Messenger(user_id, username).root.mainloop()
        
    def back(self):
        self.password.grid_forget()
        self.in_button.grid_forget()
        self.up_button.grid_forget()
        self.back_button.grid_forget()
        self.entry.config(state='normal')
        self.entry.delete(0, END)
        self.password.delete(0, END)
        self.entry.focus_set()
        self.button.grid(row=4, column=1, pady=15, sticky='n')
        self.root.bind("<Return>", lambda e: self.check())
        self.info_label.config(text='Enter your username:')
    
if __name__ == "__main__":
    PasswordManger().root.mainloop()