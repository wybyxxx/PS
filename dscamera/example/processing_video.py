import cv2
from dscamera import DSCamera
import json

if __name__ == "__main__":
    json_file = "./calibration3-5.json"
    cam = DSCamera(json_file)

    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 参数为设备索引号或文件路径
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 1280)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 960)
    cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FPS, 30)
    # fourcc = cv2.VideoWriter_fourcc(*'H264')
    # out = cv2.VideoWriter('./output.mp4', fourcc, 30.0, (1280, 960))

    while (cap.isOpened()):

        ret, frame = cap.read()
        # 处理帧
        perspective = cam.to_perspective(frame, img_size=(512, 512))
        equirect = cam.to_equirect(frame, img_size=(512, 1024))

        # 显示
        cv2.imshow("orig", frame)
        cv2.imshow('Perspective Transform', perspective)
        cv2.imshow('Equirectangular Projection', equirect)

        # 写入视频文件
        # out.write(equirect)  # 假设我们只记录equirect结果
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 释放资源
    cap.release()
    # out.release()
    cv2.destroyAllWindows()



