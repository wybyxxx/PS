import numpy as np
import OpenEXR
import Imath
import matplotlib.pyplot as plt


def read_exr(file_path):
    # 打开EXR文件
    exr_file = OpenEXR.InputFile(file_path)

    # 获取图像的宽度和高度
    header = exr_file.header()
    dw = header['dataWindow']
    size = (dw.max.x - dw.min.x + 1, dw.max.y - dw.min.y + 1)

    # 读取颜色通道
    FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)
    R = np.frombuffer(exr_file.channel('R', FLOAT), dtype=np.float32)
    G = np.frombuffer(exr_file.channel('G', FLOAT), dtype=np.float32)
    B = np.frombuffer(exr_file.channel('B', FLOAT), dtype=np.float32)

    # 重塑数据为图像形状
    R = np.reshape(R, (size[1], size[0]))
    G = np.reshape(G, (size[1], size[0]))
    B = np.reshape(B, (size[1], size[0]))

    # 合并为一个图像
    img = np.dstack((R, G, B))

    return img


# 指定EXR文件路径
file_path = r"E:\JUFE\codes\Real-Time Sphere Sweeping Stereo from Multiview Fisheye Images\sphere-stereo\resources\output\inv_distance_0.exr"

# 读取EXR文件
img = read_exr(file_path)

# 显示图像
plt.imshow(img)
plt.show()