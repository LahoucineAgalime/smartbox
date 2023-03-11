
from django.shortcuts import render
from django.http import HttpResponse, JsonResponse,StreamingHttpResponse
from .video import VideoCamera
from .models import Camera
import redis
import json

pool = redis.ConnectionPool(host='localhost', port=6379, decode_responses=True)
client = redis.Redis(connection_pool=pool)

def index(request):
    return render(request, 'monitor/index.html')


def real(request):
    uid=request.GET.get('uid')
    assert uid,'uid不能为空'
    camera=Camera.objects.get(uid=uid)
    rtsp=camera.rtsp
    camera=VideoCamera(rtsp)
    return StreamingHttpResponse(camera.gen(),
                    content_type='multipart/x-mixed-replace; boundary=frame')

def camera_list(request):
    cameras=Camera.objects.all()
    result={}
    cam_list=[]
    for camera in cameras:
        temp={}
        temp['uid']=camera.uid
        temp['name']=camera.name
        temp['rtsp']=camera.rtsp
        temp['position']=camera.position
        temp['is_active']=camera.is_active
        temp['img']=client.get(camera.uid)
        cam_list.append(temp)
    result['msg']='success'
    result['status']=1
    result['data']=cam_list
    return JsonResponse(result)


