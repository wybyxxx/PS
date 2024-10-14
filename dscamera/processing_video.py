from dscamera.camera import DSCamera
import cv2
import math
import numpy as np


def equirectangular_to_cylindrical(img, fov=180, cylindrical_w=2048, cylindrical_h=1024):
    img = np.asarray(img)
    h, w, _ = img.shape

    # Create meshgrid for the output cylindrical image
    x, y = np.meshgrid(np.arange(cylindrical_w), np.arange(cylindrical_h))

    # Constants for the conversion
    fov = (fov / 180) * math.pi  # 180 degrees field of view
    r = cylindrical_w / fov

    # Calculate theta and phi for each pixel in the cylindrical image
    theta = (x - cylindrical_w / 2) / r
    phi = (y - cylindrical_h / 2) / r

    # Calculate corresponding coordinates in the equirectangular image
    lon = theta
    lat = phi

    px = ((lon + math.pi) / (2 * math.pi) * w).astype(int)
    py = ((lat + (math.pi / 2)) / math.pi * h).astype(int)

    # Ensure the indices are within bounds
    px = np.clip(px, 0, w - 1)
    py = np.clip(py, 0, h - 1)

    # Use the indices to map the pixels
    cylindrical_img = img[py, px]
    print(type(cylindrical_img))
    return cylindrical_img


if __name__ == "__main__":

    json_file = "../dscamera/example/calibration3-0.json"
    ca = DSCamera(json_file)

    H = 960
    W = 1280

    HS = 2048
    WS = 1024

    # 初始化摄像头
    cap = cv2.VideoCapture(0)  # 参数为设备索引号或文件路径
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, W)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, H)
    cap.set(6, cv2.VideoWriter.fourcc('M', 'J', 'P', 'G'))
    cap.set(cv2.CAP_PROP_FPS, 30)

    i = 1
    while (cap.isOpened()):
        ret, frame = cap.read()
        # 处理帧  h w
        perspective = ca.to_perspective(frame, img_size=(1024, 1024))
        equirect = ca.to_equirect(frame, img_size=(1024, 2048))
        cylindrical = equirectangular_to_cylindrical(equirect)

        # 显示
        cv2.namedWindow("orig", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("orig", int(W / 2), int(H / 2))
        cv2.imshow("orig", frame)
        #
        cv2.namedWindow("Perspective Transform", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Perspective Transform", int(WS / 2), int(WS / 2))
        cv2.imwrite(r'D:\Files\jxufe\codes\dscamera\data\perspective\perspective{}.png'.format(i), perspective)
        cv2.imshow('Perspective Transform', perspective)

        cv2.namedWindow("Equirectangular Projection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("Equirectangular Projection", int(HS / 2), int(WS / 2))
        cv2.imwrite(r'D:\Files\jxufe\codes\dscamera\data\equirect\equirect{}.png'.format(i), equirect)
        cv2.imshow('Equirectangular Projection', equirect)


        cv2.namedWindow("cylindrical Projection", cv2.WINDOW_NORMAL)
        cv2.resizeWindow("cylindrical Projection", int(HS / 2), int(WS / 2))
        cylindrical = cylindrical.get()
        cv2.imwrite(r'D:\Files\jxufe\codes\dscamera\data\cylindrical\cylindrical{}.png'.format(i), cylindrical)
        cv2.imshow('cylindrical Projection', np.asnumpy(cylindrical))

        i += 1
        # 写入视频文件
        # out.write(equirect)  # 假设我们只记录equirect结果
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break

        # 释放资源
    cap.release()
    # out.release()
    cv2.destroyAllWindows()
