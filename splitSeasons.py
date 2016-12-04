import cv2
import numpy as np

path = 'image.jpg'
img = cv2.imread(path)
height = int(np.size(img, 0))
width = int(np.size(img, 1))

crop_img1 = img[:height//2, :width//2]
crop_img2 = img[:height//2, width//2+1:]
crop_img3 = img[height//2+1:, :width//2]
crop_img4 = img[height//2+1:, width//2+1:]

gray = cv2.cvtColor(crop_img1,cv2.COLOR_BGR2GRAY)
print('mat0: ', gray[0,0])
if gray[0,0] >= 250:
	print('first_if')
	cv2.floodFill(gray, None, (0,0), 0)

if gray[0,0] == 0:
	print('second_if')
	_,thresh = cv2.threshold(gray,1,255,cv2.THRESH_BINARY)
	contours = cv2.findContours(thresh,cv2.RETR_EXTERNAL,cv2.CHAIN_APPROX_SIMPLE)
	cnt = contours[0]
	x,y,w,h = cv2.boundingRect(cnt)
	crop = img[y:y+h,x:x+w]
	cv2.imwrite('crop_' + path, crop)

cv2.imwrite('1_' + path, crop_img1)
cv2.imwrite('2_' + path, crop_img2)
cv2.imwrite('3_' + path, crop_img3)
cv2.imwrite('4_' + path, crop_img4)