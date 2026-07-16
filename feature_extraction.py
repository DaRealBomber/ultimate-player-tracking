import cv2
import numpy as np

def image_cropping(original_path:str, return_folder:str, cropped_name:str, corner_list:list):
      '''
      For image cropping before running feature extraction

      orignal path as string (include r in front of string to avoid formatting issues)
      
      corner list format as [bottom y, top y, bottom x, top x]

      '''
      
      
      img = cv2.imread(original_path)
      cropped_img = img[corner_list[0]:corner_list[1], corner_list[2]:corner_list[3]]

      cv2.imwrite(fr"{return_folder}\{cropped_name}.jpg", cropped_img)



# image_cropping(r"night-pretrain/night-training-data_00162.jpg", r"C:\Users\parent\Documents\GitHub\ultimate-player-tracking\cropped_images", "crop_test",  )

def normalize_coordinates(image_path:str, label:str, convert: bool):

      img = cv2.imread(image_path)
      height, width = img.shape[:2]

      #check for confidence label
      parts = label.split()
      if len(parts) > 5:
            parts = parts[0:5]

      cls, cx, cy, w, h = map(float, parts)

      cx *= width
      cy *= height
      w *= width
      h *= height

      if not convert:
            return [cx, cy, w, h]
      else:
            return[int(cy - (h/2)), int(cy + (h/2)), int(cx - (w/2)), int(cx + (w/2))]


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


generate_hsv_map(r"C:\Users\parent\Documents\GitHub\ultimate-player-tracking\demo\homography demo\full-court.jpeg")