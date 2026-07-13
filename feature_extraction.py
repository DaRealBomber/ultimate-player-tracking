import cv2


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


image_path = r"C:\Users\parent\Documents\GitHub\ultimate-player-tracking\night-pretrain\night-training-data_00162.jpg"
crop_folder = r"C:\Users\parent\Documents\GitHub\ultimate-player-tracking\cropped_images"
custom_label = "0 0.473591 0.436885 0.0223117 0.10577 0.928218"
custom_corners = normalize_coordinates(image_path, custom_label, True)

image_cropping(image_path, crop_folder, "crop_yay", custom_corners)
