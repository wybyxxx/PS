# import the opencv library 
import cv2 
import time

# define a video capture object 
vid0 = cv2.VideoCapture(0)
WIDTH=1280
HEIGHT=960


vid0.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid0.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid0.set(cv2.CAP_PROP_FPS,30)
vid0.set(cv2.CAP_PROP_RECTIFICATION,1)


# vid0.set(cv2.CAP_PROP_BRIGHTNESS,100)
# vid0.set(cv2.CAP_PROP_CONTRAST, 50)
# vid0.set(cv2.CAP_PROP_SATURATION, 80)

# vid0.set(cv2.CAP_PROP_BRIGHTNESS, 0)
# vid0.set(cv2.CAP_PROP_CONTRAST, 1)
# vid0.set(cv2.CAP_PROP_SATURATION, 60)

# vid0.set(cv2.CAP_PROP_AUTO_EXPOSURE, 3)
# vid0.set(cv2.CAP_PROP_AUTO_EXPOSURE, 1)
# vid0.set(cv2.CAP_PROP_EXPOSURE,-6)


print(vid0.get(3),vid0.get(4))
print(vid0.get(cv2.CAP_PROP_BRIGHTNESS),vid0.get(cv2.CAP_PROP_CONTRAST),vid0.get(cv2.CAP_PROP_SATURATION),vid0.get(cv2.CAP_PROP_EXPOSURE))
print(vid0.get(cv2.CAP_PROP_RECTIFICATION),vid0.get(cv2.CAP_PROP_FPS))

counter = -1
start_time = time.time()
while(True): 
    ret0, frame0 = vid0.read() 
    if counter == -1:
        counter = 0
    counter += 1
    elapsed_time = time.time() - start_time
    if elapsed_time > 0:
        fps = counter / elapsed_time
        cv2.putText(frame0, f"FPS: {fps:.2f}", (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
    cv2.imshow('frame 0', frame0) 

      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid0.release() 

# Destroy all the windows 
cv2.destroyAllWindows() 
