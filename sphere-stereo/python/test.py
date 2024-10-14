import OpenEXR
import Imath
import numpy as np
import os
import matplotlib.pyplot as plt

# 读取 EXR 文件
file_path = r'E:\JUFE\codes\Real-Time Sphere Sweeping Stereo from Multiview Fisheye Images\sphere-stereo\evaluation_dataset2\gt\inv_distance_0.exr'
exr_file = OpenEXR.InputFile(file_path)

# 获取图像的宽度和高度
header = exr_file.header()
dw = header['dataWindow']
width = dw.max.x - dw.min.x + 1
height = dw.max.y - dw.min.y + 1

# 检查通道信息
channel_names = exr_file.header()['channels'].keys()
print("Available channels:", list(channel_names))

# 定义浮点类型
FLOAT = Imath.PixelType(Imath.PixelType.FLOAT)

# 读取 EXR 文件中的 R, G, B 三个通道（或者根据可用通道选择合适的）
if 'R' in channel_names and 'G' in channel_names and 'B' in channel_names:
    channels = ['R', 'G', 'B']
else:
    channels = list(channel_names)[:3]  # 选择前三个通道作为示例

# 读取通道数据并转换为 NumPy 数组
channel_data = [exr_file.channel(c, FLOAT) for c in channels]
images = [np.frombuffer(data, dtype=np.float32).reshape(height, width) for data in channel_data]

# 合并通道为 RGB 图像
img = np.stack(images, axis=-1)

# 展示图像
plt.imshow(np.clip(img, 0, 1))  # 使用 clip 以防像素值超出 [0, 1] 的范围
plt.title("EXR Image")
plt.axis('off')  # 关闭坐标轴
plt.show()
