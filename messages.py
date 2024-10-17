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
    canvas = tk.Canvas(root, width=width, height=height)
    
    # Создание фона сообщения с закругленными углами
    create_rounded_rectangle(canvas, 5, 5, width, height, radius=20, fill='#404040')

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

