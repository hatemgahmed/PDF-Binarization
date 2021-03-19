
from pdf2image import convert_from_path
from tkinter import *
from tkinter import filedialog
from PIL import Image, ImageOps
import numpy as np
import cv2
import os

# Helper tasks for filling in the gaps
def erosion(img):
    kernel = np.ones((3,3),np.uint8)
    return cv2.erode(img,kernel,iterations = 1)
def dilation(img):
    kernel = np.ones((3,3),np.uint8)
    return cv2.dilate(img,kernel,iterations = 1)

def pdf2img(path):
    images = convert_from_path(str(path))
    outImages=[]
    for img in images:
        img=ImageOps.grayscale(img)
        im=np.array(img)
        
        # Compute edges
        edges=cv2.Canny(im,threshold1=100,threshold2=255)
        edges=255-edges
        # close gaps between enclosed edges
        edges=dilation(dilation(erosion(erosion(edges))))
        # Perform computations on larger scale
        im=im.astype('int32')
        im+=100     # increase brightness
        im-=((255-edges)/1.5).astype('int32')       # Add edges to the image
        # Thresholding
        thresh=120
        im[im>thresh]=255
        im[im<thresh]=0
        # Typecast back to range 0-255
        im[im>255]=255
        im[im<0]=0
        im=im.astype('uint8')

        im=Image.fromarray(im)
        outImages.append(im)
    # Want the file in same location of original file
    dir,file=os.path.split(os.path.abspath(path))
    savePath=os.path.join(dir,file[:-4]+"_processed"+".pdf")
    outImages[0].save(savePath,save_all=True, append_images=outImages)
        
#Get file path
filename=filedialog.askopenfilename(title = "Select file",filetypes = (("pdf files","*.pdf"),("all files","*.*")))
pdf2img(filename)