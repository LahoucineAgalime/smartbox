import cv2
import base64
import requests

pre_frame = None
def human_detect(frame):
    gray_pic = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    gray_pic = cv2.resize(gray_pic, (480, 480))
    # 用高斯滤波进行模糊处理
    gray_pic = cv2.GaussianBlur(gray_pic, (21, 21), 0)
    # 如果没有背景图像就将当前帧当作背景图片
    global pre_frame
    if pre_frame is None:
        pre_frame = gray_pic
    else:
        # absdiff把两幅图的差的绝对值输出到另一幅图上面来
        img_delta = cv2.absdiff(pre_frame, gray_pic)
        
        # threshold阈值函数(原图像应该是灰度图,对像素值进行分类的阈值,当像素值高于（有时是小于）阈值时应该被赋予的新的像素值,阈值方法)
        thresh = cv2.threshold(img_delta, 30, 255, cv2.THRESH_BINARY)[1]
        # 用一下腐蚀与膨胀
        thresh = cv2.dilate(thresh, None, iterations=2)
        # print(thresh)
        # findContours检测物体轮廓(寻找轮廓的图像,轮廓的检索模式,轮廓的近似办法)
        contours, hierarchy = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for c in contours:
        # 设置敏感度
        # contourArea计算轮廓面积
            if cv2.contourArea(c) < 1000:
                continue
            else:
                try:
                    requests.post('http://localhost:8001/alert',data={'msg':"有人员活动"},timeout=3)
                except:
                    pass
        pre_frame = gray_pic
