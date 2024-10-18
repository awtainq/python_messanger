from tkinter import *
from tkinter import messagebox
from tkinter.simpledialog import askstring
import datetime
from database import DatabaseManager
from message_verify import check_message
import json
from messages import generate_message_canvas, generate_comment_canvas, generate_buttton

db = DatabaseManager('users.db')


class Messenger:
    def __init__(self, root, user_id, username):
        self.root = root
        self.user_id = user_id
        self.username = username
        self.root.title(f'{username} - Messenger')
        self.center_window(900, 600)
        self.root.configure(bg='#262626')

        self.current_chat_id = None
        self.scroll_positions = {}
        
        self.root.grid_rowconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)

        self.left_frame = Frame(root, bg='#262626')
        self.left_frame.grid(row=0, column=0, sticky='ns')
        self.left_frame.grid_rowconfigure(0, weight=1)
        self.left_frame.grid_columnconfigure(0, weight=1)

        self.right_frame = Frame(root, bg='#262626')
        self.right_frame.grid(row=0, column=1, sticky='nsew')
        self.right_frame.grid_rowconfigure(0, weight=1)
        self.right_frame.grid_columnconfigure(0, weight=1)

        self.button = generate_buttton(self.left_frame, text='New Chat', command=self.newchat)
        self.button.grid(row=1, column=0, padx=10, pady=10)

        self.root.bind('<Return>', lambda event: self.send_message())

        self.chat_listbox = Listbox(self.left_frame, bg='#262626', fg='white', selectbackground='#333333', highlightbackground='#262626', bd=0)
        self.chat_listbox.grid(row=0, column=0, sticky='nsew', padx=10, pady=10)

        self.scrollbar = Scrollbar(self.left_frame, orient=VERTICAL, bg='#262626')
        self.scrollbar.config(command=self.chat_listbox.yview)
        self.chat_listbox.config(yscrollcommand=self.scrollbar.set)
        self.scrollbar.grid(row=0, column=1, sticky='ns')

        self.chat_listbox.bind('<<ListboxSelect>>', self.open_chat)

        self.canvas = Canvas(self.right_frame, bg='#262626')
        self.scroll_y = Scrollbar(self.right_frame, orient="vertical", command=self.canvas.yview, bg='#262626')
        self.scroll_y.grid(row=0, column=1, sticky='ns')
    
        self.messages_frame = Frame(self.canvas, bg='#262626')
        self.canvas.create_window((0, 0), window=self.messages_frame, anchor='nw')
        self.canvas.config(yscrollcommand=self.scroll_y.set)
        self.canvas.grid(row=0, column=0, sticky="nsew")

        self.input_frame = Frame(self.right_frame, bg='#262626')
        self.input_frame.grid(row=1, column=0, sticky='ew', padx=10, pady=10)
        self.input_frame.grid_columnconfigure(0, weight=1)

        self.message_entry = Entry(self.input_frame, bg='#262626', fg='white', insertbackground='white', bd=0)
        self.message_entry.grid(row=0, column=0, sticky='ew')

        self.send_button = generate_buttton(self.input_frame, text='Send', command=self.send_message)
        self.send_button.grid(row=0, column=1, columnspan=2, padx=10, sticky='e')

        self.message_entry.config(state='normal')
        self.send_button.config(state='normal')

        self.chat_ids = []

        self.refresh_chat_list()

        self.messages_frame.bind("<Configure>", lambda e: self.canvas.configure(scrollregion=self.canvas.bbox("all")))
        self.canvas.bind("<Enter>", lambda e: self._bind_mousewheel())
        self.canvas.bind("<Leave>", lambda e: self._unbind_mousewheel())

    def center_window(self, width, height):
        screen_width = self.root.winfo_screenwidth()
        screen_height = self.root.winfo_screenheight()
        x = (screen_width // 2) - (width // 2)
        y = (screen_height // 2) - (height // 2)
        self.root.geometry(f'{width}x{height}+{x}+{y}')

    def newchat(self):
        chatname = askstring('New Chat', 'Enter chat name')
        if chatname:
            db.cursor.execute("INSERT INTO Chats (name) VALUES (?)", (chatname,))
            db.commit()
            messagebox.showinfo('Chat Adding', 'Success')
            self.refresh_chat_list()
        else:
            messagebox.showwarning('Chat Adding', 'Chat name cannot be empty')

    def refresh_chat_list(self):
        self.chat_listbox.delete(0, END)
        self.chat_ids = []
        chat_names = db.cursor.execute("SELECT name, id FROM Chats").fetchall()
        for chat_name, chat_id in chat_names:
            self.chat_listbox.insert(END, chat_name)
            self.chat_ids.append(chat_id)

    def open_chat(self, event):
        selection = self.chat_listbox.curselection()
        if selection:
            index = selection[0]
            self.current_chat_id = self.chat_ids[index]
            self.load_messages(self.current_chat_id)
            self.message_entry.config(state='normal')
            self.send_button.config(state='normal')
            self.root.after(100, self.message_entry.focus_set)
        else:
            self.current_chat_id = None
            for widget in self.messages_frame.winfo_children():
                widget.destroy()
            self.message_entry.config(state='disabled')
            self.send_button.config(state='disabled')

    def load_messages(self, chat_id):
        if self.current_chat_id is not None:
            self.scroll_positions[self.current_chat_id] = self.canvas.yview()

        for widget in self.messages_frame.winfo_children():
            widget.destroy()
        messages = db.cursor.execute("""
            SELECT Messages.message, Users.login, Messages.time, Messages.id
            FROM Messages 
            JOIN Users ON Messages.user_id = Users.user_id 
            WHERE Messages.chat_id = ? 
            ORDER BY Messages.time
        """, (self.current_chat_id,)).fetchall()

        for message_text, sender_login, message_time, message_id in messages:
            comment_count=len(self.get_comments(message_id))
            generate_message_canvas(self.messages_frame, self.root.winfo_width()-250, sender_login, message_time[:-10], message_text, self.get_likes_count(message_id), comment_count, lambda mid=message_id: self.like_message(mid, self.user_id), lambda mid=message_id: self.comment_message(mid)).pack(padx=3, pady=2)
            for comment in self.get_comments(message_id):
                generate_comment_canvas(self.messages_frame, self.root.winfo_width()-350, f'{comment['user']}:', comment['time'][:-10], comment['text']).pack(anchor='e', padx=3, pady=2)

        self.canvas.update_idletasks()
        self.message_entry.focus_set()

        bbox = self.canvas.bbox("all")
        if chat_id in self.scroll_positions:
            self.canvas.yview_moveto(self.scroll_positions[chat_id][0])
        else:
            self.scroll_to_bottom()

    def scroll_to_bottom(self):
        bbox = self.canvas.bbox('all')
        if bbox:
            canvas_height = self.canvas.winfo_height()
            content_height = bbox[3] - bbox[1]
            if content_height > canvas_height:
                self.canvas.yview_moveto(1)
            else:
                self.canvas.yview_moveto(0)



    def _bind_mousewheel(self):
        self.canvas.bind_all("<MouseWheel>", self._on_mousewheel)
        self.canvas.bind_all("<Button-4>", self._on_mousewheel)
        self.canvas.bind_all("<Button-5>", self._on_mousewheel)

    def _unbind_mousewheel(self):
        self.canvas.unbind_all("<MouseWheel>")
        self.canvas.unbind_all("<Button-4>")
        self.canvas.unbind_all("<Button-5>")

    def _on_mousewheel(self, event):
        if event.delta:
            delta = event.delta
        else:
            delta = -120 if event.num == 5 else 120
        current_view = self.canvas.yview()
        if delta > 0 and current_view[0] > 0: 
            self.canvas.yview_scroll(-1, "units")
        elif delta < 0 and current_view[1] < 1:
            self.canvas.yview_scroll(1, "units")

    def like_message(self, message_id, user_id):
        db.cursor.execute("SELECT likes FROM Messages WHERE id = ?", (message_id,))
        result = db.cursor.fetchone()

        likes = json.loads(result[0]) if result[0] else []
        if user_id in likes:
            likes.remove(user_id)
        else:
            likes.append(user_id)
        db.cursor.execute("UPDATE Messages SET likes = ? WHERE id = ?", (json.dumps(likes), message_id))
        db.commit()
        self.load_messages(self.current_chat_id)

    def get_likes_count(self, message_id):
        db.cursor.execute("SELECT likes FROM Messages WHERE id = ?", (message_id,))
        result = db.cursor.fetchone()
        if result is None:
            return 0
        likes = json.loads(result[0]) if result[0] else []
        return len(likes)

    def get_comments(self, message_id):
        comments = db.cursor.execute("""
            SELECT Comments.comment, Users.login, Comments.time
            FROM Comments 
            JOIN Users ON Comments.user_id = Users.user_id 
            WHERE Comments.message_id = ? 
            ORDER BY Comments.time
        """, (message_id,)).fetchall()
        return [{'text': comment_text, 'user': user_login, 'time': comment_time} for comment_text, user_login, comment_time in comments]

    def comment_message(self, message_id):
        comment_text = askstring("Add Comment", "Enter your comment:")
        if comment_text:
            if check_message(comment_text):
                current_time = datetime.datetime.now()
                db.cursor.execute("INSERT INTO Comments (message_id, comment, user_id, time) VALUES (?, ?, ?, ?)",
                                (message_id, comment_text, self.user_id, current_time))
                db.commit()
                messagebox.showinfo("Comment", "Comment added successfully")
                self.load_messages(self.current_chat_id)
            else: messagebox.showwarning("Warning",)
        else:
            messagebox.showwarning("Warning", "Comment cannot be empty")

    def send_message(self):
        message_text = self.message_entry.get()
        if message_text.strip():
            if check_message(message_text):
                current_time = datetime.datetime.now()
                db.cursor.execute("INSERT INTO Messages (chat_id, message, user_id, time) VALUES (?, ?, ?, ?)",
                            (self.current_chat_id, message_text, self.user_id, current_time))
                db.commit()
                self.message_entry.delete(0, END)
                self.load_messages(self.current_chat_id)
            else:
                messagebox.showwarning("Warning", "Message contains forbidden words")
        else:
            messagebox.showwarning("Warning", "Cannot send empty message")

if __name__ == '__main__':
    root = Tk()

    Messenger(root, 1, 'admin')
    root.mainloop()