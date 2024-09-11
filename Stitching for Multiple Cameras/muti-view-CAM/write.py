# import the opencv library 
import cv2 
import numpy as np
import os
import time


WIDTH=1280
HEIGHT=960
format='.jpg'

out_path0 = r'E:\JUFE\data\medical\zxy\0'
out_path1 = r'E:\JUFE\data\medical\zxy\1'
out_path2 = r'E:\JUFE\data\medical\zxy\2'

os.makedirs(out_path0,exist_ok=True)
os.makedirs(out_path1,exist_ok=True)
os.makedirs(out_path2,exist_ok=True)

out_paths = [out_path0,out_path1,out_path2]
# define a video capture object 

vid0 = cv2.VideoCapture(0) 
vid0.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid0.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid0.set(cv2.CAP_PROP_FPS,30)

vid1 = cv2.VideoCapture(1)
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid1.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid1.set(cv2.CAP_PROP_FPS,30)

vid2 = cv2.VideoCapture(2)
vid2.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid2.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid2.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid2.set(cv2.CAP_PROP_FPS,30)

i=1
ret0, frame0 = vid0.read() 
cv2.imshow('在此窗口内按\'q\'键停止拍摄', frame0[:50,:50,:])

f0=[]
f1=[]
f2=[]
Cams = [f0,f1,f2]
while(True):     
    # Capture the video frame 
    # by frame 
    ret0, frame0 = vid0.read() 
    ret1, frame1 = vid1.read()
    ret2, frame2 = vid2.read()

    if i==1:
        start_time = time.perf_counter()
    f0.append(frame0)
    f1.append(frame1)
    f2.append(frame2)

    i = i+1

    # the 'q' button is set as the 
    print(i)
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break

end_time = time.perf_counter()
duration_ms = (end_time - start_time)
print(f"运行{duration_ms:.4f}秒，平均帧率{(i+1)/duration_ms}")
# After the loop release the cap object 

for idx, cam in enumerate(Cams):
    i=1
    for f in cam:
        cv2.imwrite(os.path.join(out_paths[idx],str(i)+format), f)
        i+=1
    print(f"cap{idx} has been saved...")

vid0.release() 
# vid1.release()
# vid2.release()

# Destroy all the windows 
cv2.destroyAllWindows() 
