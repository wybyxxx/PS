# import the opencv library 
import cv2 

# define a video capture object 
WIDTH=1280
HEIGHT=960


vid0 = cv2.VideoCapture(0)
vid0.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
vid0.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
vid0.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
vid0.set(cv2.CAP_PROP_FPS,30)


# vid1 = cv2.VideoCapture(1)
# vid1.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
# vid1.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
# vid1.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
# vid1.set(cv2.CAP_PROP_FPS,30)



# vid2 = cv2.VideoCapture(2)
# vid2.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
# vid2.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
# vid2.set(6,cv2.VideoWriter.fourcc('M','J','P','G'))
# vid2.set(cv2.CAP_PROP_FPS,30)

  
while(True):
      
    # Capture the video frame 
    # by frame 
    ret0, frame0 = vid0.read()
    # ret1, frame1 = vid1.read()
    # ret2, frame2 = vid2.read()
  
    # Display the resulting frame 
    cv2.imshow('frame 0', frame0)
    # cv2.imshow('frame 1', frame1)
    # cv2.imshow('frame 2', frame2)
      
    # the 'q' button is set as the 
    # quitting button you may use any 
    # desired button of your choice 
    if cv2.waitKey(1) & 0xFF == ord('q'): 
        break
  
# After the loop release the cap object 
vid0.release() 
# vid1.release()
# vid2.release()
# Destroy all the windows 
cv2.destroyAllWindows() 
