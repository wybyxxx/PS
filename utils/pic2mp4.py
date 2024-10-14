import time

import cv2
import os
from natsort import natsorted
from tqdm import tqdm

start = time.time()

# 图片文件夹路径
image_folder = '../Depth_Anything/data/20240929/equirect'
output_video = '../Depth_Anything/data/20240929/equirect.mp4'

# image_folder = r'D:\app\Zotero\BaiduSyncdisk\jxufe\jxufe\codes\Depth_Anything\data\20240929\equirect'  # 替换为你存放 JPG 图片的文件夹路径
# output_video = r'D:\app\Zotero\BaiduSyncdisk\jxufe\jxufe\codes\Depth_Anything\data\20240929\equirect.mp4'  # 输出视频的文件名

# 获取所有图片文件名并按自然排序
images = [img for img in os.listdir(image_folder) if img.endswith(".png")]
images = natsorted(images)  # 使用 natsort 进行自然排序

# 读取第一张图片获取视频尺寸
first_image = cv2.imread(os.path.join(image_folder, images[0]))
height, width, layers = first_image.shape

# 定义视频编解码器为 XVID 和输出视频的帧率
fourcc = cv2.VideoWriter_fourcc(*'XVID')  # 使用 XVID 编码器
fps = 5  # 每秒30帧，可根据需要调整
video = cv2.VideoWriter(output_video, fourcc, fps, (width, height))

# 将每张图片写入视频
for image in tqdm(images, desc="Processing", unit='image'):
    img_path = os.path.join(image_folder, image)
    frame = cv2.imread(img_path)
    video.write(frame)

# 释放资源
video.release()
cv2.destroyAllWindows()
print(time.time() - start)
