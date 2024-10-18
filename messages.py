import tkinter as tk

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

def create_custom_button(canvas, x, y, width, height, text, command):
    button = tk.Canvas(canvas, width=width, height=height, bg='#404040', highlightthickness=0)
    create_rounded_rectangle(button, 0, 0, width, height, radius=15, fill='#262626', outline='#262626')
    button.create_text(width//2, height//2, text=text, font=("Helvetica", 12, "bold"), fill='white')
    button.bind("<Button-1>", lambda e: command())
    canvas.create_window(x, y, anchor='nw', window=button)
    return button

def generate_message_canvas(root, width, sender, time, text, likes, comments, like_command, comment_command):
    # Создание временного окна для вычисления высоты текста
    temp_root = tk.Toplevel(root)
    temp_root.withdraw()  # Скрыть временное окно

    temp_canvas = tk.Canvas(temp_root, width=width)
    temp_text_label = tk.Label(temp_canvas, text=text, font=("Helvetica", 12), wraplength=width - 20, justify='left')
    temp_text_label.update_idletasks()
    text_height = temp_text_label.winfo_reqheight()

    # Высота сообщения с учетом высоты текста и дополнительных элементов
    height = text_height + 95

    # Создание основного Canvas
    canvas = tk.Canvas(root, width=width, height=height, bg='#262626',highlightthickness=0)
    
    # Создание фона сообщения с закругленными углами
    create_rounded_rectangle(canvas, 5, 5, width, height, radius=20, fill='#404040', outline='#404040')

    # Добавление метки с ником отправителя
    sender_label = tk.Label(canvas, text=sender, font=("Helvetica", 13, "bold"), bg='#404040')
    canvas.create_window(15, 10, anchor='nw', window=sender_label)

    # Добавление метки с временем отправки
    time_label = tk.Label(canvas, text=time, font=("Helvetica", 11), bg='#404040')
    canvas.create_window(width - 10, 10, anchor='ne', window=time_label)

    # Добавление метки с текстом сообщения
    text_label = tk.Label(canvas, text=text, font=("Helvetica", 13), bg='#404040', wraplength=width - 20, justify='left')
    canvas.create_window(15, 40, anchor='nw', window=text_label)

    # Добавление кастомной кнопки лайка
    create_custom_button(canvas, 15, height - 40, 60, 30, f'♥️ {likes}', command=like_command)

    # Добавление кастомной кнопки комментария
    create_custom_button(canvas, width - 75, height - 40, 60, 30, f'💬 {comments}', command=comment_command)

    temp_root.destroy()  # Уничтожить временное окно

    return canvas

def generate_comment_canvas(root, width, sender, time, text):
    # Создание временного окна для вычисления высоты текста
    temp_root = tk.Toplevel(root)
    temp_root.withdraw()  # Скрыть временное окно

    temp_canvas = tk.Canvas(temp_root, width=width, bg='#262626')
    temp_text_label = tk.Label(temp_canvas, text=text, font=("Helvetica", 12), wraplength=width - 20, justify='left')
    temp_text_label.update_idletasks()
    text_height = temp_text_label.winfo_reqheight()

    # Высота сообщения с учетом высоты текста и дополнительных элементов
    height = text_height + 50

    # Создание основного Canvas
    canvas = tk.Canvas(root, width=width, height=height, bg='#262626', highlightthickness=0)
    
    # Создание фона сообщения с закругленными углами
    create_rounded_rectangle(canvas, 5, 5, width-5, height-5, radius=20, fill='#404040', outline='#404040')

    # Добавление метки с ником отправителя
    sender_label = tk.Label(canvas, text=sender, font=("Helvetica", 13, "bold"), bg='#404040')
    canvas.create_window(15, 10, anchor='nw', window=sender_label)

    # Добавление метки с временем отправки
    time_label = tk.Label(canvas, text=time, font=("Helvetica", 11), bg='#404040')
    canvas.create_window(width - 10, 10, anchor='ne', window=time_label)

    # Добавление метки с текстом сообщения
    text_label = tk.Label(canvas, text=text, font=("Helvetica", 13), bg='#404040', wraplength=width - 20, justify='left')
    canvas.create_window(15, 40, anchor='nw', window=text_label)

    temp_root.destroy()  # Уничтожить временное окно

    return canvas

def generate_buttton(root, text, command):
    button = tk.Canvas(root, width=100, height=30, bg='#262626', highlightthickness=0)
    create_rounded_rectangle(button, 0, 0, 100, 30, radius=15, fill='#404040', outline='#404040')
    button.create_text(50, 15, text=text, font=("Helvetica", 12, "bold"), fill='white')
    button.bind("<Button-1>", lambda e: command())
    return button


def generate_chatname(root, name, command):
    chatname = tk.Canvas(root, width=150, height=50, bg='#262626', highlightthickness=0)
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

class CustomScrollbar(tk.Canvas):
    def __init__(self, parent, *args, **kwargs):
        super().__init__(parent, *args, **kwargs)
        self.scrollbar = None
        self.scroll_pos = 0
        self.bind("<Configure>", self._update_scrollbar)
        self.bind("<Button-1>", self._start_scroll)
        self.bind("<B1-Motion>", self._scroll)

    def _update_scrollbar(self, event=None):
        self.delete("scrollbar")
        if self.scrollbar:
            self.delete(self.scrollbar)
        # Устанавливаем размеры скроллбара в зависимости от размера области
        view_size = self.winfo_height()
        scrollbar_height = view_size * (self.get()[1] - self.get()[0])
        self.scrollbar = create_rounded_rectangle(self, 0, self.scroll_pos, self.winfo_width(), scrollbar_height, radius=10, fill='#404040', outline='#404040', tags="scrollbar")

    def _start_scroll(self, event):
        # Запоминаем начальную позицию
        self.scan_mark(event.x, event.y)

    def _scroll(self, event):
        # Перетаскивание скроллбара
        self.scan_dragto(event.x, event.y, gain=1)
        self._update_scrollbar()

    def set(self, lo, hi):
        # Обновляем позицию скроллбара на основе переданных значений
        self.scroll_pos = float(lo) * self.winfo_height()
        self.coords(self.scrollbar, 0, self.scroll_pos, self.winfo_width(), float(hi) * self.winfo_height())
        self._update_scrollbar()

    def get(self):
        # Возвращаем позицию скроллбара в формате (lo, hi)
        return self.coords(self.scrollbar)