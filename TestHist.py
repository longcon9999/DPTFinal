import cv2
from colordescriptor import ColorDescriptor

url = 'static/dataset/Bunny1.png'
img = cv2.imread(url)
cd = ColorDescriptor((10, 12, 4))
cd.hist2d(img)
cd.hist2dv2(img)
