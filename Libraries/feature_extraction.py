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


def generate_hsv_map(img_source:str, save:bool, show:bool, part, test:any):
      #part 0 = hue, part 1 = saturation, part 2 = value, part 3 = test

      
      img = cv2.imread(f"{img_source}")
      hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
      H, S, V = cv2.split(hsv)

      image = []

      for count_out, row in enumerate(H):
            row_pixels = []
            for count_in, value in enumerate(row):
                  current_H = int(value)
                  current_S = int(S[count_out][count_in])
                  current_V = int(V[count_out][count_in])

                  if part == 0:
                        row_pixels.append([current_H, 255, 255])
                  elif part == 1:
                        row_pixels.append([179, current_S, 255])
                  elif part == 2:
                        row_pixels.append([179, 255, current_V])
                  elif part == 3:
                        builder = []
                        if test[0] == 1:
                              builder.append(current_H)
                        else:
                              builder.append(179)
                        if test[1] == 1:
                              builder.append(current_S)
                        else:
                              builder.append(255)
                        if test[2] == 1:
                              builder.append(current_V)
                        else:
                              builder.append(255)

                        row_pixels.append(builder)

                  else:
                        #fail case, invalid part num
                        return "Invalid part number"
                  
            image.append(row_pixels)



      print("completed image generation")
      hsv_image = np.array(image, dtype=np.uint8)
      bgr = cv2.cvtColor(hsv_image, cv2.COLOR_HSV2BGR)

      if save:
            cv2.imwrite(f"{img_source[:-4]}-{part}br.png", bgr)

      if show:
            cv2.imshow("image", bgr)
            cv2.waitKey(0)


generate_hsv_map(r"demo/HSV Map demo/full-frame.png", True, False, 3, [1,1,0])