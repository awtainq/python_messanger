import tkinter as tk
from database import DatabaseManager


db=DatabaseManager('users.db')

def create_rounded_rectangle(canvas, x1, y1, x2, y2, radius=25, **kwargs):
    points = [
        x1 + radius, y1,
        x1 + radius, y1,
        x2 - radius, y1,
        x2 - radius, y1,
        x2, y1,
        x2, y1 + radius,
        x2, y1 + radius,
        x2, y2 - radius,
        x2, y2 - radius,
        x2, y2,
        x2 - radius, y2,
        x2 - radius, y2,
        x1 + radius, y2,
        x1 + radius, y2,
        x1, y2,
        x1, y2 - radius,
        x1, y2 - radius,
        x1, y1 + radius,
        x1, y1 + radius,
        x1, y1,
    ]
    return canvas.create_polygon(points, **kwargs, smooth=True)

def create_custom_button(canvas, x, y, width, height, text, command, color):
    button = tk.Canvas(canvas, width=width, height=height, bg='#404040', highlightthickness=0)
    create_rounded_rectangle(button, 0, 0, width, height, radius=15, fill=color, outline=color)
    button.create_text(width//2, height//2, text=text, font=("Helvetica", 12, "bold"), fill='white')
    button.bind("<Button-1>", lambda e: command())
    canvas.create_window(x, y, anchor='nw', window=button)
    return button

def generate_message_canvas(root, width, sender, time, text, likes, comments, like_command, comment_command, is_like):
    width+=25
    temp_root = tk.Toplevel(root)
    temp_root.withdraw()
    temp_canvas = tk.Canvas(temp_root, width=width)
    temp_text_label = tk.Label(temp_canvas, text=text, font=("Helvetica", 13), wraplength=width - 170, justify='left')
    temp_text_label.update_idletasks()
    text_height = temp_text_label.winfo_reqheight()

    height = max(text_height+35, 75)

    canvas = tk.Canvas(root, width=width, height=height, bg='#262626',highlightthickness=0)
    
    create_rounded_rectangle(canvas, 5, 5, width, height, radius=20, fill='#404040', outline='#404040')

    sender_label = tk.Label(canvas, text=sender, font=("Helvetica", 13, "bold"), bg='#404040', fg='white')
    canvas.create_window(15, 10, anchor='nw', window=sender_label)

    time_label = tk.Label(canvas, text=time, font=("Helvetica", 11), bg='#404040', fg='white')
    canvas.create_window(width - 10, 10, anchor='ne', window=time_label)

    text_label = tk.Label(canvas, text=text, font=("Helvetica", 13), bg='#404040', wraplength=width - 170, justify='left', fg='white')
    canvas.create_window(15, 30, anchor='nw', window=text_label)

    like_color = '#99b3e6' if is_like else '#262626'
    create_custom_button(canvas, width-75-10-66, height - 37, 60, 30, f'♥️ {likes}', command=like_command, color=like_color)

    create_custom_button(canvas, width - 75, height - 37, 60, 30, f'💬 {comments}', command=comment_command, color='#262626')

    temp_root.destroy() 

    return canvas

def generate_comment_canvas(root, width, sender, time, text):
    temp_root = tk.Toplevel(root)
    temp_root.withdraw()  

    temp_canvas = tk.Canvas(temp_root, width=width, bg='#262626')
    temp_text_label = tk.Label(temp_canvas, text=text, font=("Helvetica", 13), wraplength=width - 20, justify='left')
    temp_text_label.update_idletasks()
    text_height = temp_text_label.winfo_reqheight()

    height = max(text_height+35, 60)

    canvas = tk.Canvas(root, width=width, height=height, bg='#262626', highlightthickness=0)
    
    create_rounded_rectangle(canvas, 5, 5, width-5, height-5, radius=20, fill='#404040', outline='#404040')

    sender_label = tk.Label(canvas, text=sender, font=("Helvetica", 13, "bold"), bg='#404040', fg='white')
    canvas.create_window(15, 10, anchor='nw', window=sender_label)

    time_label = tk.Label(canvas, text=time, font=("Helvetica", 11), bg='#404040', fg='white')
    canvas.create_window(width - 10, 10, anchor='ne', window=time_label)

    text_label = tk.Label(canvas, text=text, font=("Helvetica", 13), bg='#404040', wraplength=width - 20, justify='left', fg='white')
    canvas.create_window(15, 28, anchor='nw', window=text_label)

    temp_root.destroy()

    return canvas

def generate_buttton(root, text, command):
    button = tk.Canvas(root, width=100, height=30, bg='#262626', highlightthickness=0)
    create_rounded_rectangle(button, 0, 0, 100, 30, radius=15, fill='#404040', outline='#404040')
    button.create_text(50, 15, text=text, font=("Helvetica", 10, "bold"), fill='white')
    button.bind("<Button-1>", lambda e: command())
    return button

def generate_chatname(root, name, command, is_active):
    chatname = tk.Canvas(root, width=150, height=50, bg='#262626', highlightthickness=0)
    if is_active:
        create_rounded_rectangle(chatname, 0, 0, 150, 50, radius=15, fill='#99b3e6', outline='#99b3e6')
    else:
        create_rounded_rectangle(chatname, 0, 0, 150, 50, radius=15, fill='#404040', outline='#404040')
    truncated_name = truncate_text(name, 140, ("Helvetica", 12, "bold"), chatname)
    chatname.create_text(75, 25, text=truncated_name, font=("Helvetica", 12, "bold"), fill='white', anchor='center')
    chatname.bind("<Button-1>", lambda e: command())
    return chatname

def truncate_text(text, max_width, font, canvas):
    words = text.split()
    truncated_text = ""
    for word in words:
        test_text = truncated_text + " " + word if truncated_text else word
        temp_text_id = canvas.create_text(0, 0, text=test_text, font=font, anchor='nw')
        bbox = canvas.bbox(temp_text_id)
        canvas.delete(temp_text_id)
        if bbox[2] > max_width:
            if truncated_text:
                truncated_text += "..."
            break
        truncated_text = test_text
    return truncated_text

def center_window(root, width, height):    
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width // 2) - (width // 2)
    y = (screen_height // 2) - (height // 2)
    root.geometry(f'{width}x{height}+{x}+{y}')
    
class text_canvas:
    def __init__(self, root):
        self.root = root
        self.root.update_idletasks()
        self.width = root.winfo_width() - 125
        self.height = 45
        self.canvas = tk.Canvas(root, bg='#262626', highlightthickness=0, height=self.height+10)
        self.canvas.pack(expand=True)
        self.rounded_rect = create_rounded_rectangle(self.canvas, 5, 0, self.width-10, self.height+10, radius=15, fill='#404040', outline='#404040')
        self.text = tk.Text(self.canvas, bg='#404040', fg='white', insertbackground='white', bd=0, height=3, wrap='word', highlightthickness=0, font=('Arial', 13), state='disabled')
        self.text.place(x=15, y=5, width=self.width-30, height=self.height)
        self.state = 'disabled'
    
    def get(self):
        return self.text.get('1.0', 'end-1c')
    
    def delete(self):
        self.text.delete('1.0', 'end')
        
    def update(self):
        text = self.get()
        self.width = self.width = self.root.winfo_width() - 125
        self.canvas.delete(self.rounded_rect)
        self.rounded_rect = create_rounded_rectangle(self.canvas, 5, 0, self.width-10, self.height+10, radius=15, fill='#404040', outline='#404040')
        self.text.config(state=self.state)
        self.text.place(x=15, y=5, width=self.width-30, height=self.height)

# root = tk.Tk()
# canvas = generate_message_canvas(root, 400, 'Sender', 'Time', 'Text', 0, 0, lambda: print('Like'), lambda: print('Comment'), False)
# canvas.pack()
# canvas.delete(1)
# canvas.config(width=600)
# create_rounded_rectangle(canvas, 5, 5, 600, 50, radius=20, fill='#404040', outline='#404040')
# root.mainloop()