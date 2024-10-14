# coding=utf-8
import cv2
import torch
import serial
from ultralytics import YOLO
from dscamera.dscamera.camera import DSCamera

'''box内容
cls: tensor([2., 2., 2.])
conf: tensor([0.7348, 0.7214, 0.7010])
data: tensor([[2.5676e+02, 2.7926e+02, 3.1822e+02, 3.2295e+02, 1.0000e+00, 7.3481e-01, 2.0000e+00],
        [3.6795e+02, 2.5550e+02, 4.1459e+02, 2.8850e+02, 2.0000e+00, 7.2141e-01, 2.0000e+00],
        [8.1858e+02, 3.2820e+02, 9.2200e+02, 3.9968e+02, 3.0000e+00, 7.0101e-01, 2.0000e+00]])
id: tensor([1., 2., 3.])
is_track: True
orig_shape: (622, 1104)
shape: torch.Size([3, 7])
xywh: tensor([[287.4892, 301.1048,  61.4607,  43.6855],
        [391.2666, 271.9997,  46.6412,  32.9959],
        [870.2893, 363.9404, 103.4269,  71.4856]])
xywhn: tensor([[0.2604, 0.4841, 0.0557, 0.0702],
        [0.3544, 0.4373, 0.0422, 0.0530],
        [0.7883, 0.5851, 0.0937, 0.1149]])
xyxy: tensor([[256.7588, 279.2621, 318.2195, 322.9476],
        [367.9460, 255.5017, 414.5872, 288.4976],
        [818.5758, 328.1976, 922.0027, 399.6832]])
xyxyn: tensor([[0.2326, 0.4490, 0.2882, 0.5192],
        [0.3333, 0.4108, 0.3755, 0.4638],
        [0.7415, 0.5276, 0.8351, 0.6426]])'''

obj = 0  # 追踪人

WIDTH = 1280
HEIGHT = 960

H = 512
W = 512

calibration_path = r"/dscamera/example/calibration3-0.json"
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
# Load the YOLOv8 model
model = YOLO(r"/ultralytics-main/models/yolov8n.pt")


prot = 'COM7'
baudrate = 115200
move_x = 0
move_y = 0
servo0 = 1500
servo1 = 1500
k = 0.2

ser = serial.Serial(prot, baudrate)


def steering_gear_control(H, V):
    commandH = '''#000P%dT1000!''' % H
    commandH = commandH.encode('utf-8')
    print('commandH:', commandH)
    ser.write(commandH)

    # time.sleep(0.01)

    commandV = '''#001P%dT1001!''' % V
    commandV = commandV.encode('utf-8')
    print('commandV:', commandV)
    ser.write(commandV)


def set_servo0_servo1(cx, cy, px, py):
    '''
    cx cy:目标物中心位置坐标
    px py:图片中心点坐标
    '''
    global move_x, move_y
    global servo0, servo1
    global H, W
    if (abs(cx - px) >= 20):
        if cx > px:
            move_x = -k * abs(cx - px)
        else:
            move_x = k * abs(cx - px)
        servo0 = int(servo0 + move_x)

    if (abs(cy - py) >= 20):
        if cy < py:
            move_y = -k * abs(cy - py)
        else:
            move_y = k * abs(cy - py)

        servo1 = int(servo1 - move_y)

    if servo0 > 2500:
        servo0 = 2500
    elif servo0 < 500:
        servo0 = 500
    if servo1 > 2200:
        servo1 = 2200
    elif servo1 < 830:
        servo1 = 830


# 设置初始位置
steering_gear_control(1500, 1500)

cap = cv2.VideoCapture(0)
cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)
cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
cap.set(cv2.CAP_PROP_FPS, 30)

cam = DSCamera(calibration_path)

cv2.namedWindow("YOLOv8 Tracking", cv2.WINDOW_NORMAL)
cv2.resizeWindow("YOLOv8 Tracking", H, W)

if __name__ == '__main__':
    # Loop through the video frames
    while cap.isOpened():
        # Read a frame from the video
        success, frame = cap.read()

        if success:

            #img_tensor = torch.from_numpy(frame.copy()).cuda()

            equirect = cam.to_equirect(frame, img_size=(512, 1024))

            equirect = equirect[:, 256:768]

            # Run YOLOv8 tracking on the frame, persisting tracks between frames
            results = model.track(equirect, persist=True)
            annotated_frame = results[0].plot()

            # Display the annotated frame
            cv2.imshow("YOLOv8 Tracking", annotated_frame)
            boxes = results[0].boxes  #
            indices = (boxes.cls == obj).nonzero(as_tuple=True)[0]

            if indices.shape[0] == 0:
                print(f"cls{obj}:No boxes")
            else:
                idx = indices[0]
                xywh = results[0].boxes.xywh[idx]
                print("xywh:", xywh)  # (中心点x, 中心点y, 宽, 高)
                set_servo0_servo1(int(xywh[0]), int(xywh[1]), W // 2, H // 2)
                steering_gear_control(servo0, servo1)

            # Break the loop if 'q' is pressed
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break
        else:
            # Break the loop if the end of the video is reached
            break

    # Release the video capture object and close the display window
    cap.release()
    cv2.destroyAllWindows()
    ser.close()
