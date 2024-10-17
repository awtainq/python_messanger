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

def add_message(canvas, x, y, width, height, sender, time, text, likes, comments):
    # Создание фона сообщения с закругленными углами
    create_rounded_rectangle(canvas, x, y, x + width, y + height, radius=20, fill='lightblue')

    # Добавление метки с ником отправителя
    sender_label = tk.Label(canvas, text=sender, font=("Helvetica", 12, "bold"), bg='lightblue')
    canvas.create_window(x + 10, y + 10, anchor='nw', window=sender_label)

    # Добавление метки с временем отправки
    time_label = tk.Label(canvas, text=time, font=("Helvetica", 10), bg='lightblue')
    canvas.create_window(x + width - 10, y + 10, anchor='ne', window=time_label)

    # Добавление метки с текстом сообщения
    text_label = tk.Label(canvas, text=text, font=("Helvetica", 12), bg='lightblue', wraplength=width - 20, justify='left')
    canvas.create_window(x + 10, y + 40, anchor='nw', window=text_label)

    # Добавление кнопки лайка
    like_button = tk.Button(canvas, text=f'👍 {likes}', command=lambda: print("Liked!"))
    canvas.create_window(x + 10, y + height - 30, anchor='sw', window=like_button)

    # Добавление кнопки комментария
    comment_button = tk.Button(canvas, text=f'🗨 {comments}', command=lambda: print("Commented!"))
    canvas.create_window(x + width - 10, y + height - 30, anchor='se', window=comment_button)

root = tk.Tk()
canvas = tk.Canvas(root, width=500, height=500)
canvas.pack()

# Добавление сообщения на Canvas
add_message(canvas, 20, 20, 460, 150, "User123", "12:34 PM", "This is a sample message.", 5, 3)

root.mainloop()