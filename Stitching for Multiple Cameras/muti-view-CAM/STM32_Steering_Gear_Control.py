# coding=utf-8
import time
import serial

#指定端口和波特率，波特率越高传输速度越快
ser = serial.Serial('COM6', 115200)

while(True):
    l = list(input("请输入舵机转动角度(格式为：水平舵机角度(0-270°),垂直舵机角度(0-180°)): "))

    #水平舵机控制范围500-2500，对应角度为0-270°（1=0.135°，1°≈7.4）
    if l[0] <= 270 and l[0] >= 0:
        l[0] = int(7.4*l[0]+500)
        command = '''#000P%dT1000!''' % l[0]
        ser.write(command)
    else:
        print("水平舵机超出转动范围！（0-270°）")
        pass

    # 两个舵机的指令不能发送太快，不然只会执行一条指令
    time.sleep(0.1)

    # 垂直平舵机控制范围830-2200，对应角度为0-180°（1=0.131°，1°≈7.6）
    if l[1] <= 180 and l[1] >= 0 :
        l[1] = int(7.6*l[1]+830)
        command1 = '''#001P%dT1001!''' % l[1]
        ser.write(command1)
    else:
        print("垂直舵机超出转动范围！（0-180°）")
        pass
    print(l)

ser.close()