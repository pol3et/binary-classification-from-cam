import camera
import model
import cv2 as cv
import PIL.Image, PIL.ImageTk
import tkinter as tk
from tkinter import simpledialog as sd
import os

class App():

    def __init__(self, window=tk.Tk(), window_title="Camera Classifier"):

        self.window = window
        self.window.title(window_title)

        self.counters = [1,1]
        
        self.model = model.Model()

        self.auto_predict = False

        try:
            self.video = camera.Camera()
        except:
            tk.messagebox.showwarning("Ошибка", "Камера не найдена")
            return

        self.init_gui()

        self.delay = 15
        self.update()

        self.window.attributes('-topmost', True)
        self.window.mainloop()


    def init_gui(self):
        self.canvas = tk.Canvas(self.window, width=self.video.width, height=self.video.height)
        self.canvas.pack()

        self.first_class = sd.askstring("Первый объект", "Введите название первого объекта", parent = self.window)
        self.second_class = sd.askstring("Второй объект", "Введите название второго объекта", parent = self.window)

        self.label = tk.Label(self.window, text='404 meow not found')
        self.label.config(font=("Arial", 20))
        self.label.pack(anchor=tk.CENTER, expand=True)

        self.btn_toggleauto = tk.Button(self.window, text='Авто распознавание', width=50, command=self.auto_predict_toggle)
        self.btn_toggleauto.pack(anchor=tk.CENTER, expand=True)

        self.btn_first_class = tk.Button(self.window, text=self.first_class, width=50,
                                         command=lambda: self.save_class(1))
        self.btn_first_class.pack(anchor=tk.CENTER, expand=True)

        self.btn_second_class = tk.Button(self.window, text=self.second_class, width=50,
                                         command=lambda: self.save_class(2))
        self.btn_second_class.pack(anchor=tk.CENTER, expand=True)

        self.btn_train = tk.Button(self.window, text='Обучить модель', width=50,
                                   command=lambda: self.train_model())
        self.btn_train.pack(anchor=tk.CENTER, expand=True)

        self.btn_predict = tk.Button(self.window, text='Распознать объект', width=50,
                                     command=lambda: self.predict())
        self.btn_predict.pack(anchor=tk.CENTER, expand=True)

        self.btn_reset = tk.Button(self.window, text='Начать заново', width=50,
                                   command=self.reset)
        self.btn_reset.pack(anchor=tk.CENTER, expand=True)
    

    def auto_predict_toggle(self):
        self.auto_predict = not self.auto_predict


    def save_class(self, class_num):
        frame = self.video.get_frame()

        if not os.path.exists('1'):
            os.mkdir('1')
        if not os.path.exists('2'):
            os.mkdir('2')

        cv.imwrite(f'{class_num}/frame{self.counters[class_num-1]}.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
        img = PIL.Image.open(f'{class_num}/frame{self.counters[class_num-1]}.jpg')
        img.thumbnail((150, 150), PIL.Image.BOX)
        img.save(f'{class_num}/frame{self.counters[class_num-1]}.jpg')

        self.counters[class_num-1]+=1

    
    def reset(self):
        for dir in ['1','2']:
            for file in os.listdir(dir):
                file_path = os.path.join(dir, file)
                if os.path.isfile(file_path):
                    os.unlink(file_path)

        self.counters = [1,1]
        self.model = model.Model()
        self.label.config(text='404 meow not found')


    def update(self):
        if self.auto_predict:
            self.predict()

        frame = self.video.get_frame()

        self.photo = PIL.ImageTk.PhotoImage(image=PIL.Image.fromarray(frame))
        self.canvas.create_image(0,0,image=self.photo, anchor=tk.NW)

        self.window.after(self.delay, self.update)

    def train_model(self):
        if self.counters[0] == 1 or self.counters[1] == 1:
            tk.messagebox.showwarning("Ошибка", "Недостаточно данных для обучения")
            return
        self.model.train(self.counters)

    def predict(self):
        frame = self.video.get_frame()

        prediction = self.model.predict(frame)
        if prediction == -1:
            self.auto_predict_toggle()
            self.label.config(text='404 meow not found')
            tk.messagebox.showwarning("Ошибка", "Модель не обучена")

        if prediction == 1:
            self.label.config(text=self.first_class)
        elif prediction == 2:
            self.label.config(text=self.second_class)