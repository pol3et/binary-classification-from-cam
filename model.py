from sklearn.svm import LinearSVC
import cv2 as cv
import numpy as np
import PIL

class Model:

    def __init__(self):
        self.model = LinearSVC(dual=False)
        self.isfit = False

    def train(self, counters):
        img_list = []
        labels = []
        
        for i in range(1, counters[0]):
            img = cv.imread(f'1/frame{i}.jpg',0).reshape(-1)
            img_list.append(img)
            labels.append(1)

        for i in range(1, counters[1]):
            img = cv.imread(f'2/frame{i}.jpg',0).reshape(-1)
            img_list.append(img)
            labels.append(2)

        img_list = np.array(img_list).reshape(len(img_list), -1)

        self.isfit = True
        self.model.fit(img_list, labels)
        

    def predict(self, frame):
        if not self.isfit:
            return -1
        else:
            cv.imwrite('frame.jpg', cv.cvtColor(frame, cv.COLOR_RGB2GRAY))
            img = PIL.Image.open('frame.jpg')
            img.thumbnail((150, 150), PIL.Image.BOX)
            img.save('frame.jpg')

            img = cv.imread('frame.jpg', 0).reshape(-1)
            return self.model.predict([img])[0]