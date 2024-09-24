# import the opencv library 
import cv2 
import numpy as np
import os
import time


WIDTH=1280
HEIGHT=960
format='.jpg'

out_path0 = r'E:\jxufe\data\medical\xyz\0'
out_path1 = r'E:\jxufe\data\medical\xyz\1'
out_path2 = r'E:\jxufe\data\medical\xyz\2'

os.makedirs(out_path0,exist_ok=True)
os.makedirs(out_path1,exist_ok=True)
# os.makedirs(out_path2,exist_ok=True)


out_paths = [out_path0,out_path1,out_path2]
# define a video capture object 
print('cam0...')
vid0 = cv2.VideoCapture(0) 
vid0.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid0.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid0.set(cv2.CAP_PROP_FPS,30)
# # 检查设置是否成功
# actual_exposure = vid0.get(cv2.CAP_PROP_EXPOSURE)
# print(f"当前曝光值: {actual_exposure}")


print('cam1...')
vid1 = cv2.VideoCapture(1)
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid1.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid1.set(cv2.CAP_PROP_FPS,30)

# vid1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1.0) # 打开自动曝光
# vid1.set(cv2.CAP_PROP_AUTO_EXPOSURE, 0.0) # 关闭自动曝光
# vid1.set(cv2.CAP_PROP_AUTO_WB, 1.0)
# vid1.set(cv2.CAP_PROP_EXPOSURE, 0.01)
# actual_exposure = vid1.get(cv2.CAP_PROP_EXPOSURE)
# print(f"当前曝光值: {actual_exposure}")

# print('cam2...')
# vid2 = cv2.VideoCapture(2)
# vid2.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
# vid2.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
# vid2.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
# vid2.set(cv2.CAP_PROP_FPS,30)

i=1
last_id = 1
frame = np.zeros([50,50])
cv2.imshow('在此窗口内按\'q\'键停止拍摄', frame)


Cams = [[],[],[]]
print('c')
record = True

while(True):     
    pressedKey = cv2.waitKey(1) & 0xFF
    if record:
        print(i)
        ret0, frame0 = vid0.read()
        ret1, frame1 = vid1.read()
        # ret2, frame2 = vid2.read()

 #       if i==1:
 #           start_time = time.perf_counter()
        Cams[0].append(frame0)
        Cams[1].append(frame1)
        # Cams[2].append(frame2)
        

        i = i+1

    if pressedKey == ord('q'): 
        if record == True:
            for idx, fx in enumerate(Cams):
                id = last_id
                for f in fx:
                    cv2.imwrite(os.path.join(out_paths[idx], str(id) + format), f)
                    id += 1
                print(f"cap{idx} has been saved...")
        Cams=[[],[],[]]
            
        break
        
    elif pressedKey == ord('p'):
        for idx, fx in enumerate(Cams):
            id = last_id
            for f in fx:
                cv2.imwrite(os.path.join(out_paths[idx], str(id) + format), f)
                id += 1
            print(f"cap{idx} has been saved...")
        Cams=[[],[],[]]
            
        last_id = id + 1
        record = False
        
        
    elif pressedKey == ord('r'):
        record = True
        
        
        
#end_time = time.perf_counter()
#duration_ms = (end_time - start_time)
#print(f"运行{duration_ms:.4f}秒，平均帧率{(i+1)/duration_ms}")
# After the loop release the cap object 

vid0.release() 
vid1.release()
# vid2.release()

# Destroy all the windows 
cv2.destroyAllWindows()
