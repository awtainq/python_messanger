import tkinter as tk

class ResizeApp:
    def __init__(self, root):
        self.root = root
        self.root.geometry("400x300")
        self.root.title("Изменение окна и отпускание мыши")

        # Привязка событий
        self.root.bind("<Configure>", self.on_window_resize)
        self.root.bind("<ButtonRelease-1>", self.on_mouse_release)

        # Флаг, чтобы отслеживать изменение окна
        self.window_resized = False

        # Метка для отображения информации
        self.label = tk.Label(self.root, text="Измените размер окна мышью", font=("Helvetica", 14))
        self.label.pack(pady=20)

    def on_window_resize(self, event):
        """Отслеживает изменение размера окна"""
        self.window_resized = True
        self.new_width = event.width
        self.new_height = event.height

    def on_mouse_release(self, event):
        """Отслеживает отпускание кнопки мыши"""
        if self.window_resized:
            self.label.config(text=f"Окно изменено: ширина={self.new_width}, высота={self.new_height}")
            self.window_resized = False  # Сбрасываем флаг после изменения

# Запуск приложения
root = tk.Tk()
app = ResizeApp(root)
root.mainloop()