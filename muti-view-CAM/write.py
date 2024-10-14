# import the opencv library 
import cv2 
import numpy as np
import os
import time

WIDTH=1280
HEIGHT=960
format='.jpg'

out_path0 = r'D:\app\Zotero\BaiduSyncdisk\jxufe\data\medical\3d\0'
out_path1 = r'D:\app\Zotero\BaiduSyncdisk\jxufe\data\medical\3d\1'
out_path2 = r'D:\app\Zotero\BaiduSyncdisk\jxufe\data\medical\3d\2'

os.makedirs(out_path0,exist_ok=True)
os.makedirs(out_path1,exist_ok=True)
os.makedirs(out_path2,exist_ok=True)

out_paths = [out_path0,out_path1,out_path2]
# define a video capture object 
print('a')
vid0 = cv2.VideoCapture(0) 
vid0.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid0.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid0.set(cv2.CAP_PROP_FPS,30)


print('a1')
vid1 = cv2.VideoCapture(1)
vid1.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid1.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid1.set(cv2.CAP_PROP_FPS,30)
print('a2')

vid2 = cv2.VideoCapture(2)
vid2.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid2.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid2.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid2.set(cv2.CAP_PROP_FPS,30)
print('b')

i=0
last_id = 0
frame = np.zeros([100,100])
cv2.imshow('Press Q to exit...', frame)

Cams = [[],[],[]]
print('c')
record = True

counter = i
fps = 0
while(True):     
    pressedKey = cv2.waitKey(1) & 0xFF
    if record:
        ret0, frame0 = vid0.read()
        ret1, frame1 = vid1.read()
        ret2, frame2 = vid2.read()

        if counter == i:
            start_time = time.time()

        Cams[0].append(frame0)
        Cams[1].append(frame1)
        Cams[2].append(frame2)

        i = i+1

        # fps = (i-counter) / (time.time() - start_time) if i%20==0 else 0
        print(i)

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
        counter = i
        
        
vid0.release() 
vid1.release()
vid2.release()

# Destroy all the windows 
cv2.destroyAllWindows()
