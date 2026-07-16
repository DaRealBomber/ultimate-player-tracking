
#hsv extraction tool
import cv2
import matplotlib.pyplot as plt
import numpy as np

big_change = 10
big_H = []
big_S = []
big_V = []

dominant_H = []
respective_S = []
respective_V = []

unique_H = []


img = cv2.imread(r"emilie_cropped.png")


hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

H, S, V = cv2.split(hsv)

def run_dominant(H, S, V):
      for row in H:
            for value in row:
                  big_H.append(int(value)) 

      for row in S:
            for value in row:
                  big_S.append(int(value))

      for row in V:
            for value in row:
                  big_V.append(int(value))


      for value in big_H:
            if not value in unique_H:
                  unique_H.append(value)

      #solve for dominant using big change
      for value in unique_H:
            if unique_H.index(value) != len(unique_H) -1 and abs(unique_H[unique_H.index(value) + 1] - value) > big_change:
                  add = True
                  for i in range(value -5, value + 5):
                        if value in dominant_H:
                              add = False
                  
                  if add:
                        dominant_H.append(value * 2)
                        respective_S.append((big_S[big_H.index(value)]) * 100 / 256)
                        respective_V.append((big_V[big_H.index(value)]) * 100 / 256)


image = []

for row in H:

      row_pixels = []
      for value in row:


            row_pixels.append([int(value), 255, 255])

      image.append(row_pixels)

hsv_image = np.array(image, dtype=np.uint8)

bgr = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
cv2.imshow("image", bgr)
cv2.waitKey(0)

def generate_hsv_map(img_source:str):
      img = cv2.imread(f"{img_source}")

      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)

      H, S, V = cv2.split(hsv)

      image = []

      for row in H:

            row_pixels = []
            for value in row:


                  row_pixels.append([int(value), 255, 255])

            image.append(row_pixels)

      hsv_image = np.array(image, dtype=np.uint8)

      bgr = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)
      cv2.imshow("image", bgr)
      cv2.waitKey(0)

# # plt.hist(H.ravel(), bins=180)
# # plt.show()