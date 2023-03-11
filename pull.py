from multiprocessing import Process
from gevent import monkey;monkey.patch_all()
import gevent
import redis
import base64
import time
import cv2
import MySQLdb
import numpy as np
from algo.detection import human_detect

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
client = redis.Redis(connection_pool=pool)
def get_cursor():
    try:
        conn= MySQLdb.connect(
                host='localhost',
                port = 3306,
                user='root',
                passwd='123456',
                db ='monitor',
                )
    except Exception as e:
        pass
    cursor = conn.cursor()
    return cursor

def getCaptureList():
    cursor = get_cursor()
    cursor.execute('select uid,name,rtsp from tb_camera where is_active =1')
    dataset=cursor.fetchall()
    cap_list=[{'uid':d[0],'rtsp':d[2]} for d in dataset]
    return cap_list


def pull(cap,uid):
    f = 10  # 25帧取一张图
    temp = 1
    while True:
        success, frame = cap.read()
        if success:
            temp += 1
            if temp == f:
                img = cv2.imencode('.jpg', frame)[1]
                img_code = str(base64.b64encode(img))[2:-1]
                client.set(uid, img_code)
                return True



def pull_server():
    print('streaming pull server ')
    while True:
        cameras = getCaptureList()
        task_list = []
        for camera in cameras:
            cap = cv2.VideoCapture(camera['rtsp'])
            if cap.isOpened():
                task_list.append(gevent.spawn(pull, cap,camera['uid']))
        gevent.joinall(task_list)
        time.sleep(1)

def algo_server():
    print('algo server ')
    while True:
        cameras = getCaptureList()
        task_list = []
        for camera in cameras:
            code=client.get(camera['uid'])
            code=base64.b64decode(code)
            arr=np.frombuffer(code,np.uint8)
            img = cv2.imdecode(arr, cv2.IMREAD_COLOR)
            task_list.append(gevent.spawn(human_detect,img))
        gevent.joinall(task_list)

if __name__ == '__main__':
    pull_srv = Process(target=pull_server)
    algo_srv = Process(target=algo_server)
    pull_srv.start()
    algo_srv.start()


