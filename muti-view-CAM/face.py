"""
人脸检测就是通过摄像头实时获取的图片，来标记出人脸的位置。本节代码的目的就是将摄
像头拍摄的画面中的人脸用矩形框表示出来。人脸检测的本质是特征识别，OpenMV中已经集
成了非常多的特征库和算法库，比如image模块下的find_features()特征寻找函数。

利用Haar Cascade特征检测器来实现：一个Haar Cascade是一系列简单区域的对比检查，
人脸识别有25个阶段，每个阶段有几百次检测。Haar Cascade运行很快是因为它是逐个阶
段进行检测的。OpenMV使用一种称为积分图像的数据结构来在恒定时间内快速执行每个
区域的对比度检查
"""
#导入相应库
import sensor, time, image
from pyb import UART

# 初始化摄像头
sensor.reset()






move_x=0
move_y=0

servo0=1500
servo1=1500

uart.write("{{#000P{:0>4d}T1000!#001P{:0>4d}T1000!}}\n".format(servo0,servo1))


# FPS clock
clock = time.clock()

while (True):

    #拍摄一张照片
    img = sensor.snapshot()

    faces = img.find_features(face_cascade, threshold=0.85, scale=1.35)
    """
    image.find_features(cascade, threshold=0.5, scale=1.5, roi)
    搜索和Haar Cascade匹配的所有区域的图像，并返回一个关于这些特征的边界框矩形元祖(x, ,y, w, h)的列表，若没有发现任何特征，
    则返回一个空白列表。基于Haar特征的cascade分类器一种有效的物品检测(object detect)方法。它是一种机器学习方法，通过许多
    正负样例中训练得到cascade方程，然后将其应用于其他图片。详细内容可以参考博客：使用Haar Cascade 进行人脸识别
    cascade：Haar Cascade 对象
    threshold: 是浮点数（0.0-1.0），其中较小的值在提高检测速率同时增加误报率。相反，较高的值会降低检测速率，同时降低误报率。
    scale: 是一个必须大于1.0的浮点数。较高的比例因子运行更快，但是其图像匹配相应较差。理想值介于1.35到1.5之间。
    roi:指定识别区域的矩形元组(x, y, w, h)。如果没有指定，roi即整个图像的图像矩形。
    """
    #在找到的目标上画框，标记出来
    if faces:
        #追踪人脸
        max_size = 0
        max_blob=faces[0]
        for blob in faces:#寻找最大人脸
            if blob[2] * blob[3] > max_size:
                max_blob = blob
                max_size = blob[2] * blob[3]
        face=max_blob

        cx = int(face[0] + face[2] / 2)
        cy = int(face[1] + face[3] / 2)
        #img.draw_rectangle(face,color=(255,0,0))       #在目标区域的画方框
        #img.draw_cross(cx, cy, size=2,color=(255,0,0)) #在目标区域的中心点处画十字

        #-------------------机械臂执行跟随--------------------
        if(abs(cx-120)>=5):
            if cx > 120:
                move_x=-0.3*abs(cx-120)
            else:
                move_x=0.3*abs(cx-120)
            servo0=int(servo0+move_x)

        if(abs(cy-80)>=5):
            if cy < 80:
                move_y=-0.3*abs(cy-80)
            else:
                move_y=0.3*abs(cy-80)

            servo1=int(servo1-move_y)


        if servo0>2400: servo0=2400
        elif servo0<600: servo0=600
        if servo1>2300: servo1=2300
        elif servo1<700: servo1=700


        uart.write("{{#000P{:0>4d}T0000!#001P{:0>4d}T0000!}}".format(servo0,servo1))
        time.sleep_ms(20)



