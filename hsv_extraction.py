
#hsv extraction tool
import cv2
import matplotlib.pyplot as plt


img = cv2.imread(r"C:\Users\parent\Documents\GitHub\ultimate-player-tracking\full-frame.png")

def generate_histogram(path:str):
      img = cv2.imread(rf"{path}")
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

H, S, V = cv2.split(hsv)



plt.hist(H.ravel(), bins=180)
plt.show()