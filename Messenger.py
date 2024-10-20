from tkinter import *
from tkinter import messagebox, ttk
from tkinter.simpledialog import askstring
from database import DatabaseManager
from message_verify import check_message
from interface import *

db = DatabaseManager('users.db')

class Messenger:
    def __init__(self, user_id, username):
        self.root = Tk()
        self.user_id = user_id
        self.username = username
        self.root.title(f'{username} - Messenger')
        center_window(self.root, 900, 600)
        self.root.configure(bg='#262626')
        self.root.minsize(600, 250)
        
        self.current_chat_id = None
        self.scroll_positions = {}
        self.window_size = (self.root.winfo_width(), self.root.winfo_height())
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.left_frame = Frame(self.root, bg='#262626')
        self.left_frame.grid(row=0, column=0, sticky='ns')
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.right_frame = Frame(self.root, bg='#262626')
        self.right_frame.grid(row=0, column=1, sticky='nsew')
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.button = generate_buttton(self.left_frame, text='New Chat', command=self.newchat)
        self.button.grid(row=1, column=0, padx=15, pady=11, sticky='ws')

        self.chat_list_canvas = Canvas(self.left_frame, bg='#262626', highlightthickness=0,width=155)
        self.chat_list_canvas.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.chat_list_frame = Frame(self.chat_list_canvas, bg='#262626')
        self.chat_list_canvas.create_window((0, 0), window=self.chat_list_frame, anchor='nw')

        style = ttk.Style()
        style.theme_use('default')
        style.configure("Custom.Vertical.TScrollbar",
                        background="#404040",
                        troughcolor="#262626",
                        gripcount=0,
                        borderwidth=0,
                        padding=0,
                        relief="flat",
                        bordercolor="#262626",
                        arrowcolor="#262626")
        style.layout("Custom.Vertical.TScrollbar",
                     [('Vertical.Scrollbar.trough',
                       {'children': [('Vertical.Scrollbar.thumb', {'expand': '1', 'sticky': 'nswe'})],
                        'sticky': 'ns'})])
        style.map("Custom.Vertical.TScrollbar",
                  background=[('active', '#404040')])
                
        self.scrollbar = ttk.Scrollbar(self.left_frame, orient=VERTICAL, command=self.chat_list_canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scrollbar.grid(row=0, column=1, sticky='wns')
        self.chat_list_canvas.config(yscrollcommand=self.scrollbar.set)

        self.canvas = Canvas(self.right_frame, bg='#262626', highlightthickness=0)
        self.scroll_y = ttk.Scrollbar(self.right_frame, orient="vertical", command=self.canvas.yview, style="Custom.Vertical.TScrollbar")
        self.scroll_y.grid(row=0, column=1, sticky='ns')
        self.messages_frame = Frame(self.canvas, bg='#262626')
        self.canvas.create_window((0, 0), window=self.messages_frame, anchor='nw')
        self.canvas.config(yscrollcommand=self.scroll_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.input_frame = Frame(self.right_frame, bg='#262626')
        self.input_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = Entry(self.input_frame, bg='#262626', fg='white', insertbackground='white', bd=0, state='disabled')
        self.message_entry.grid(row=0, column=0, sticky='ew')

        self.send_button = generate_buttton(self.input_frame, text='Send', command=self.send_message)
        self.send_button.grid(row=0, column=1, columnspan=2, padx=10, sticky='es')

        self.chat_ids = []
        self.refresh_chat_list()
        
        self.root.bind('<Return>', lambda event: self.send_message())
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())
        self.chat_list_canvas.bind("<Enter>", lambda e: self._bind_mousewheel_chat_list())
        self.chat_list_canvas.bind("<Leave>", lambda e: self._unbind_mousewheel_chat_list())
        self.messages_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.chat_list_frame.bind('<Configure>', lambda e: self.chat_list_canvas.config(scrollregion=self.chat_list_canvas.bbox('all')))

    def newchat(self):
        chatname = askstring('New Chat', 'Enter chat name')
        if chatname is None:
            return
        elif chatname.strip():
            db.chat_add(chatname)
            self.refresh_chat_list()
        else:
            messagebox.showwarning('Chat Adding', 'Chat name cannot be empty')
    
    def refresh_chat_list(self):
        for widget in self.chat_list_frame.winfo_children():
            widget.destroy()
        for chat_name, chat_id in db.chat_names_get():
            is_active = False
            if self.current_chat_id == chat_id:
                is_active = True
            generate_chatname(self.chat_list_frame, chat_name, lambda cid=chat_id: self.open_chat(cid), is_active).pack(padx=3, pady=2)

    def open_chat(self, chat_id):
        self.canvas.yview_moveto(0)
        self.message_entry.config(state='normal')
        self.load_messages(chat_id)
        self.refresh_chat_list()
        self.canvas.update_idletasks()
        messages_height = sum([widget.winfo_height() for widget in self.messages_frame.winfo_children()])
        if messages_height > self.canvas.winfo_height():
            self.canvas.yview_moveto(1)
        else:
            self.canvas.yview_moveto(0) 

    def load_messages(self, chat_id):
        if self.current_chat_id == chat_id:
            self.scroll_positions[self.current_chat_id] = self.canvas.yview()
        self.current_chat_id = chat_id
        for widget in self.messages_frame.winfo_children():
            widget.destroy()

        for message_text, sender_login, message_time, message_id in db.messages_get(self.current_chat_id):
            comment_count=len(db.get_comments(message_id))
            generate_message_canvas(self.messages_frame, self.root.winfo_width()-250, sender_login, message_time[:-10], message_text,
                                    db.get_likes_count(message_id), comment_count, lambda mid=message_id: self.like_message(mid, self.user_id),
                                    lambda mid=message_id: self.comment_message(mid), db.is_liked(message_id, self.user_id)).pack(padx=10, pady=2)
            for text, user, time in db.get_comments(message_id):
                generate_comment_canvas(self.messages_frame, self.root.winfo_width()-350, f'{user}:', time[:-10], text).pack(anchor='e', padx=7, pady=0)

        self.canvas.update_idletasks()
        self.message_entry.focus_set()
        self.canvas.yview_moveto(self.scroll_positions[chat_id][0] if chat_id in self.scroll_positions else 1)

    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        
    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")

    def _bind_mousewheel_chat_list(self):
        self.chat_list_canvas.bind_all("<MouseWheel>", self._on_mousewheel_chat_list)

    def _unbind_mousewheel_chat_list(self):
        self.chat_list_canvas.unbind_all("<MouseWheel>")

    def _on_mousewheel(self, event):
        if event.delta:
            delta = event.delta
        else:
            delta = -120 if event.num == 4 else 120
        current_view = self.canvas.yview()
        if delta > 0 and current_view[0] > 0:
            self.canvas.yview_scroll(-1, "units")
        elif delta < 0 and current_view[1] < 1:
            self.canvas.yview_scroll(1, "units")

    def _on_mousewheel_chat_list(self, event):
        if event.delta:
            delta = event.delta
        else:
            delta = -120 if event.num == 5 else 120
        current_view = self.chat_list_canvas.yview()
        if delta > 0 and current_view[0] > 0:
            self.chat_list_canvas.yview_scroll(-1, "units")
        elif delta < 0 and current_view[1] < 1:
            self.chat_list_canvas.yview_scroll(1, "units")

    def comment_message(self, message_id):
        comment_text = askstring("Add Comment", "Enter your comment:")
        if comment_text:
            if check_message(comment_text):
                db.comment_message(message_id, comment_text, self.user_id)
                self.load_messages(self.current_chat_id)
            else: messagebox.showwarning("Warning",)
        else:
            messagebox.showwarning("Warning", "Comment cannot be empty")

    def send_message(self):
        message_text = self.message_entry.get()
        if message_text.strip():
            if check_message(message_text):
                db.message_add(self.current_chat_id, message_text, self.user_id)
                self.message_entry.delete(0, END)
                self.load_messages(self.current_chat_id)
                self.canvas.yview_moveto(1)
            else:
                messagebox.showwarning("Warning", "Message contains forbidden words")
        else:
            messagebox.showwarning("Warning", "Cannot send empty message")

    def like_message(self, message_id, user_id):
        db.like_message(message_id, user_id)
        self.load_messages(self.current_chat_id)
                
if __name__ == '__main__':
    Messenger(7, 'admin').root.mainloop()