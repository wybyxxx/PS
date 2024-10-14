# coding:GBK
from ast import Import
import cv2
import serial
import struct
import time
import numpy as np

# 打开串口
# ser = serial.Serial('COM4', 921600)  # 将 COM1 替换为你的串口号和相应的波特率


ser = serial.Serial('COM6', 115200)  # 将 COM1 替换为你的串口号和相应的波特率


def imshow(img):
    # 解码图像数据
    img = cv2.imdecode(np.frombuffer(img, dtype=np.uint8), cv2.IMREAD_COLOR)

    # 显示图像
    cv2.imshow("Received Image", img)
    cv2.waitKey(1)
    key = cv2.waitKey(1)
    if key == 32:  # 空格退出
        cv2.destroyAllWindows()
        while True:
            pass


# 接收图像并保存
# file_preserve = 1 保存图片文件
def receive_and_save_image(output_path, file_preserve):
    # 读取图像大小
    print('read')
    size_data = ser.read(100)
    print('size_data', size_data)
    size = struct.unpack("<L", size_data)[0]

    # 读取图像数据
    image_data = ser.read(size)
    print('image_data', image_data)
    # # 解码图像数据
    img = cv2.imdecode(np.frombuffer(image_data, dtype=np.uint8), cv2.IMREAD_COLOR)

    # 保存图像
    if file_preserve == 1:
        with open(output_path, 'wb') as file:
            file.write(image_data)

    # 发送确认信号 "#"
    ser.write(b'#')
    #
    # 接收停止信号
    stop_signal = ser.read(1)
    if stop_signal == b'#':
        # imshow(image_data)
        return img, True
    else:
        return img, False


# 图像保存路径
output_image_path = r'E:\jxufe\codes\Stitching for Multiple Cameras\received_image.jpg'

while True:
    # 在需要延时的地方调用sleep()函数
    # time.sleep(0.01)  # 延时0.1秒
    # 循环接收并保存图像
    # key = int(input("请输入: "))
    key = 1
    if key == 0:
        break

    while key == 1:
        img, uart_img_key = receive_and_save_image(output_image_path, 0)
        if uart_img_key:
            imshow(img)
            break

# 关闭串口
ser.close()
cv2.destroyAllWindows()
