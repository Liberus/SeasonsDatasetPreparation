import cv2
import numpy as np
import os


src_dir = 'inputs/'
tgt_dir = 'outputs/'
split_dirs = ('C', 'A', 'D', 'B')
prefix = 'splitted'
split_i = 0

def removeBounds(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    print('mat0: ', gray[0,0])

    if gray[0,0] >= 250:
            cv2.floodFill(gray, None, (0,0), 0)

    if gray[0,0] == 0:
            _,thresh = cv2.threshold(gray,240,250,cv2.THRESH_BINARY)
            im2, contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
            image_area = image.shape[0]*image.shape[1]
            contours = [x for x in contours if (cv2.contourArea(x) > 0.8*image_area and cv2.contourArea(x) < 0.98*image_area)]
            cnt = contours[1]
            mask = np.zeros(image.shape[:2], dtype="uint8") # Create mask where white is what we want, black otherwise
            cv2.drawContours(mask, [cnt], -1, 255, -1) # Draw filled contour in mask
            out[mask == 255] = image[mask == 255]
            return out

def removeBounds2(image):
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    print('mat0: ', gray[0,0])
    x, y = 0,0
    w, h = image.shape[:2]
    while np.all(gray[x:x+1][:]) > 240:
        x+=1
    while np.all(gray[w-1:w][:]) > 240:
        h-=1
    while np.all(gray[:][y:y+1]) > 240:
        y+=1
    while np.all(gray[:][h-1:h]) > 240:
        h-=1
    return image[x:w,y:h]

    
def unwind(path):
    global split_i

    img = cv2.imread(path)
    height = int(np.size(img, 0))
    width = int(np.size(img, 1))

    crop_img1 = img[:height//2, :width//2]
    crop_img2 = img[:height//2, width//2+width%2:]
    crop_img3 = img[height//2+height%2:, :width//2]
    crop_img4 = img[height//2+height%2:, width//2+width%2:]

    
    #cv2.imwrite("crop1.jpg", removeBounds2(crop_img1))
    #cv2.imwrite("crop2.jpg", removeBounds2(crop_img2))
    #cv2.imwrite("crop3.jpg", removeBounds2(crop_img3))
    #cv2.imwrite("crop4.jpg", removeBounds2(crop_img4))

    for split_dir, img in zip(split_dirs, (crop_img1, crop_img2, crop_img3, crop_img4)):
        cv2.imwrite('{}{}/{}_{}.jpg'.format(tgt_dir, split_dir, prefix, split_i), img)
    split_i += 1


#for path in os.listdir(src_dir):
#    path = src_dir + path
#    unwind(path)

unwind("image.jpg")
