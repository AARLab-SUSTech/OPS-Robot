import numpy as np
from numpy.matlib import repmat
from sklearn. preprocessing import normalize
import matplotlib.pyplot as plt
import cv2
from sklearn.cluster import KMeans


class detect():

    def __init__(self, thresh_draw=False, image_on=True,contour_draw=False,circle_draw=False,n_cl=4):
        self.image_on=image_on
        self.contour_draw=contour_draw
        self.thresh_draw=thresh_draw
        self.circle_draw=circle_draw
        self.n_cl=n_cl



    def getFrameLabel(self,img_input,verbose=False):
        # load the frame
        image = np.float32(img_input)
        h, w = np.shape(image)
        img=np.reshape(image,(h,w,1))
        # add coordinates
        row_indexes = np.arange(0,h)
        col_indexes = np.arange(0, w)
        coordinates = np.zeros(shape=(h, w, 2))
        coordinates[..., 0] = normalize(repmat(row_indexes, w, 1).T)
        coordinates[..., 1] = normalize(repmat(col_indexes, h, 1))
        # print(np.shape(coordinates))
        data = np.concatenate((img, coordinates), axis=-1)
        data = (np.reshape(data, newshape=(w * h,3)))
        kmeans = KMeans(n_clusters=self.n_cl, random_state=0).fit(data)
        labels_new = kmeans.labels_
        num=np.zeros((3,1))
        num[0] = sum(labels_new==0)
        num[1] = sum(labels_new==1)
        num[2] = sum(labels_new==2)
        labels_new[labels_new==np.argmax(num)]=255
        labels_new[labels_new==np.argmin(num)]=255
        
        # print('num',h)
        frame_new = np.reshape(labels_new, newshape=(h,w))


        b=frame_new[h-20:h]
        b=b[:,np.arange(w-20,w)]
        if sum(sum(b))>500:
            frame_new=~frame_new


        frame_new = np.array(frame_new,dtype='uint8')


        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE,(10,10))
        frame_new = cv2.erode(frame_new,kernel)        #腐蚀图像
        dilated = cv2.dilate(frame_new,kernel)      #膨胀图像

        if self.thresh_draw ==True:
            cv2.imshow('thresh_draw',frame_new)
            cv2.waitKey(1)
        return frame_new


    def find_contour(self,frame):
        frame=np.array(frame,dtype='uint8')

        ret, binary = cv2.threshold(frame, 120, 255,cv2.THRESH_BINARY)
        contours,hierarch=cv2.findContours(binary,cv2.RETR_CCOMP,cv2.CHAIN_APPROX_NONE)

        contour_area = []
        for i in range(len(contours)):
            contour_area.append(cv2.contourArea(contours[i]))
        # background = np.ones(np.shape(frame),dtype=np.uint8)
        max_contour = contours[np.argmax(contour_area)]
        return max_contour



    def find_xy(self,image):
        #decrease resolution
        fx = 0.3
        fy = 0.3
        frame = cv2.resize(image, (0, 0), fx=fx, fy=fy, interpolation=cv2.INTER_NEAREST)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h,w=np.shape(frame)
        # cut the dectetion frame
        
        offset_x = 0.35
        frame=frame[0:int(h*0.35)]
        frame=frame[:,np.arange(int(w*offset_x),int(w*(1-offset_x)))]

        # kmeans 
        frame = detect.getFrameLabel(self,frame,verbose=False)
        contour= detect.find_contour(self,frame)
        contour=np.reshape(contour,(-1,2))
        contour[:,0]= (contour[:,0] + offset_x*w)*(1/fx)
        contour[:,1]= (contour[:,1]*(1/fy))
        
        point=contour[np.argmax(contour[:,1]),:]
        cx=int(point[0])
        cy=int(point[1])

        if self.image_on==True:   
        # draw the contour of the detection area
            if self.contour_draw == True:
                b=np.shape(contour)
                new_contour=np.reshape(contour,(-1,1,2))
                frame_contour=cv2.drawContours(image,new_contour,-1,color=(0,255,0),  thickness=2, lineType=None,maxLevel=1, offset=None)

            if self.circle_draw == True:
                # (x,y),radius = cv2.minEnclosingCircle(contour)
                x=int(point[0])
                y=int(point[1])
                beta=0.3
                if (x>500 and x<700 and y>100 and y<250):
                    beta=0.7
                frame_contour = cv2.circle(image,(x,y),15,(0,0,255),4)
                zeros = np.zeros((image.shape), dtype=np.uint8)
                e1 = cv2.ellipse(zeros,(x+370,y+50),(150,60),90,0,360,(200,0,0),-1)
                e2 = cv2.ellipse(zeros,(x-300,y+50),(150,60),90,0,360,(200,0,0),-1)
                e=np.array((e1+e2))
                # frame_contour=0.3*e+image
                frame_contour = cv2.addWeighted(image,1, e, beta, 0)
                # frame_contour = cv2.line(image,(int(point[0]),int(point[1])),(int(point[0]),int(point[1])+100),(0,0,255),1,4)
                # frame_contour = cv2.line(image,(int(point[0]-250),int(point[1])+100),(int(point[0]+250),int(point[1])+100),(0,0,255),1,4)


        return frame_contour, cx, cy



    def weather_swab(self,frame,thr=150):
        frame = cv2.resize(frame, (0, 0), fx=0.3, fy=0.3, interpolation=cv2.INTER_NEAREST)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        h,w=np.shape(frame)
        frame=frame[0:int(h*0.5)]
        ret, binary = cv2.threshold(frame, thr, 1,cv2.THRESH_BINARY)
        cv2.imshow('b',binary)
        cv2.waitKey(1)
        num = sum(binary.flatten())
        # print('shape:',np.shape(binary))
        # print('sum:',num )
        if num >=600:
            boolean = True
        else:
            boolean = False

        return boolean




