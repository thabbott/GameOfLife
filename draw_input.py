import cv2
import numpy as np
 
M = 100
N = 100

print("Click with the left mouse button to toggle cell. \n Once done selecting initial conditions, press 'esc'.")
load = input("Load existing file? [Y/N]: ")

# mouse callback function
def draw(event,x,y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
            img[(y,x)] = 1-img[(y,x)]
                
if 'Y' in load:
    fname = input("Name of file: ")
    img = abs(np.loadtxt(fname)-1)
else:
    img = np.ones((N,M))

cv2.namedWindow('Game of Life Initial Conditions',cv2.WINDOW_NORMAL)
cv2.resizeWindow('Game of Life Initial Conditions', 8*M,8*N)
cv2.setMouseCallback('Game of Life Initial Conditions',draw)

while True:
    cv2.imshow('Game of Life Initial Conditions',img)     
    if cv2.waitKey(20) == 27:
        break
cv2.destroyAllWindows()

img= 1-img
img = np.array(img, dtype=np.int8)


name = input("Enter name for output file (if it's the same as the input name, you'll overwrite the original file): ") 
np.savetxt(name,img,fmt="%s")